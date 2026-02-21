#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WorkingTimeTracker - Turkish

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
RESULT_FILE_PREFIX = "Result"
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
    total_seconds = int(round(hours * 3600))
    h = total_seconds // 3600
    rest = total_seconds % 3600
    m = rest // 60
    s = rest % 60
    return h, m, s
def format_hms(hours):
    h, m, s = hours_to_hms(hours)
    return f"{h}s {m}d {s}sn"
def hours_to_minutes(hours):
    return int(round(hours * 60))
def hours_to_seconds(hours):
    return int(round(hours * 3600))

# ============================== TIME PARSING FUNCTION ==============================

def parse_time(time_value):
    if pd.isna(time_value) or str(time_value).strip() == '':
        log_write(f"⏱️ Boş zaman değeri", "DEBUG")
        return None
    time_str = str(time_value).strip()
    log_write(f"⏱️ Çözümleniyor: '{time_str}'", "DEBUG")
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                result = int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
                log_write(f"  → ss:dd:sn formatı = {result:.2f}s", "DEBUG")
                return result
            elif len(parts) == 2:
                result = int(parts[0]) + int(parts[1])/60
                log_write(f"  → ss:dd formatı = {result:.2f}s", "DEBUG")
                return result
        if '.' in time_str:
            num_str = time_str.replace('.0', '')
            if num_str.isdigit():
                if len(num_str) == 4:
                    result = int(num_str[0:2]) + int(num_str[2:4])/60
                    log_write(f"  → 4 haneli noktalı = {result:.2f}s", "DEBUG")
                    return result
                elif len(num_str) == 3:
                    result = int(num_str[0:1]) + int(num_str[1:3])/60
                    log_write(f"  → 3 haneli noktalı = {result:.2f}s", "DEBUG")
                    return result
                elif len(num_str) <= 2:
                    result = float(num_str)
                    log_write(f"  → noktalı sayı = {result:.2f}s", "DEBUG")
                    return result
        if time_str.isdigit():
            number = int(time_str)
            if len(time_str) == 6:
                result = int(time_str[0:2]) + int(time_str[2:4])/60 + int(time_str[4:6])/3600
                log_write(f"  → 6 haneli = {result:.2f}s", "DEBUG")
                return result
            elif len(time_str) == 4:
                h = int(time_str[0:2])
                m = int(time_str[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 4 haneli = {result:.2f}s", "DEBUG")
                    return result
            elif len(time_str) == 3:
                h = int(time_str[0:1])
                m = int(time_str[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → 3 haneli = {result:.2f}s", "DEBUG")
                    return result
            elif len(time_str) <= 2:
                result = float(number)
                log_write(f"  → basit sayı = {result:.2f}s", "DEBUG")
                return result
        try:
            number = float(time_str)
            if 0 <= number <= 24:
                if number == int(number):
                    result = number
                    log_write(f"  → Excel tamsayı = {result:.2f}s", "DEBUG")
                    return result
                else:
                    h = int(number)
                    m = int((number - h) * 60 + 0.5)
                    result = h + m/60
                    log_write(f"  → Excel ondalık = {result:.2f}s", "DEBUG")
                    return result
        except:
            pass
    except Exception as e:
        log_write(f"  ❌ Çözümleme hatası: {e}", "ERROR")
    log_write(f"  ❌ Çözümlenemedi", "WARN")
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
        day_text = f"\n👤 {name}:\n"
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
                    diff = round(end_hours - start_hours, 2)
                    log_write(f"    → Fark: {diff:.2f}s", "DEBUG")
                    if MIN_HOURS_PER_DAY < diff < MAX_HOURS_PER_DAY:
                        total += diff
                        days_worked += 1
                        daily_values.append(diff)
                        h, m, s = hours_to_hms(diff)
                        minutes = hours_to_minutes(diff)
                        seconds = hours_to_seconds(diff)
                        line = f"  Gün {row_idx+1}: {start} - {end} = {h}s{m:02d}d{s:02d}sn   {diff:.2f}s   {minutes}d   {seconds}sn"
                        day_text += line + "\n"
                        log_write(f"  ✅ {line}", "CALC")
                    else:
                        day_text += f"  Gün {row_idx+1}: {start} - {end} = ? (geçersiz: {diff:.2f}s)\n"
                        log_write(f"  ⚠️ Geçersiz fark: {diff:.2f}s", "WARN")
                else:
                    day_text += f"  Gün {row_idx+1}: {start} - {end} = ? (çözümlenemedi)\n"
                    log_write(f"  ⚠️ Çözümlenemedi", "WARN")
        avg = round(total/days_worked, 2) if days_worked > 0 else 0
        h_avg, m_avg, s_avg = hours_to_hms(avg)
        min_avg = hours_to_minutes(avg)
        sec_avg = hours_to_seconds(avg)
        total_hms = format_hms(total)
        total_min = hours_to_minutes(total)
        total_sec = hours_to_seconds(total)
        summary_line = f"  📊 Toplam: {total_hms} / {days_worked} gün (günlük ortalama: {h_avg}s{m_avg:02d}d{s_avg:02d}sn) ({avg:.2f}s/gün) ({min_avg}d/gün) ({sec_avg}sn/gün)"
        day_text += summary_line + "\n"
        log_write(summary_line, "RESULT")
        log_write(f"    Dakika cinsinden toplam: {total_min}d, saniye cinsinden: {total_sec}sn", "DEBUG")
        all_details += day_text
        results[name] = {
            'total': round(total, 2),
            'total_hms': total_hms,
            'total_min': total_min,
            'total_sec': total_sec,
            'days': days_worked
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
        summary += f"{'Müderris':<30} {'Toplam (s/d/sn)':>20} {'Toplam (s)':>12} {'Toplam (d)':>12} {'Toplam (sn)':>12} {'Gün':>8}\n"
        summary += "-" * 120 + "\n"
        total_all = 0
        days_all = 0
        for name, r in results.items():
            summary += f"{name:<30} {r['total_hms']:>20} {r['total']:>12.2f} {r['total_min']:>12} {r['total_sec']:>12} {r['days']:>8}\n"
            total_all += r['total']
            days_all += r['days']
        total_all_hms = format_hms(total_all)
        total_all_min = hours_to_minutes(total_all)
        total_all_sec = hours_to_seconds(total_all)
        summary += "-" * 120 + "\n"
        summary += f"{'TÜM MÜDERRISLER':<30} {total_all_hms:>20} {total_all:>12.2f} {total_all_min:>12} {total_all_sec:>12} {days_all:>8}\n"
        summary += "\n"
        details_header = "=" * 123 + "\n"
        details_header += "=" * 49 + " 📋 MÜDERRIS BAZINDA DETAYLAR " + "=" * 50 + "\n"
        details_header += "=" * 123 + "\n\n"
        processed_details = ""
        employee_blocks = details_text.strip().split("\n\n👤 ")
        for i, block in enumerate(employee_blocks):
            if i == 0:
                if block.startswith("👤"):
                    processed_details += block
                else:
                    processed_details += "👤 " + block
            else:
                processed_details += "\n" + "-" * 123 + "\n👤 " + block
        processed_details += "\n"
        completion = "\n" + "=" * 123 + "\n"
        completion += "=" * 52 + " Tamamlandı " + "=" * 53 + "\n"
        completion += "=" * 123 + "\n\n"
        footer = f"📁 Orijinal dosya: {original}\n"
        footer += f"📅 Hesaplanma tarihi: {datetime.now().strftime(RESULT_DATE_FORMAT)}\n"
        footer += f"📋 Log dosyası: {LOG_FILE}\n"
        footer += "\n" + "=" * 123 + "\n"
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write(details_header)
            f.write(processed_details)
            f.write(completion)
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
        results = process_file(file)
        if not results:
            log_save()
            return
        archive_folder = create_archive_folder()
        if not archive_folder:
            log_save()
            return
        results_dict, details_text = results
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