#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CopySync

# ============================== IMPORTS ==============================

import os
import sys
import csv
import shutil
import hashlib
import time
from pathlib import Path

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

# Source drive to back up
SOURCE_DRIVE = r"F:\\"
# Target drive where backup will be stored
TARGET_DRIVE = r"E:\\"
# CSV file logging all issues found during comparison
CHECK_CSV = "CheckComplete.csv"
# Log file for detailed execution trace
LOG_FILE = "BackupAutomationLog.txt"
# Human-readable summary report
SUMMARY_FILE = "Backup_Summary.txt"
# List of items still missing after final check
REMAINING_ISSUES_FILE = "remaining_issues.txt"

# Enable SHA-256 hash comparison for detecting content differences (slow but thorough)
USE_HASH_COMPARISON = False
# Files and folders to skip during scanning
EXCLUDE_ITEMS = [
    '$RECYCLE.BIN',
    'System Volume Information',
    '.Trash',
    '.Trashes',
    'Thumbs.db',
    'desktop.ini'
]

# Buffer size in bytes for reading files during hash calculation
HASH_BUFFER_SIZE = 65536
# Print progress every N scanned items during comparison
PROGRESS_INTERVAL_SCAN = 1000
# Print progress every N copied files
PROGRESS_INTERVAL_COPY = 10
# Maximum number of missing items shown in console output
MAX_DISPLAY_MISSING = 20
# Timestamp format for renaming old log files
LOG_BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
# Width of major separator lines in reports
SUMMARY_LINE_WIDTH = 70
# Width of minor separator lines in reports
SUB_LINE_WIDTH = 40
# Character encoding for all output files
FILE_ENCODING = "utf-8"

# ============================== CONFIGURATION ==============================
# ============================== HELPER FUNCTIONS ==============================

def log_message(message, print_also=True):
    """Write a timestamped message to the log file and optionally print it to console."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, 'a', encoding=FILE_ENCODING) as log:
        log.write(log_entry + "\n")
    
    if print_also:
        print(message)

def get_file_hash(file_path, buffer_size=HASH_BUFFER_SIZE):
    """Calculate the SHA-256 hash of a file. Returns None on error."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception:
        return None

def print_header(title):
    """Print a formatted header with the given title."""
    print("\n" + "="*SUMMARY_LINE_WIDTH)
    print(f" {title}")
    print("="*SUMMARY_LINE_WIDTH)

# ============================== HELPER FUNCTIONS ==============================
# ============================== STEP 1: PERFORM COMPLETE COMPARISON ==============================

def perform_complete_comparison():
    """Compare all files and folders between source and target. Return a list of missing or mismatched items."""
    
    print_header("STEP 1: COMPARE ALL FILES AND FOLDERS")
    log_message("START: Complete comparison")
    
    # Convert drive paths to Path objects for easier manipulation
    source_path = Path(SOURCE_DRIVE)
    target_path = Path(TARGET_DRIVE)
    
    # Validate that source path exists
    if not source_path.exists():
        log_message(f"❌ ERROR: Source path does not exist: {SOURCE_DRIVE}")
        return []
    
    # Validate that target path exists
    if not target_path.exists():
        log_message(f"❌ ERROR: Target path does not exist: {TARGET_DRIVE}")
        return []
    
    # List to collect all missing or faulty items
    missing_items = []
    total_scanned = 0
    start_time = time.time()
    
    log_message(f"Source: {SOURCE_DRIVE}")
    log_message(f"Target: {TARGET_DRIVE}")
    log_message(f"Hash comparison: {'YES' if USE_HASH_COMPARISON else 'NO'}")
    
    print(f"Scanning source directory...")
    
    # Walk through the entire source directory tree
    for root, dirs, files in os.walk(SOURCE_DRIVE):
        # Exclude unwanted directories from traversal (modifies dirs in-place)
        dirs[:] = [d for d in dirs if d not in EXCLUDE_ITEMS]
        
        current_path = Path(root)
        # Get the path relative to the source root
        relative_path = current_path.relative_to(source_path)
        
        # --- Check directories ---
        for dir_name in dirs:
            if dir_name in EXCLUDE_ITEMS:
                continue
                
            source_dir = source_path / relative_path / dir_name
            target_dir = target_path / relative_path / dir_name
            
            # Directory does not exist on target
            if not target_dir.exists():
                missing_items.append({
                    'type': 'directory',
                    'path': str(relative_path / dir_name),
                    'source_path': str(source_dir),
                    'target_path': str(target_dir),
                    'reason': 'Directory missing'
                })
            
            total_scanned += 1
        
        # --- Check files ---
        for file_name in files:
            if file_name in EXCLUDE_ITEMS:
                continue
            
            source_file = source_path / relative_path / file_name
            target_file = target_path / relative_path / file_name
            
            # File does not exist on target
            if not target_file.exists():
                missing_items.append({
                    'type': 'file',
                    'path': str(relative_path / file_name),
                    'source_path': str(source_file),
                    'target_path': str(target_file),
                    'reason': 'File missing',
                    'size': os.path.getsize(source_file) if source_file.exists() else 0
                })
                total_scanned += 1
                continue
            
            # File exists on both sides - compare size and optionally hash
            try:
                source_size = os.path.getsize(source_file)
                target_size = os.path.getsize(target_file)
                
                # Size mismatch detected
                if source_size != target_size:
                    missing_items.append({
                        'type': 'file',
                        'path': str(relative_path / file_name),
                        'source_path': str(source_file),
                        'target_path': str(target_file),
                        'reason': f'Size mismatch ({source_size} vs {target_size} bytes)',
                        'size': source_size
                    })
                
                # Sizes match, but hash comparison is enabled - check content
                elif USE_HASH_COMPARISON:
                    source_hash = get_file_hash(source_file)
                    target_hash = get_file_hash(target_file)
                    
                    # Content mismatch detected via hash
                    if source_hash and target_hash and source_hash != target_hash:
                        missing_items.append({
                            'type': 'file',
                            'path': str(relative_path / file_name),
                            'source_path': str(source_file),
                            'target_path': str(target_file),
                            'reason': 'Content mismatch (hash)',
                            'size': source_size
                        })
            
            except Exception as e:
                # Catch any unexpected errors during comparison (e.g. permission denied)
                missing_items.append({
                    'type': 'file',
                    'path': str(relative_path / file_name),
                    'source_path': str(source_file),
                    'target_path': str(target_file),
                    'reason': f'Error during comparison: {str(e)}',
                    'size': 0
                })
            
            total_scanned += 1
            
            # Show progress at configured intervals
            if total_scanned % PROGRESS_INTERVAL_SCAN == 0:
                elapsed = time.time() - start_time
                elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
                print(f"\rScanned: {total_scanned} | Missing: {len(missing_items)} | Time: {elapsed_str}", end="")
    
    # Display final comparison results
    elapsed = time.time() - start_time
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print(f"\r{' '*80}")
    print(f"\nComparison complete!")
    print(f"Elements scanned: {total_scanned}")
    print(f"Missing/faulty elements: {len(missing_items)}")
    print(f"Time elapsed: {elapsed_str}")
    
    log_message(f"Comparison complete: {total_scanned} elements scanned, {len(missing_items)} problems found")
    
    return missing_items

# ============================== STEP 1: PERFORM COMPLETE COMPARISON ==============================
# ============================== STEP 2: COPY MISSING ITEMS ==============================

def copy_missing_items(missing_items):
    """Copy all missing files and create all missing directories. Return True if no errors occurred."""
    
    # Nothing to copy - already in sync
    if not missing_items:
        print("\n✓ No missing elements found - nothing to copy.")
        log_message("No missing elements - copy step skipped")
        return True
    
    print_header("STEP 2: COPY MISSING ELEMENTS")
    log_message(f"START: Copy {len(missing_items)} missing elements")
    
    # Statistics dictionary to track progress
    stats = {
        'directories_created': 0,
        'files_copied': 0,
        'files_skipped': 0,
        'total_bytes': 0,
        'errors': 0,
        'start_time': time.time()
    }
    
    # --- Phase 1: Create all missing directories first ---
    print("Creating missing directories...")
    directories = [item for item in missing_items if item['type'] == 'directory']
    
    for i, item in enumerate(directories, 1):
        try:
            target_dir = Path(item['target_path'])
            # Create the directory including any missing parent directories
            target_dir.mkdir(parents=True, exist_ok=True)
            stats['directories_created'] += 1
            
            print(f"\rDirectories: {i}/{len(directories)}", end="")
            log_message(f"Directory created: {item['path']}")
        
        except Exception as e:
            stats['errors'] += 1
            log_message(f"❌ Error creating {item['path']}: {str(e)}")
    
    if directories:
        print()  # New line after directory progress
    
    # --- Phase 2: Copy all missing files ---
    files = [item for item in missing_items if item['type'] == 'file']
    
    if files:
        print(f"Copying {len(files)} missing files...")
        
        for i, item in enumerate(files, 1):
            try:
                source_file = Path(item['source_path'])
                target_file = Path(item['target_path'])
                
                # Skip if source file no longer exists
                if not source_file.exists():
                    log_message(f"⚠️ Source does not exist: {item['path']}")
                    stats['files_skipped'] += 1
                    continue
                
                # Ensure the target parent directory exists
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file with metadata preservation
                file_size = os.path.getsize(source_file)
                shutil.copy2(source_file, target_file)
                
                stats['files_copied'] += 1
                stats['total_bytes'] += file_size
                
                # Show progress at configured intervals or on last file
                if i % PROGRESS_INTERVAL_COPY == 0 or i == len(files):
                    elapsed = time.time() - stats['start_time']
                    percent = (i / len(files)) * 100
                    # Calculate current transfer speed in MB/s
                    speed = stats['total_bytes'] / elapsed / 1024 / 1024 if elapsed > 0 else 0
                    
                    print(f"\rFiles: {i}/{len(files)} ({percent:.1f}%) | "
                          f"{stats['total_bytes']/1024**3:.2f} GB | "
                          f"{speed:.1f} MB/s", end="")
                
                log_message(f"File copied: {item['path']} ({file_size} bytes)")
            
            except Exception as e:
                stats['errors'] += 1
                log_message(f"❌ Error copying {item['path']}: {str(e)}")
        
        print()  # New line after file progress
    
    # Display copy statistics
    elapsed = time.time() - stats['start_time']
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print_header("COPY STATISTICS")
    print(f"Time elapsed:            {elapsed_str}")
    print(f"Directories created:     {stats['directories_created']}")
    print(f"Files copied:            {stats['files_copied']}")
    print(f"Files skipped:           {stats['files_skipped']}")
    print(f"Total data copied:       {stats['total_bytes']/1024**3:.2f} GB")
    
    # Calculate and display average transfer speed
    if elapsed > 0 and stats['files_copied'] > 0:
        avg_speed = stats['total_bytes'] / elapsed / 1024 / 1024
        print(f"Average speed:           {avg_speed:.1f} MB/s")
    
    print(f"Errors:                  {stats['errors']}")
    
    log_message(f"Copy complete: {stats['files_copied']} files, "
                f"{stats['directories_created']} directories, "
                f"{stats['errors']} errors")
    
    # Return True only if no errors occurred
    return stats['errors'] == 0

# ============================== STEP 2: COPY MISSING ITEMS ==============================
# ============================== STEP 3: FINAL CHECK ==============================

def perform_final_check():
    """Perform a final comparison to verify everything was copied correctly. Return True if consistent."""
    
    print_header("STEP 3: FINAL COMPLETE CHECK")
    log_message("START: Final complete check")
    
    source_path = Path(SOURCE_DRIVE)
    target_path = Path(TARGET_DRIVE)
    
    # Collect any issues still present after copying
    remaining_issues = []
    checked_items = 0
    start_time = time.time()
    
    print("Checking if all elements are present...")
    
    # Walk through source again to verify everything exists on target
    for root, dirs, files in os.walk(SOURCE_DRIVE):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_ITEMS]
        
        current_path = Path(root)
        relative_path = current_path.relative_to(source_path)
        
        # Check directories
        for dir_name in dirs:
            if dir_name in EXCLUDE_ITEMS:
                continue
                
            target_dir = target_path / relative_path / dir_name
            if not target_dir.exists():
                remaining_issues.append(f"Directory missing: {relative_path / dir_name}")
            
            checked_items += 1
        
        # Check files
        for file_name in files:
            if file_name in EXCLUDE_ITEMS:
                continue
            
            target_file = target_path / relative_path / file_name
            if not target_file.exists():
                remaining_issues.append(f"File missing: {relative_path / file_name}")
            
            checked_items += 1
            
            # Show progress at configured intervals
            if checked_items % PROGRESS_INTERVAL_SCAN == 0:
                elapsed = time.time() - start_time
                print(f"\rChecked: {checked_items} | Still missing: {len(remaining_issues)}", end="")
    
    elapsed = time.time() - start_time
    elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    
    print(f"\r{' '*80}")
    
    # --- Success case: no remaining issues ---
    if not remaining_issues:
        print(f"\n✅ CONGRATULATIONS!")
        print(f"✅ All {checked_items} elements were successfully copied!")
        print(f"✅ Backup is complete and consistent!")
        print(f"✅ Check time: {elapsed_str}")
        
        log_message(f"✅ FINAL CHECK PASSED: All {checked_items} elements present")
        return True
    
    # --- Failure case: some items still missing ---
    else:
        print(f"\n⚠️  WARNING: {len(remaining_issues)} elements still missing!")
        print(f"⚠️  Elements checked: {checked_items}")
        print(f"⚠️  Check time: {elapsed_str}")
        
        print("\nMissing elements:")
        # Show only the first N missing items to avoid console flood
        for issue in remaining_issues[:MAX_DISPLAY_MISSING]:
            print(f"  • {issue}")
        
        if len(remaining_issues) > MAX_DISPLAY_MISSING:
            print(f"  ... and {len(remaining_issues) - MAX_DISPLAY_MISSING} more")
        
        log_message(f"⚠️  FINAL CHECK FAILED: {len(remaining_issues)} elements missing")
        
        # Save the complete list of missing elements to a file
        with open(REMAINING_ISSUES_FILE, 'w', encoding=FILE_ENCODING) as f:
            f.write(f"Missing elements after backup - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            for issue in remaining_issues:
                f.write(f"{issue}\n")
        
        print(f"\nℹ️  List of missing elements saved to: {REMAINING_ISSUES_FILE}")
        
        return False

# ============================== STEP 3: FINAL CHECK ==============================
# ============================== STEP 4: SAVE RESULTS AND CREATE REPORT ==============================

def save_results_and_report(missing_items, success):
    """Save detailed CSV results and create a human-readable summary report."""
    
    print_header("STEP 4: CREATE REPORT")
    
    # Write detailed CSV with all found problems (if any)
    if missing_items:
        with open(CHECK_CSV, 'w', newline='', encoding=FILE_ENCODING) as csvfile:
            fieldnames = ['type', 'path', 'reason', 'size', 'source_path', 'target_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(missing_items)
        
        print(f"✓ Detailed list saved as: {CHECK_CSV}")
    
    summary_file = SUMMARY_FILE
    
    # Write the human-readable summary report
    with open(summary_file, 'w', encoding=FILE_ENCODING) as f:
        f.write("="*SUMMARY_LINE_WIDTH + "\n")
        f.write("BACKUP AUTOMATION - SUMMARY\n")
        f.write("="*SUMMARY_LINE_WIDTH + "\n\n")
        
        f.write(f"Timestamp:               {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source:                  {SOURCE_DRIVE}\n")
        f.write(f"Target:                  {TARGET_DRIVE}\n")
        f.write(f"Hash comparison:         {'YES' if USE_HASH_COMPARISON else 'NO'}\n\n")
        
        f.write("RESULTS:\n")
        f.write("-"*SUB_LINE_WIDTH + "\n")
        
        if not missing_items:
            f.write("✅ No problems found - backup was already complete!\n")
        else:
            # Count by type for the summary
            dirs_count = sum(1 for item in missing_items if item['type'] == 'directory')
            files_count = sum(1 for item in missing_items if item['type'] == 'file')
            
            f.write(f"Problems found:           {len(missing_items)}\n")
            f.write(f"  • Missing directories:  {dirs_count}\n")
            f.write(f"  • Missing/faulty files: {files_count}\n\n")
            
            if success:
                f.write("✅ All missing elements were successfully copied!\n")
                f.write("✅ Final check passed!\n")
            else:
                f.write("⚠️  Some elements could not be copied.\n")
                f.write("⚠️  Please check the log file for details.\n")
        
        f.write("\nFILES:\n")
        f.write("-"*SUB_LINE_WIDTH + "\n")
        f.write(f"Detailed CSV list:        {CHECK_CSV}\n")
        f.write(f"Log file:                 {LOG_FILE}\n")
        f.write(f"Summary:                  {summary_file}\n")
        
        # Mention the remaining issues file if it exists
        if os.path.exists(REMAINING_ISSUES_FILE):
            f.write(f"Missing elements:         {REMAINING_ISSUES_FILE}\n")
    
    print(f"✓ Summary saved as: {summary_file}")
    print(f"✓ Log file: {LOG_FILE}")

# ============================== STEP 4: SAVE RESULTS AND CREATE REPORT ==============================
# ============================== MAIN FUNCTION - PROCESS CONTROL ==============================

def main():
    """Main function that controls the entire backup automation workflow."""
    
    # Initialize log file - rename old log if it exists
    if os.path.exists(LOG_FILE):
        old_log = f"{LOG_FILE}.{time.strftime(LOG_BACKUP_TIMESTAMP_FORMAT)}.bak"
        os.rename(LOG_FILE, old_log)
        log_message(f"Old log file renamed to: {old_log}", print_also=False)
    
    # Display startup banner
    print_header("BACKUP AUTOMATION STARTING")
    print(f"Source:      {SOURCE_DRIVE}")
    print(f"Target:      {TARGET_DRIVE}")
    print(f"Hash check:  {'Enabled' if USE_HASH_COMPARISON else 'Disabled'}")
    print(f"Log file:    {LOG_FILE}")
    print("="*SUMMARY_LINE_WIDTH)
    
    total_start_time = time.time()
    
    try:
        # Step 1: Scan and compare source vs target
        missing_items = perform_complete_comparison()
        
        if not missing_items:
            # Already fully synchronized
            print("\n" + "✅" * 35)
            print("✅ EVERYTHING ALREADY COMPLETE - NOTHING TO DO!")
            print("✅" * 35)
            
            success = True
        else:
            # Step 2: Copy all missing elements
            copy_success = copy_missing_items(missing_items)
            # Step 3: Verify the copy was successful
            final_check_success = perform_final_check()
            # Overall success requires both copy and check to succeed
            success = copy_success and final_check_success
        
        # Step 4: Generate reports
        save_results_and_report(missing_items, success)
        
    except KeyboardInterrupt:
        # Handle user abort gracefully
        log_message("❌ ABORTED by user (Ctrl+C)")
        print("\n\n❌ Process was aborted by user!")
        success = False
    
    except Exception as e:
        # Catch any unexpected errors to prevent crash
        log_message(f"❌ UNKNOWN ERROR: {str(e)}")
        print(f"\n\n❌ An unexpected error occurred: {e}")
        success = False
    
    # Display final summary
    total_time = time.time() - total_start_time
    total_time_str = time.strftime('%H:%M:%S', time.gmtime(total_time))
    
    print_header("OVERALL SUMMARY")
    print(f"Total time:        {total_time_str}")
    print(f"Success:           {'✅ YES' if success else '❌ NO'}")
    print(f"Log file:          {LOG_FILE}")
    
    if success:
        print("\n" + "🎉" * 35)
        print("🎉 BACKUP AUTOMATION COMPLETED SUCCESSFULLY!")
        print("🎉" * 35)
    else:
        print("\n" + "⚠️ " * 18)
        print("⚠️  BACKUP AUTOMATION COMPLETED WITH ISSUES")
        print("⚠️ " * 18)
        print("\nPlease check the log file for details!")
    
    # Wait for user input before closing (useful when run via double-click)
    input("\nPress Enter to exit...")

# ============================== MAIN FUNCTION - PROCESS CONTROL ==============================
# ============================== PROGRAM START ==============================

# Entry point: run main() when script is executed directly
if __name__ == "__main__":
    main()
