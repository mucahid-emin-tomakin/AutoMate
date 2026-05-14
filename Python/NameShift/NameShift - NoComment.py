#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NameShift - NoComment

# ============================== IMPORTS ==============================

import os
import re

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

FOLDER_PATH = r"C:\Users\USER\Documents\Projekte"
LOG_FILE = r"C:\Users\USER\Downloads\folder_file_list.txt"
RENAME_LOG_FILE = r"C:\Users\USER\Downloads\rename_log.csv"
RENAME_FOLDERS = True
LOG_FOLDER_FILE_NAMES = True
RENAME_FILES = True
RENAME_FILE_EXTENSIONS = [".html"]
REMOVE_CHARS = ["(", ")"]
FILE_ENCODING = "utf-8"
CSV_SEPARATOR = ";"
DATE_INPUT_ORDER = ["day", "month", "year"]
DATE_OUTPUT_ORDER = ["year", "month", "day"]
DATE_SEPARATOR = "."
MIN_LENGTH_FOR_DATE = 18

# ============================== CONFIGURATION ==============================
# ============================== HELPER FUNCTIONS ==============================

def log_rename(old_name, new_name):
    with open(RENAME_LOG_FILE, "a", encoding=FILE_ENCODING) as f:
        f.write(f"{old_name}{CSV_SEPARATOR}{new_name}\n")

def reorder_date(date_part):
    parts = date_part.split(DATE_SEPARATOR)
    
    if len(parts) != 3:
        return date_part
    
    date_dict = {}
    for i, order in enumerate(DATE_INPUT_ORDER):
        date_dict[order] = parts[i]
    
    new_parts = [date_dict[order] for order in DATE_OUTPUT_ORDER]
    return DATE_SEPARATOR.join(new_parts)

def extract_parts(folder_name):
    parts = folder_name.split("-")
    
    if len(parts) >= 3:
        first_part = parts[0]
        date_part = parts[1]
        last_part = "-".join(parts[2:])
        return first_part, date_part, last_part
    elif len(parts) == 2:
        first_part = parts[0]
        date_part = parts[1]
        return first_part, date_part, None
    
    return folder_name, None, None

# ============================== FOLDER RENAME ==============================
# ============================== LOG FOLDER & FILE NAMES ==============================

def rename_folders():
    
    print("=" * 50)
    print(" STEP: RENAME FOLDERS")
    print("=" * 50)
    
    folder_names = [f for f in os.listdir(FOLDER_PATH) if os.path.isdir(os.path.join(FOLDER_PATH, f))]
    renamed_count = 0
    
    for folder_name in folder_names:
        full_path = os.path.join(FOLDER_PATH, folder_name)
        
        if len(folder_name) <= MIN_LENGTH_FOR_DATE:
            continue
        
        first_part, date_part, last_part = extract_parts(folder_name)
        
        if date_part is None:
            continue
        
        new_date_part = reorder_date(date_part)
        
        if last_part:
            new_name = f"{first_part}-{new_date_part}-{last_part}"
        else:
            new_name = f"{first_part}-{new_date_part}"
        
        if new_name != folder_name:
            new_path = os.path.join(FOLDER_PATH, new_name)
            
            try:
                os.rename(full_path, new_path)
                print(f"✓ Renamed: {folder_name}  →  {new_name}")
                log_rename(folder_name, new_name)
                renamed_count += 1
            except Exception as e:
                print(f"❌ Error renaming {folder_name}: {e}")
    
    print(f"\nFolders renamed: {renamed_count}\n")

# ============================== LOG FOLDER & FILE NAMES ==============================
# ============================== FILE RENAME ==============================

def log_folder_file_names():
    
    print("=" * 50)
    print(" STEP: LOG FOLDER & FILE NAMES")
    print("=" * 50)
    
    folder_count = 0
    file_count = 0
    
    with open(LOG_FILE, "w", encoding=FILE_ENCODING) as f:
        for root, dirs, files in os.walk(FOLDER_PATH):
            for dir_name in dirs:
                f.write(f"{dir_name}\n")
                folder_count += 1
            
            for file_name in files:
                f.write(f"{file_name}\n")
                file_count += 1
    
    print(f"✓ Folders logged: {folder_count}")
    print(f"✓ Files logged: {file_count}")
    print(f"✓ Log saved to: {LOG_FILE}\n")

# ============================== LOG FOLDER & FILE NAMES ==============================
# ============================== FILE RENAME ==============================

def rename_files():
    
    print("=" * 50)
    print(" STEP: RENAME FILES")
    print("=" * 50)
    
    renamed_count = 0
    counter = 0
    
    for root, dirs, files in os.walk(FOLDER_PATH):
        for file_name in files:
            file_ext = os.path.splitext(file_name)[1].lower()
            
            if file_ext not in [ext.lower() for ext in RENAME_FILE_EXTENSIONS]:
                continue
            
            if not any(char in file_name for char in REMOVE_CHARS):
                continue
            
            new_name = file_name
            for char in REMOVE_CHARS:
                new_name = new_name.replace(char, "")
            
            if new_name != file_name:
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_name)
                
                if os.path.exists(new_path):
                    counter += 1
                    name_part, ext_part = os.path.splitext(new_name)
                    new_name = f"{name_part} {counter}{ext_part}"
                    new_path = os.path.join(root, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✓ Renamed: {file_name}  →  {new_name}")
                    log_rename(file_name, new_name)
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming {file_name}: {e}")
    
    print(f"\nFiles renamed: {renamed_count}\n")

# ============================== FILE RENAME ==============================
# ============================== MAIN ==============================

def main():
    
    print("\n" + "=" * 50)
    print(" FOLDER & FILE MANAGER")
    print("=" * 50)
    print(f"Target path: {FOLDER_PATH}")
    print(f"Rename folders: {RENAME_FOLDERS}")
    print(f"Log names: {LOG_FOLDER_FILE_NAMES}")
    print(f"Rename files: {RENAME_FILES}")
    print("=" * 50 + "\n")
    
    if RENAME_FOLDERS:
        rename_folders()
    
    if LOG_FOLDER_FILE_NAMES:
        log_folder_file_names()
    
    if RENAME_FILES:
        rename_files()
    
    print("=" * 50)
    print(" ALL STEPS COMPLETED")
    print("=" * 50)

# ============================== MAIN ==============================
# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    main()
