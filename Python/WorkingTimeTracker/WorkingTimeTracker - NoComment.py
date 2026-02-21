#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WorkingTimeTracker

# ============================== IMPORTS ==============================

import subprocess
import sys
import os
import time
import shutil
import traceback
from datetime import datetime

# ============================== CONFIGURATION VARIABLES ==============================

FILE_PATTERNS = ["WorkingTimeTracker*.csv", "WorkingTimeTracker*.xlsx"]
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
            f.write(f"WORKING TIME TRACKER - COMPLETE LOG\n")
            f.write(f"Created: {datetime.now().strftime(RESULT_DATE_FORMAT)}\n")
            f.write(f"Status: {'✅ SUCCESSFUL' if script_successful else '❌ FAILED'}\n")
            if error_message:
                f.write(f"Error: {error_message}\n")
            f.write("=" * 100 + "\n\n")
            for line in log_lines:
                f.write(line + "\n")
        return log_path
    except Exception as e:
        try:
            with open("emergency_log.txt", 'w', encoding='utf-8') as f:
                f.write(f"Emergency log - {datetime.now()}\n")
                f.write(f"Error: {e}\n")
                for line in log_lines:
                    f.write(line + "\n")
        except:
            pass
        return None
def set_error(error_msg):
    global error_message, script_successful
    error_message = error_msg
    script_successful = False
    log_write(f"❌ ERROR: {error_msg}", "ERROR")

# ============================== AUTO INSTALLATION ==============================

def install_packages():
    log_write("=" * 60, "SYSTEM")
    log_write("🔧 AUTO INSTALLATION", "SYSTEM")
    log_write("=" * 60, "SYSTEM")
    packages = ['pandas', 'openpyxl', 'xlrd']
    missing = []
    for package in packages:
        try:
            __import__(package)
            log_write(f"✅ {package} already installed", "INSTALL")
        except ImportError:
            log_write(f"⚠️ {package} not found", "INSTALL")
            missing.append(package)
    if missing:
        log_write(f"📦 Installing: {', '.join(missing)}", "INSTALL")
        for package in missing:
            log_write(f"→ Installing {package}...", "INSTALL")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                log_write(f"  ✅ {package} installed", "INSTALL")
            except:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--user", package, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    log_write(f"  ✅ {package} installed (user mode)", "INSTALL")
                except Exception as e:
                    set_error(f"Failed to install {package}: {str(e)}")
                    log_save()
                    sys.exit(1)
        log_write("✅ Installation complete! Restarting...", "INSTALL")
        log_save()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        log_write("✅ All packages available", "INSTALL")

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
    return f"{h}h {m}m {s}s"
def hours_to_minutes(hours):
    return int(round(hours * 60))
def hours_to_seconds(hours):
    return int(round(hours * 3600))

# ============================== TIME PARSING FUNCTION ==============================

def parse_time(time_value):
    if pd.isna(time_value) or str(time_value).strip() == '':
        log_write(f"⏱️ Empty time value", "DEBUG")
        return None
    time_str = str(time_value).strip()
    log_write(f"⏱️ Parsing: '{time_str}'", "DEBUG")
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                result = int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
                log_write(f"  → Detected as hh:mm:ss = {result:.2f}h", "DEBUG")
                return result
            elif len(parts) == 2:
                result = int(parts[0]) + int(parts[1])/60
                log_write(f"  → Detected as hh:mm = {result:.2f}h", "DEBUG")
                return result
        if '.' in time_str:
            num_str = time_str.replace('.0', '')
            if num_str.isdigit():
                if len(num_str) == 4:
                    result = int(num_str[0:2]) + int(num_str[2:4])/60
                    log_write(f"  → Detected as 4-digit with dot = {result:.2f}h", "DEBUG")
                    return result
                elif len(num_str) == 3:
                    result = int(num_str[0:1]) + int(num_str[1:3])/60
                    log_write(f"  → Detected as 3-digit with dot = {result:.2f}h", "DEBUG")
                    return result
                elif len(num_str) <= 2:
                    result = float(num_str)
                    log_write(f"  → Detected as number with dot = {result:.2f}h", "DEBUG")
                    return result
        if time_str.isdigit():
            number = int(time_str)
            if len(time_str) == 6:
                result = int(time_str[0:2]) + int(time_str[2:4])/60 + int(time_str[4:6])/3600
                log_write(f"  → Detected as 6-digit = {result:.2f}h", "DEBUG")
                return result
            elif len(time_str) == 4:
                h = int(time_str[0:2])
                m = int(time_str[2:4])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → Detected as 4-digit = {result:.2f}h", "DEBUG")
                    return result
            elif len(time_str) == 3:
                h = int(time_str[0:1])
                m = int(time_str[1:3])
                if 0 <= h <= 24 and 0 <= m <= 59:
                    result = h + m/60
                    log_write(f"  → Detected as 3-digit = {result:.2f}h", "DEBUG")
                    return result
            elif len(time_str) <= 2:
                result = float(number)
                log_write(f"  → Detected as simple number = {result:.2f}h", "DEBUG")
                return result
        try:
            number = float(time_str)
            if 0 <= number <= 24:
                if number == int(number):
                    result = number
                    log_write(f"  → Detected as Excel integer = {result:.2f}h", "DEBUG")
                    return result
                else:
                    h = int(number)
                    m = int((number - h) * 60 + 0.5)
                    result = h + m/60
                    log_write(f"  → Detected as Excel decimal = {result:.2f}h", "DEBUG")
                    return result
        except:
            pass
    except Exception as e:
        log_write(f"  ❌ Error parsing: {e}", "ERROR")
    log_write(f"  ❌ Could not parse", "WARN")
    return None

# ============================== FILE FUNCTIONS ==============================

def find_file():
    log_write("-" * 60, "STEP")
    log_write("🔍 STEP 1: SEARCHING FOR FILE", "STEP")
    log_write("-" * 60, "STEP")
    files = []
    for pattern in FILE_PATTERNS:
        found = glob.glob(pattern)
        files.extend(found)
        log_write(f"  Pattern {pattern}: {len(found)} found", "FILE")
    if not files:
        set_error("No WorkingTimeTracker file found!")
        log_write("📁 Files in folder:", "INFO")
        for f in os.listdir('.'):
            if os.path.isfile(f):
                log_write(f"  - {f}", "INFO")
        return None
    if len(files) == 1:
        log_write(f"✅ Found: {files[0]}", "FILE")
        return files[0]
    log_write(f"📁 Multiple files found:", "FILE")
    for i, f in enumerate(files, 1):
        log_write(f"  {i}. {f}", "FILE")
    log_write(f"✅ Taking first file: {files[0]}", "FILE")
    return files[0]
def process_file(filepath):
    log_write("-" * 60, "STEP")
    log_write("📄 STEP 2: READING FILE", "STEP")
    log_write("-" * 60, "STEP")
    log_write(f"  File: {filepath}", "FILE")
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, header=None, encoding='utf-8')
            log_write("  ✅ CSV successfully read", "FILE")
        else:
            df = pd.read_excel(filepath, header=None)
            log_write("  ✅ Excel successfully read", "FILE")
    except Exception as e:
        set_error(f"Error reading file: {e}")
        return None
    log_write(f"  Rows: {len(df)}, Columns: {len(df.columns)}", "FILE")
    log_write("-" * 60, "STEP")
    log_write("👥 STEP 3: DETECTING EMPLOYEES", "STEP")
    log_write("-" * 60, "STEP")
    header = df.iloc[0].tolist()
    log_write(f"  Row 1 (raw data): {header}", "DEBUG")
    employees = []
    for i in range(0, len(header), 2):
        if i < len(header) and pd.notna(header[i]) and str(header[i]).strip():
            name = str(header[i]).strip()
            employees.append(name)
            log_write(f"  Column {i}-{i+1}: {name}", "EMPLOYEE")
    if not employees:
        set_error("No employees found in row 1!")
        return None
    log_write(f"✅ Employees: {', '.join(employees)}", "EMPLOYEE")
    data = df.iloc[1:].reset_index(drop=True)
    log_write(f"📊 Data rows: {len(data)}", "DATA")
    log_write("-" * 60, "STEP")
    log_write("🧮 STEP 4: CALCULATING HOURS", "STEP")
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
                log_write(f"  Day {row_idx+1}: {start} - {end}", "DEBUG")
                start_hours = parse_time(start)
                end_hours = parse_time(end)
                if start_hours is not None and end_hours is not None:
                    if end_hours < start_hours:
                        log_write(f"    → Night shift detected ({end_hours:.2f}h < {start_hours:.2f}h)", "DEBUG")
                        end_hours += 24
                    diff = round(end_hours - start_hours, 2)
                    log_write(f"    → Difference: {diff:.2f}h", "DEBUG")
                    if MIN_HOURS_PER_DAY < diff < MAX_HOURS_PER_DAY:
                        total += diff
                        days_worked += 1
                        daily_values.append(diff)
                        h, m, s = hours_to_hms(diff)
                        minutes = hours_to_minutes(diff)
                        seconds = hours_to_seconds(diff)
                        line = f"  Day {row_idx+1}: {start} - {end} = {h}h{m:02d}m{s:02d}s   {diff:.2f}h   {minutes}m   {seconds}s"
                        day_text += line + "\n"
                        log_write(f"  ✅ {line}", "CALC")
                    else:
                        day_text += f"  Day {row_idx+1}: {start} - {end} = ? (invalid: {diff:.2f}h)\n"
                        log_write(f"  ⚠️ Invalid difference: {diff:.2f}h", "WARN")
                else:
                    day_text += f"  Day {row_idx+1}: {start} - {end} = ? (unparseable)\n"
                    log_write(f"  ⚠️ Unparseable", "WARN")
        avg = round(total/days_worked, 2) if days_worked > 0 else 0
        h_avg, m_avg, s_avg = hours_to_hms(avg)
        min_avg = hours_to_minutes(avg)
        sec_avg = hours_to_seconds(avg)
        total_hms = format_hms(total)
        total_min = hours_to_minutes(total)
        total_sec = hours_to_seconds(total)
        summary_line = f"  📊 Total: {total_hms} in {days_worked} days ({h_avg}h{m_avg:02d}m{s_avg:02d}s/day) ({avg:.2f}h/day) ({min_avg}m/day) ({sec_avg}s/day)"
        day_text += summary_line + "\n"
        log_write(summary_line, "RESULT")
        log_write(f"    Total in minutes: {total_min}m, in seconds: {total_sec}s", "DEBUG")
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
    log_write("📁 STEP 5: CREATING ARCHIVE FOLDER", "STEP")
    log_write("-" * 60, "STEP")
    try:
        if not os.path.exists(ARCHIVE_FOLDER_NAME):
            os.makedirs(ARCHIVE_FOLDER_NAME)
            log_write(f"📁 Main archive created: {ARCHIVE_FOLDER_NAME}", "ARCHIVE")
        else:
            log_write(f"📁 Main archive exists: {ARCHIVE_FOLDER_NAME}", "ARCHIVE")
        sub_archive = os.path.join(ARCHIVE_FOLDER_NAME, LOG_TIMESTAMP)
        os.makedirs(sub_archive, exist_ok=True)
        log_write(f"📁 Subfolder created: {sub_archive}", "ARCHIVE")
        return sub_archive
    except Exception as e:
        set_error(f"Failed to create archive folder: {e}")
        return None
def save_results(results, details_text, original, archive_folder):
    log_write("-" * 60, "STEP")
    log_write("💾 STEP 6: SAVING RESULTS", "STEP")
    log_write("-" * 60, "STEP")
    try:
        result_file = f"{RESULT_FILE_PREFIX}.txt"
        result_path = os.path.join(archive_folder, result_file)
        log_write(f"  Creating: {result_path}", "SAVE")
        summary = "=" * 123 + "\n"
        summary += "=" * 49 + " 📊 WORKING HOURS - SUMMARY " + "=" * 50 + "\n"
        summary += "=" * 123 + "\n\n"
        summary += f"{'Employee':<30} {'Total (h/m/s)':>20} {'Total (h)':>12} {'Total (m)':>12} {'Total (s)':>12} {'Days':>8}\n"
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
        summary += f"{'ALL EMPLOYEES':<30} {total_all_hms:>20} {total_all:>12.2f} {total_all_min:>12} {total_all_sec:>12} {days_all:>8}\n"
        summary += "\n"
        details_header = "=" * 123 + "\n"
        details_header += "=" * 49 + " 📋 DETAILS BY EMPLOYEE " + "=" * 50 + "\n"
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
        completion += "=" * 52 + " Completed " + "=" * 53 + "\n"
        completion += "=" * 123 + "\n\n"
        footer = f"📁 Original file: {original}\n"
        footer += f"📅 Calculated on: {datetime.now().strftime(RESULT_DATE_FORMAT)}\n"
        footer += f"📋 Log file: {LOG_FILE}\n"
        footer += "\n" + "=" * 123 + "\n"
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write(details_header)
            f.write(processed_details)
            f.write(completion)
            f.write(footer)
        log_write(f"  ✅ Results saved: {result_file}", "SAVE")
        return result_path
    except Exception as e:
        set_error(f"Error saving results: {e}")
        return None
def copy_original(original, archive_folder):
    log_write("-" * 60, "STEP")
    log_write("📦 STEP 7: COPYING ORIGINAL FILE", "STEP")
    log_write("-" * 60, "STEP")
    try:
        time.sleep(1)
        target_path = os.path.join(archive_folder, os.path.basename(original))
        shutil.copy2(original, target_path)
        log_write(f"  ✅ Original copied: {os.path.basename(original)}", "ARCHIVE")
        log_write(f"    → Destination: {target_path}", "ARCHIVE")
        return True
    except Exception as e:
        log_write(f"  ⚠️ Copying failed: {e}", "WARN")
        log_write("  📌 Please check if file is open in Excel.", "HINT")
        return False

# ============================== MAIN PROGRAM ==============================

def main():
    global script_successful
    archive_folder = None
    try:
        log_write("=" * 100, "SYSTEM")
        log_write("🚀 WORKING TIME TRACKER STARTED", "SYSTEM")
        log_write(f"  Python Version: {sys.version}", "SYSTEM")
        log_write(f"  Timestamp: {LOG_TIMESTAMP}", "SYSTEM")
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
        log_write("✨ ALL STEPS COMPLETED SUCCESSFULLY", "SYSTEM")
        log_write(f"  📁 Archive folder: {archive_folder}", "SYSTEM")
        log_write(f"  📄 Result: {RESULT_FILE_PREFIX}.txt", "SYSTEM")
        log_write(f"  📋 Log: {LOG_FILE_PREFIX}.txt", "SYSTEM")
        log_write(f"  📦 Original: {os.path.basename(file)}", "SYSTEM")
        log_write("=" * 100, "SYSTEM")
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
        set_error(error_msg)
    finally:
        log_save(archive_folder)

# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    main()