#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WorkingTimeTracker - MesaiCizelgesi

# ============================== IMPORTS ==============================

import subprocess
import sys
import os
import time
import shutil
import traceback
from datetime import datetime

# ============================== CONFIGURATION VARIABLES ==============================

FILE_PATTERNS = ["MesaiCizelgesi*.csv", "MesaiCizelgesi*.xlsx"]
ARCHIVE_FOLDER_NAME = "Archive"
LOG_FILE_PREFIX = "Log"
RESULT_FILE_PREFIX = "Rapor"
FOLDER_DATE_FORMAT = "%Y.%m.%d_%H.%M.%S"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
RESULT_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
MAX_HOURS_PER_DAY = 24
MIN_HOURS_PER_DAY = 0

# ============================== LOGGING SETUP ==============================

def get_timestamp():
    return datetime.now().strftime(FOLDER_DATE_FORMAT)
LOG_TIMESTAMP = get_timestamp()
LOG_FILE = f"{LOG_FILE_PREFIX}.txt"
log_lines = []
script_successful = False
error_message = ""
def log_write(text, level="INFO"):
    timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
    if text.startswith("="):
        log_line = f"[{timestamp}] [{level}]   {text}"
    else:
        log_line = f"[{timestamp}] [{level}]      {text}"
    log_lines.append(log_line)
def log_save(archive_folder=None):
    global script_successful, error_message
    try:
        if archive_folder:
            log_path = os.path.join(archive_folder, LOG_FILE)
        else:
            log_path = LOG_FILE
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(f"MESAI ÇIZERGESI - TAM LOG\n")
            f.write(f"Oluşturulma: {datetime.now().strftime(RESULT_DATE_FORMAT)}\n")
            f.write(f"Durum: {'✅ BAŞARILI' if script_successful else '❌ BAŞARISIZ'}\n")
            if error_message:
                f.write(f"Hata: {error_message}\n")
            f.write("=" * 100 + "\n\n")
            for line in log_lines:
                f.write(line + "\n")
        return log_path
    except Exception as e:
        try:
            with open("emergency_log.txt", 'w', encoding='utf-8') as f:
                f.write(f"Acil durum log - {datetime.now()}\n")
                f.write(f"Hata: {e}\n")
                for line in log_lines:
                    f.write(line + "\n")
        except:
            pass
        return None
def set_error(error_msg):
    global error_message, script_successful
    error_message = error_msg
    script_successful = False
    log_write(f"❌ HATA: {error_msg}", "ERROR")

# ============================== AUTO INSTALLATION ==============================

def install_packages():
    log_write("=" * 60, "SYSTEM")
    log_write("🔧 OTOMATİK KURULUM", "SYSTEM")
    log_write("=" * 60, "SYSTEM")
    packages = ['pandas', 'openpyxl', 'xlrd']
    missing = []
    for package in packages:
        try:
            __import__(package)
            log_write(f"✅ {package} zaten kurulu", "INSTALL")
        except ImportError:
            log_write(f"⚠️ {package} bulunamadı", "INSTALL")
            missing.append(package)
    if missing:
        log_write(f"📦 Kuruluyor: {', '.join(missing)}", "INSTALL")
        for package in missing:
            log_write(f"→ {package} kuruluyor...", "INSTALL")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                log_write(f"  ✅ {package} kuruldu", "INSTALL")
            except:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--user", package, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    log_write(f"  ✅ {package} kuruldu (kullanıcı modu)", "INSTALL")
                except Exception as e:
                    set_error(f"{package} kurulamadı: {str(e)}")
                    log_save()
                    sys.exit(1)
        log_write("✅ Kurulum tamamlandı! Yeniden başlatılıyor...", "INSTALL")
        log_save()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        log_write("✅ Tüm paketler mevcut", "INSTALL")

# ============================== IMPORTS ==============================

install_packages()
import pandas as pd
import glob

# ============================== TIME CONVERSION FUNCTIONS ==============================

def hours_to_hms(hours):
    total_seconds = hours * 3600
    h = int(total_seconds // 3600)
    rest = total_seconds - (h * 3600)
    m = int(rest // 60)
    s = rest - (m * 60)
    if s >= 59.9999:
        s = 0
        m += 1
        if m >= 60:
            m = 0
            h += 1
    return h, m, s
def format_hms(hours):
    h, m, s = hours_to_hms(hours)
    if abs(s - int(s)) < 0.01:
        if int(s) == 0:
            return f"{h}s{m:02d}d00sn"
        else:
            return f"{h}s{m:02d}d{int(s):02d}sn"
    else:
        s_str = f"{s:.2f}".replace('.', ',').rstrip('0').rstrip(',')
        return f"{h}s{m:02d}d{s_str}sn"
def format_minutes_rounded(minutes):
    if minutes == int(minutes):
        return int(minutes)
    else:
        return int(minutes) + 1
def format_number(value):
    if abs(value - int(value)) < 0.001:
        return f"{int(value)}"
    else:
        return f"{value:.2f}".replace('.', ',').rstrip('0').rstrip(',')
def hours_to_minutes(hours):
    return hours * 60
def hours_to_seconds(hours):
    return hours * 3600

# ============================== TIME PARSING FUNCTION ==============================

def parse_time(time_value):
    if pd.isna(time_value) or str(time_value).strip() == '':
        log_write(f"⏱️ Boş zaman değeri", "DEBUG")
        return None
    original_str = str(time_value).strip()
    time_str = original_str
    if ',' in time_str:
        time_str = time_str.replace(',', '.')
        log_write(f"⏱️ Komma durch Punkt ersetzt: '{time_str}'", "DEBUG")
    log_write(f"⏱️ Çözümleniyor: '{time_str}'", "DEBUG")
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                h = int(parts[0])
                m = int(parts[1])
                s = int(parts[2])
                result = h + m/60 + s/3600
                log_write(f"  → SS:DD:SN = {h:02d}:{m:02d}:{s:02d} = {result:.6f}s", "DEBUG")
                return result
            elif len(parts) == 2:
                h = int(parts[0])
                m = int(parts[1])
                result = h + m/60
                log_write(f"  → SS:DD = {h:02d}:{m:02d} = {result:.6f}s", "DEBUG")
                return result
        if time_str.endswith('.0') and time_str.replace('.0', '').isdigit():
            base = time_str.replace('.0', '')
            if len(base) == 4:  # 1705.0 -> 1705
                h = int(base[0:2])
                m = int(base[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 4-stellig mit .0 = {h:02d}:{m:02d} = {result:.6f}s", "DEBUG")
                    return result
            elif len(base) == 3:  # z.B. 905.0 -> 905
                h = int(base[0:1])
                m = int(base[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 3-stellig mit .0 = {h:02d}:{m:02d} = {result:.6f}s", "DEBUG")
                    return result
        punkt_count = time_str.count('.')
        if punkt_count == 1 or (',' in original_str and punkt_count == 0):
            try:
                zahl = float(time_str)
                if 0 <= zahl <= 24:
                    h = int(zahl)
                    m = int(round((zahl - h) * 60))
                    if m == 60:
                        h += 1
                        m = 0
                    result = h + m/60
                    log_write(f"  → Dezimal = {zahl} -> {h}h {m}m = {result:.6f}s", "DEBUG")
                    return result
            except ValueError:
                pass
        clean = time_str.replace('.', '').replace(',', '')
        if clean.isdigit():
            if len(clean) == 6:
                h = int(clean[0:2])
                m = int(clean[2:4])
                s = int(clean[4:6])
                if 0 <= h <= 24 and 0 <= m <= 59 and 0 <= s <= 59:
                    result = h + m/60 + s/3600
                    log_write(f"  → 6-stellig = {h:02d}:{m:02d}:{s:02d} = {result:.6f}s", "DEBUG")
                    return result
            elif len(clean) == 4:
                h = int(clean[0:2])
                m = int(clean[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 4-stellig = {h:02d}:{m:02d} = {result:.6f}s", "DEBUG")
                    return result
            elif len(clean) == 3:
                h = int(clean[0:1])
                m = int(clean[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 3-stellig = {h:02d}:{m:02d} = {result:.6f}s", "DEBUG")
                    return result
            elif len(clean) <= 2:
                result = float(clean)
                log_write(f"  → einfache Zahl = {result:.2f}s", "DEBUG")
                return result
        try:
            zahl = float(time_str)
            if 0 <= zahl <= 24:
                h = int(zahl)
                m = int((zahl - h) * 60 + 0.0001)
                s = int(((zahl - h) * 60 - m) * 60 + 0.5)
                if s >= 60:
                    s = 0
                    m += 1
                    if m >= 60:
                        m = 0
                        h += 1
                result = h + m/60 + s/3600
                log_write(f"  → Excel-Zahl = {zahl} -> {h:02d}:{m:02d}:{s:02d} = {result:.6f}s", "DEBUG")
                return result
        except ValueError:
            pass
    except Exception as e:
        log_write(f"  ❌ Çözümleme hatası: {e}", "ERROR")
    log_write(f"  ❌ Çözümlenemedi: '{original_str}'", "WARN")
    return None

# ============================== FILE FUNCTIONS ==============================

def find_file():
    log_write("-" * 60, "STEP")
    log_write("🔍 ADIM 1: DOSYA ARANIYOR", "STEP")
    log_write("-" * 60, "STEP")
    files = []
    for pattern in FILE_PATTERNS:
        found = glob.glob(pattern)
        files.extend(found)
        log_write(f"  Şablon {pattern}: {len(found)} bulundu", "FILE")
    if not files:
        set_error("MesaiCizelgesi dosyası bulunamadı!")
        log_write("📁 Klasördeki dosyalar:", "INFO")
        for f in os.listdir('.'):
            if os.path.isfile(f):
                log_write(f"  - {f}", "INFO")
        return None
    if len(files) == 1:
        log_write(f"✅ Bulunan: {files[0]}", "FILE")
        return files[0]
    log_write(f"📁 Birden fazla dosya bulundu:", "FILE")
    for i, f in enumerate(files, 1):
        log_write(f"  {i}. {f}", "FILE")
    log_write(f"✅ İlk dosya seçildi: {files[0]}", "FILE")
    return files[0]
def process_file(filepath):
    log_write("-" * 60, "STEP")
    log_write("📄 ADIM 2: DOSYA OKUNUYOR", "STEP")
    log_write("-" * 60, "STEP")
    log_write(f"  Dosya: {filepath}", "FILE")
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, header=None, encoding='utf-8')
            log_write("  ✅ CSV başarıyla okundu", "FILE")
        else:
            df = pd.read_excel(filepath, header=None)
            log_write("  ✅ Excel başarıyla okundu", "FILE")
    except Exception as e:
        set_error(f"Dosya okuma hatası: {e}")
        return None
    log_write(f"  Satır: {len(df)}, Sütun: {len(df.columns)}", "FILE")
    log_write("-" * 60, "STEP")
    log_write("👥 ADIM 3: ÇALIŞANLAR TESPİT EDİLİYOR", "STEP")
    log_write("-" * 60, "STEP")
    header = df.iloc[0].tolist()
    log_write(f"  Satır 1 (ham veri): {header}", "DEBUG")
    employees = []
    for i in range(0, len(header), 2):
        if i < len(header) and pd.notna(header[i]) and str(header[i]).strip():
            name = str(header[i]).strip()
            employees.append(name)
            log_write(f"  Sütun {i}-{i+1}: {name}", "EMPLOYEE")
    if not employees:
        set_error("1. satırda Müderris bulunamadı!")
        return None
    log_write(f"✅ Müderrisler: {', '.join(employees)}", "EMPLOYEE")
    data = df.iloc[1:].reset_index(drop=True)
    log_write(f"📊 Veri satırları: {len(data)}", "DATA")
    log_write("-" * 60, "STEP")
    log_write("🧮 ADIM 4: SAATLER HESAPLANIYOR", "STEP")
    log_write("-" * 60, "STEP")
    all_details = ""
    results = {}
    for idx, name in enumerate(employees):
        start_col = idx * 2
        end_col = start_col + 1
        log_write(f"\n👤 {name}:", "CALC")
        total = 0
        days_worked = 0
        daily_values = []
        day_text = "-" * 120 + "\n"
        day_text += f"{(' 👤 Müderris ' + name + ' Efendi'):^120}\n"
        day_text += "-" * 120 + "\n"
        for row_idx in range(len(data)):
            start = data.iloc[row_idx, start_col]
            end = data.iloc[row_idx, end_col]
            if pd.notna(start) and pd.notna(end) and str(start).strip() and str(end).strip():
                log_write(f"  Gün {row_idx+1}: {start} - {end}", "DEBUG")
                start_hours = parse_time(start)
                end_hours = parse_time(end)
                if start_hours is not None and end_hours is not None:
                    if end_hours < start_hours:
                        log_write(f"    → Gece vardiyası tespit edildi ({end_hours:.2f}s < {start_hours:.2f}s)", "DEBUG")
                        end_hours += 24
                    diff = end_hours - start_hours
                    log_write(f"    → Fark: {diff}f", "DEBUG")
                    if MIN_HOURS_PER_DAY < diff < MAX_HOURS_PER_DAY:
                        total += diff
                        days_worked += 1
                        daily_values.append(diff)
                        h, m, s = hours_to_hms(diff)
                        minutes = hours_to_minutes(diff)
                        seconds = hours_to_seconds(diff)
                        start_str = str(start).strip()
                        end_str = str(end).strip()
                        start_formatted = f"{start_str:>10}"
                        end_formatted = f"{end_str:>10}"
                        if abs(s - int(s)) < 0.001:
                            s_str = f"{int(s):02d}"
                        else:
                            s_str = f"{s:6.3f}".replace('.', ',')
                        minutes_rounded = format_minutes_rounded(minutes)
                        minutes_str = str(minutes_rounded)
                        seconds_str = format_number(seconds)
                        line = (f"Gün {row_idx+1:4d}: {start_formatted}  -{end_formatted}   ="
                               f"  {h:2d}s{m:02d}d{s_str}sn         {diff:8.6f}s        {minutes_str:>8}d     {seconds_str:>8}sn")
                        day_text += line + "\n"
                        log_write(f"  ✅ {line}", "CALC")
                    else:
                        start_str = str(start).strip()
                        end_str = str(end).strip()
                        start_formatted = f"{start_str:>10}"
                        end_formatted = f"{end_str:>10}"
                        day_text += f"  Gün {row_idx+1:2d}: {start_formatted} - {end_formatted} = ? (geçersiz: {diff:.2f}s)\n"
                        log_write(f"  ⚠️ Geçersiz fark: {diff:.2f}s", "WARN")
                else:
                    start_str = str(start).strip() if pd.notna(start) else ""
                    end_str = str(end).strip() if pd.notna(end) else ""
                    start_formatted = f"{start_str:>10}"
                    end_formatted = f"{end_str:>10}"
                    day_text += f"  Gün {row_idx+1:2d}: {start_formatted} - {end_formatted} = ? (çözümlenemedi)\n"
                    log_write(f"  ⚠️ Çözümlenemedi", "WARN")
        if days_worked > 0:
            avg = total / days_worked
            h_avg, m_avg, s_avg = hours_to_hms(avg)
            if abs(s_avg - int(s_avg)) < 0.001:
                s_avg_str = f"{int(s_avg):02d}"
            else:
                s_avg_str = f"{s_avg:.2f}".replace('.', ',').rstrip('0').rstrip(',')
            total_hms = format_hms(total)
            total_min = hours_to_minutes(total)
            total_sec = hours_to_seconds(total)
            avg_min = hours_to_minutes(avg)
            avg_sec = hours_to_seconds(avg)
            total_hms_formatted = f"{total_hms:>15}"
            total_formatted = f"{total:>12.6f}s"
            total_min_rounded = format_minutes_rounded(total_min)
            total_sec_formatted = f"{format_number(total_sec):>8}sn"
            avg_hms_formatted = f"{h_avg}s{m_avg:02d}d{s_avg_str}sn"
            avg_formatted = f"{avg:>12.6f}s"
            avg_min_rounded = format_minutes_rounded(avg_min)
            avg_sec_formatted = f"{format_number(avg_sec):>8}sn"
            toplam_text = f"       📊 Toplam {days_worked:4d} gün:"
            day_text += f"{toplam_text:<32} {total_hms_formatted:>15}  {total_formatted:>16}  {total_min_rounded:>14}d  {total_sec_formatted:>13}       \n"
            day_text += f"       📊 Günlük Ortalama:        {avg_hms_formatted:>15}  {avg_formatted:>16}  {avg_min_rounded:>14}d  {avg_sec_formatted:>13}       \n"
            log_write(f"  📊 Toplam {days_worked} gün: {total_hms} {total:.6f}s {total_min_rounded}d {format_number(total_sec)}sn", "RESULT")
            log_write(f"  📊 Günlük Ortalama: {h_avg}s{m_avg:02d}d{s_avg_str}sn {avg:.6f}s {avg_min_rounded}d {format_number(avg_sec)}sn", "RESULT")
            all_details += day_text
            results[name] = {
                'total': total,
                'total_hms': total_hms,
                'total_min': total_min,
                'total_min_rounded': total_min_rounded,
                'total_sec': total_sec,
                'days': days_worked,
                'avg': avg,
                'avg_hms': f"{h_avg}s{m_avg:02d}d{s_avg_str}sn",
                'avg_min': avg_min,
                'avg_min_rounded': avg_min_rounded,
                'avg_sec': avg_sec
            }
        else:
            day_text += f"  📊 Toplam: 0s00d00sn / 0 gün (günlük ortalama: 0s00d00sn)\n"
            all_details += day_text
            results[name] = {
                'total': 0,
                'total_hms': "0s00d00sn",
                'total_min': 0,
                'total_min_rounded': 0,
                'total_sec': 0,
                'days': 0,
                'avg': 0,
                'avg_hms': "0s00d00sn",
                'avg_min': 0,
                'avg_min_rounded': 0,
                'avg_sec': 0
            }
    return results, all_details
def create_archive_folder():
    log_write("-" * 60, "STEP")
    log_write("📁 ADIM 5: ARŞİV KLASÖRÜ OLUŞTURULUYOR", "STEP")
    log_write("-" * 60, "STEP")
    try:
        if not os.path.exists(ARCHIVE_FOLDER_NAME):
            os.makedirs(ARCHIVE_FOLDER_NAME)
            log_write(f"📁 Ana arşiv oluşturuldu: {ARCHIVE_FOLDER_NAME}", "ARCHIVE")
        else:
            log_write(f"📁 Ana arşiv mevcut: {ARCHIVE_FOLDER_NAME}", "ARCHIVE")
        sub_archive = os.path.join(ARCHIVE_FOLDER_NAME, LOG_TIMESTAMP)
        os.makedirs(sub_archive, exist_ok=True)
        log_write(f"📁 Alt klasör oluşturuldu: {sub_archive}", "ARCHIVE")
        return sub_archive
    except Exception as e:
        set_error(f"Arşiv klasörü oluşturulamadı: {e}")
        return None
def save_results(results, details_text, original, archive_folder):
    log_write("-" * 60, "STEP")
    log_write("💾 ADIM 6: SONUÇLAR KAYDEDİLİYOR", "STEP")
    log_write("-" * 60, "STEP")
    try:
        result_file = f"{RESULT_FILE_PREFIX}.txt"
        result_path = os.path.join(archive_folder, result_file)
        log_write(f"  Oluşturuluyor: {result_path}", "SAVE")
        summary = "=" * 123 + "\n"
        summary += "=" * 49 + " 📊 MÜDERRIS SAATLERİ - ÖZET " + "=" * 50 + "\n"
        summary += "=" * 123 + "\n\n"
        summary += f"{'Müderris':<30} {'Toplam (s/d/sn)':>20} {'Toplam (s)':>16} {'Toplam (d)':>16} {'Toplam (sn)':>16} {'Gün':>8}\n"
        summary += "-" * 120 + "\n"
        total_all = 0
        days_all = 0
        for name, r in results.items():
            if r['days'] > 0:
                total_min_rounded = r['total_min_rounded']
                total_sec_str = format_number(r['total_sec'])
                summary += f"{name:<26} {r['total_hms']:>22} {r['total']:>17.6f} {total_min_rounded:>16} {total_sec_str:>14} {r['days']:>11}\n"
                total_all += r['total']
                days_all += r['days']
            else:
                summary += f"{name:<26} {'0s00d00sn':>22} {0:>17.6f} {0:>16} {0:>14} {0:>11}\n"
        summary += "-" * 120 + "\n"
        total_all_hms = format_hms(total_all)
        total_all_min = hours_to_minutes(total_all)
        total_all_sec = hours_to_seconds(total_all)
        total_all_formatted = f"{total_all:.2f}".replace('.', ',')
        total_min_rounded = format_minutes_rounded(total_all_min)
        total_sec_str = format_number(total_all_sec)
        summary += f"{'TÜM MÜDERRISLER':<26} {total_all_hms:>22} {total_all_formatted:>17} {total_min_rounded:>16} {total_sec_str:>14} {days_all:>11}\n\n"
        details_header = "=" * 123 + "\n"
        details_header += "=" * 49 + " 📋 MÜDERRIS BAZINDA DETAYLAR " + "=" * 50 + "\n"
        details_header += "=" * 123 + "\n\n"
        processed_details = ""
        employee_blocks = details_text.strip().split("-" * 120 + "\n" + (" " * 60))
        for i, block in enumerate(employee_blocks):
            if block.strip():
                if i > 0:
                    processed_details += "\n"
                processed_details += block.strip()
        footer = "\n" + "-" * 120 + "\n"
        footer += "\n" + "=" * 123 + "\n"
        line1 = f"📁 Orijinal dosya: {original}"
        line2 = f"📅 Hesaplanma tarihi: {datetime.now().strftime(RESULT_DATE_FORMAT)}"
        line3 = f"📋 Log dosyası: {LOG_FILE}"
        footer += f"{'=' * 41} {line1} {'=' * 41}\n"
        footer += f"{'=' * 41} {line2} {'=' * 41}\n"
        footer += f"{'=' * 41} {line3} {'=' * 41}\n"
        footer += "=" * 123 + "\n"
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write(details_header)
            f.write(processed_details)
            f.write(footer)
        log_write(f"  ✅ Sonuçlar kaydedildi: {result_file}", "SAVE")
        return result_path
    except Exception as e:
        set_error(f"Sonuçlar kaydedilirken hata: {e}")
        return None
def copy_original(original, archive_folder):
    log_write("-" * 60, "STEP")
    log_write("📦 ADIM 7: ORİJİNAL DOSYA KOPYALANIYOR", "STEP")
    log_write("-" * 60, "STEP")
    try:
        time.sleep(1)
        target_path = os.path.join(archive_folder, os.path.basename(original))
        shutil.copy2(original, target_path)
        log_write(f"  ✅ Orijinal kopyalandı: {os.path.basename(original)}", "ARCHIVE")
        log_write(f"    → Hedef: {target_path}", "ARCHIVE")
        return True
    except Exception as e:
        log_write(f"  ⚠️ Kopyalama başarısız: {e}", "WARN")
        log_write("  📌 Dosyanın Excel'de açık olmadığından emin olun.", "HINT")
        return False

# ============================== MAIN PROGRAM ==============================

def main():
    global script_successful
    archive_folder = None
    try:
        log_write("=" * 100, "SYSTEM")
        log_write("🚀 MESAI ÇIZERGESI BAŞLATILDI", "SYSTEM")
        log_write(f"  Python Sürümü: {sys.version}", "SYSTEM")
        log_write(f"  Zaman damgası: {LOG_TIMESTAMP}", "SYSTEM")
        log_write("=" * 100, "SYSTEM")
        file = find_file()
        if not file:
            log_save()
            return
        result = process_file(file)
        if not result:
            log_save()
            return
        results_dict, details_text = result
        archive_folder = create_archive_folder()
        if not archive_folder:
            log_save()
            return
        result_path = save_results(results_dict, details_text, file, archive_folder)
        if not result_path:
            log_save()
            return
        copy_original(file, archive_folder)
        script_successful = True
        log_write("=" * 100, "SYSTEM")
        log_write("✨ TÜM ADIMLAR BAŞARIYLA TAMAMLANDI", "SYSTEM")
        log_write(f"  📁 Arşiv klasörü: {archive_folder}", "SYSTEM")
        log_write(f"  📄 Sonuç: {RESULT_FILE_PREFIX}.txt", "SYSTEM")
        log_write(f"  📋 Log: {LOG_FILE_PREFIX}.txt", "SYSTEM")
        log_write(f"  📦 Orijinal: {os.path.basename(file)}", "SYSTEM")
        log_write("=" * 100, "SYSTEM")
    except Exception as e:
        error_msg = f"Beklenmeyen hata: {str(e)}\n{traceback.format_exc()}"
        set_error(error_msg)
    finally:
        log_save(archive_folder)

# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    main()