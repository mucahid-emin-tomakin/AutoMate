#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FolderForge - NoComment

# ============================== IMPORTS ==============================

import os

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

# Target path where folders should be created
FOLDER_PATH = r"C:\Users\USER\Documents\Projekte"
# Semicolon-separated list of folder names to create
FOLDER_NAMES = "Kalender;Meine Buchungen;Nachhaltigkeit in der Lehre;KI in der Lehre;Tipps und Tricks zur Mathematik;Online-Bibliothek;Forschungsorientierte Lehre;Wissenschaftliches Arbeiten;Digitale Lernkarten;Auslandsprogramm"
# Encoding for output messages
FILE_ENCODING = "utf-8"

# ============================== CONFIGURATION ==============================
# ============================== MAIN LOGIC ==============================

def main():
    
    # Split the semicolon-separated string into a list and clean each name
    folder_list = [name.strip() for name in FOLDER_NAMES.split(";") if name.strip()]
    
    created_count = 0
    existing_count = 0
    error_count = 0
    
    print(f"Target path: {FOLDER_PATH}")
    print(f"Folders to create: {len(folder_list)}")
    print("-" * 40)
    
    # Create each folder if it does not already exist
    for folder_name in folder_list:
        full_path = os.path.join(FOLDER_PATH, folder_name)
        
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
                print(f"✓ Created: {folder_name}")
                created_count += 1
            except Exception as e:
                print(f"❌ Error: {folder_name} → {e}")
                error_count += 1
        else:
            print(f"→ Already exists: {folder_name}")
            existing_count += 1
    
    print("-" * 40)
    print(f"Created: {created_count} | Already existed: {existing_count} | Errors: {error_count}")
    print("Done.")

# ============================== MAIN LOGIC ==============================
# ============================== MAIN PROGRAM ==============================

if __name__ == "__main__":
    main()
