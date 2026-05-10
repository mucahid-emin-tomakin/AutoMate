#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MediaTracker - NoComment

# ============================== IMPORTS ==============================

import os
import re
import shutil
import subprocess
import threading
import queue
from datetime import datetime

# ============================== IMPORTS ==============================
# ============================== CONFIGURATION ==============================

# Root directory where video files are located
root_folder = r"C:\Users\USER\Downloads"
# Paths – built dynamically from root_folder
output_file = os.path.join(root_folder, "NAME.txt")
error_log = os.path.join(root_folder, "error_log.txt")
backup_folder = os.path.join(root_folder, "backup")
# Video file extensions to include (case-insensitive check)
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]
# Number of parallel threads for ffprobe calls
NUM_THREADS = 8  # Alternative: import os; NUM_THREADS = os.cpu_count() or 4
# ffprobe executable (set to full path if not in system PATH)
FFPROBE_PATH = "ffprobe"
# Timeout in seconds for each ffprobe call
FFPROBE_TIMEOUT = 11
# Regex pattern to extract episode number from filename
NUMBER_PATTERN = r'\d+'
# Timestamp format for backup files
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ============================== CONFIGURATION ==============================
# ============================== GLOBAL ERROR COLLECTOR ==============================

# List to collect error messages during execution
error_messages = []

def log_error(msg):
    """Append an error message to the global error list."""
    error_messages.append(msg)

# ============================== GLOBAL ERROR COLLECTOR ==============================
# ============================== HELPER FUNCTIONS ==============================

def extract_number(filename):
    """
    Extract the first sequence of digits from a filename and return it as integer.
    If no digits are found, return 0. This is used for natural sorting of video files.
    """
    match = re.search(NUMBER_PATTERN, filename)
    return int(match.group()) if match else 0

def get_video_length(filepath):
    """
    Use ffprobe to retrieve the duration of a video file in seconds.
    Returns 0.0 in case of any error (including timeout).
    Errors are logged via log_error.
    """
    try:
        result = subprocess.run(
            [FFPROBE_PATH, "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=FFPROBE_TIMEOUT
        )
        length_sec = float(result.stdout.strip())
        return length_sec
    except subprocess.TimeoutExpired:
        log_error(f"Timeout bei ffprobe für Datei {filepath}")
        return 0.0
    except Exception as e:
        log_error(f"Fehler bei Datei {filepath}: {e}")
        return 0.0

# ============================== HELPER FUNCTIONS ==============================
# ============================== BACKUP EXISTING OUTPUT FILE ==============================

# If the output file already exists, create a timestamped backup copy
if os.path.exists(output_file):
    os.makedirs(backup_folder, exist_ok=True)   # Ensure backup folder exists
    timestamp = datetime.now().strftime(BACKUP_TIMESTAMP_FORMAT)
    backup_path = os.path.join(backup_folder, f"NAME_backup_{timestamp}.txt")
    shutil.copy2(output_file, backup_path)      # Preserve metadata

# ============================== BACKUP EXISTING OUTPUT FILE ==============================
# ============================== DISCOVER ALL VIDEO FILES ==============================

# List that will hold tuples: (relative_path, video_filename, full_path)
all_videos = []

# Walk through the root folder recursively
for dirpath, dirnames, filenames in os.walk(root_folder):
    # Consider only files with configured video extensions (case-insensitive)
    video_files = [
        f for f in filenames
        if any(f.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)
    ]
    if video_files:
        # Relative path from root_folder to current directory
        relative_path = os.path.relpath(dirpath, root_folder)
        # Sort video files naturally using the extracted number
        sorted_videos = sorted(video_files, key=extract_number)
        for video in sorted_videos:
            full_path = os.path.join(dirpath, video)
            all_videos.append((relative_path, video, full_path))

# ============================== DISCOVER ALL VIDEO FILES ==============================
# ============================== MULTITHREADING PREPARATION ==============================

# Queue to distribute video files among worker threads
video_queue = queue.Queue()
# Results list: each entry will be (relative_path, video, length_sec, size_bytes)
video_info_results = []

def worker():
    """
    Worker thread function.
    Fetches items from video_queue, retrieves video length and file size,
    and appends the information to video_info_results.
    Stops when a None sentinel is received.
    """
    while True:
        item = video_queue.get()
        try:
            if item is None:
                break       # Sentinel to stop the worker
            relative_path, video, full_path = item
            length = get_video_length(full_path)
            try:
                size_bytes = os.path.getsize(full_path)
            except Exception as e:
                log_error(f"Fehler beim Lesen der Dateigröße {full_path}: {e}")
                size_bytes = 0
            video_info_results.append((relative_path, video, length, size_bytes))
        finally:
            video_queue.task_done()

# ============================== MULTITHREADING PREPARATION ==============================
# ============================== START WORKER THREADS ==============================

num_threads = NUM_THREADS    # Number of parallel threads for ffprobe calls
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Put all discovered video entries into the queue
for v in all_videos:
    video_queue.put(v)

# Wait until all items have been processed
video_queue.join()

# Send one sentinel (None) per thread to stop them gracefully
for i in range(num_threads):
    video_queue.put(None)
for t in threads:
    t.join()

# ============================== START WORKER THREADS ==============================
# ============================== COMPUTE SUMMARY STATISTICS ==============================

series_set = set()          # Unique series names (first part of relative path)
total_size_bytes = 0
total_length_sec = 0

for staffel, video, length, size in video_info_results:
    # The series name is the top-level directory of the relative path
    series_name = staffel.split(os.sep)[0]
    series_set.add(series_name)
    total_size_bytes += size
    total_length_sec += length

total_episodes = len(video_info_results)
total_minutes = int(total_length_sec // 60)
total_hours = total_length_sec / 3600
total_days = total_hours / 24
total_size_gb = total_size_bytes / (1024**3)

# ============================== COMPUTE SUMMARY STATISTICS ==============================
# ============================== WRITE OUTPUT FILE ==============================

with open(output_file, "w", encoding="utf-8") as f:
    # Write general information header
    f.write("[Information]\n")
    f.write(f"Anime anzahl : {len(series_set)}\n")
    f.write(f"Gesamtanzahl der Folgen: {total_episodes}\n")
    f.write(f"Ungefähre Laufzeit: {total_minutes} Minuten -> {total_hours:.2f} Stunden -> {total_days:.2f} Tage\n")
    f.write(f"Gesamtgröße der Videos: {total_size_gb:.2f} GB\n\n")

    # Variables to track the current series and season (staffel) while writing the list
    current_series = None
    current_staffel = None

    # Sort video results by series, then relative path, then natural order of video filename
    video_info_results.sort(key=lambda x: (x[0].split(os.sep)[0], x[0], extract_number(x[1])))

    # Write series/season sections and video filenames
    for staffel, video, length, size in video_info_results:
        series_name = staffel.split(os.sep)[0]

        # When a new series starts, add a blank line (unless it's the very first)
        if series_name != current_series:
            if current_series is not None:
                f.write("\n")
            current_series = series_name
            current_staffel = None   # Reset season tracker for the new series

        # When a new season (subfolder) starts, write its section header
        if staffel != current_staffel:
            current_staffel = staffel
            f.write(f"[{staffel}]\n")

        # Write the video filename
        f.write(f"{video}\n")

# ============================== WRITE OUTPUT FILE ==============================
# ============================== WRITE ERROR LOG ==============================

# If any errors were collected, save them to the error log file
if error_messages:
    with open(error_log, "w", encoding="utf-8") as ef:
        for msg in error_messages:
            ef.write(msg + "\n")

# ============================== WRITE ERROR LOG ==============================
# ============================== COMPLETION MESSAGE ==============================

print("Skript erfolgreich beendet.")