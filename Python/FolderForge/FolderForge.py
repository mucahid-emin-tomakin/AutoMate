#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FolderForge

# ============================== IMPORTS ==============================

import os

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

FOLDER_PATH = r"C:\Users\USER\Documents\Projekte"
FOLDER_NAMES = "Kalender;Meine Buchungen;Nachhaltigkeit in der Lehre;KI in der Lehre;Tipps und Tricks zur Mathematik;Online-Bibliothek;Forschungsorientierte Lehre;Wissenschaftliches Arbeiten;Digitale Lernkarten;Auslandsprogramm"
FILE_ENCODING = "utf-8"

# ============================== CONFIGURATION ==============================
# ============================== MAIN LOGIC ==============================

def main():
    
    folder_list = [name.strip() for name in FOLDER_NAMES.split(";") if name.strip()]
    
    created_count = 0
    existing_count = 0
    error_count = 0
    
    print(f"Target path: {FOLDER_PATH}")
    print(f"Folders to create: {len(folder_list)}")
    print("-" * 40)
    
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
