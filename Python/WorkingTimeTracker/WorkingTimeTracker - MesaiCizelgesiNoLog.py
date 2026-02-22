#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WorkingTimeTracker - MesaiCizelgesiNoLog

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
RESULT_FILE_PREFIX = "Rapor"
FOLDER_DATE_FORMAT = "%Y.%m.%d_%H.%M.%S"
RESULT_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
MAX_HOURS_PER_DAY = 24
MIN_HOURS_PER_DAY = 0

# ============================== AUTO INSTALLATION ==============================

def install_packages():
    packages = ['pandas', 'openpyxl', 'xlrd']
    missing = []
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    if missing:
        for package in missing:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--user", package, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except Exception as e:
                    sys.exit(1)
        os.execl(sys.executable, sys.executable, *sys.argv)

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
        return None
    original_str = str(time_value).strip()
    time_str = original_str
    if ',' in time_str:
        time_str = time_str.replace(',', '.')
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                h = int(parts[0])
                m = int(parts[1])
                s = int(parts[2])
                return h + m/60 + s/3600
            elif len(parts) == 2:
                h = int(parts[0])
                m = int(parts[1])
                return h + m/60
        if time_str.endswith('.0') and time_str.replace('.0', '').isdigit():
            base = time_str.replace('.0', '')
            if len(base) == 4:
                h = int(base[0:2])
                m = int(base[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    return h + m/60
            elif len(base) == 3:
                h = int(base[0:1])
                m = int(base[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    return h + m/60
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
                    return h + m/60
            except ValueError:
                pass
        clean = time_str.replace('.', '').replace(',', '')
        if clean.isdigit():
            if len(clean) == 6:
                h = int(clean[0:2])
                m = int(clean[2:4])
                s = int(clean[4:6])
                if 0 <= h <= 24 and 0 <= m <= 59 and 0 <= s <= 59:
                    return h + m/60 + s/3600
            elif len(clean) == 4:
                h = int(clean[0:2])
                m = int(clean[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    return h + m/60
            elif len(clean) == 3:
                h = int(clean[0:1])
                m = int(clean[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    return h + m/60
            elif len(clean) <= 2:
                return float(clean)
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
                return h + m/60 + s/3600
        except ValueError:
            pass
    except Exception:
        pass
    return None

# ============================== FILE FUNCTIONS ==============================

def find_file():
    files = []
    for pattern in FILE_PATTERNS:
        found = glob.glob(pattern)
        files.extend(found)
    if not files:
        return None
    if len(files) == 1:
        return files[0]
    return files[0]
def process_file(filepath):
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, header=None, encoding='utf-8')
        else:
            df = pd.read_excel(filepath, header=None)
    except Exception as e:
        return None
    header = df.iloc[0].tolist()
    employees = []
    for i in range(0, len(header), 2):
        if i < len(header) and pd.notna(header[i]) and str(header[i]).strip():
            name = str(header[i]).strip()
            employees.append(name)
    if not employees:
        return None
    data = df.iloc[1:].reset_index(drop=True)
    all_details = ""
    results = {}
    for idx, name in enumerate(employees):
        start_col = idx * 2
        end_col = start_col + 1
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
                start_hours = parse_time(start)
                end_hours = parse_time(end)
                if start_hours is not None and end_hours is not None:
                    if end_hours < start_hours:
                        end_hours += 24
                    diff = end_hours - start_hours
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
    try:
        timestamp = datetime.now().strftime(FOLDER_DATE_FORMAT)
        if not os.path.exists(ARCHIVE_FOLDER_NAME):
            os.makedirs(ARCHIVE_FOLDER_NAME)
        sub_archive = os.path.join(ARCHIVE_FOLDER_NAME, timestamp)
        os.makedirs(sub_archive, exist_ok=True)
        return sub_archive
    except Exception as e:
        return None
def save_results(results, details_text, original, archive_folder):
    try:
        result_file = f"{RESULT_FILE_PREFIX}.txt"
        result_path = os.path.join(archive_folder, result_file)
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
        footer += f"{'=' * 41} {line1} {'=' * 41}\n"
        footer += f"{'=' * 41} {line2} {'=' * 41}\n"
        footer += "=" * 123 + "\n"
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write(details_header)
            f.write(processed_details)
            f.write(footer)
        return result_path
    except Exception as e:
        return None
def copy_original(original, archive_folder):
    try:
        time.sleep(1)
        target_path = os.path.join(archive_folder, os.path.basename(original))
        shutil.copy2(original, target_path)
        return True
    except Exception as e:
        return False

# ============================== MAIN PROGRAM ==============================

def main():
    archive_folder = None
    try:
        file = find_file()
        if not file:
            return
        result = process_file(file)
        if not result:
            return
        results_dict, details_text = result
        archive_folder = create_archive_folder()
        if not archive_folder:
            return
        result_path = save_results(results_dict, details_text, file, archive_folder)
        if not result_path:
            return
        copy_original(file, archive_folder)
    except Exception as e:
        pass

# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    main()