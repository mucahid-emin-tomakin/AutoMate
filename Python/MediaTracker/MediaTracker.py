#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MediaTracker.py

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

root_folder = r"C:\Users\USER\Downloads"
output_file = os.path.join(root_folder, "NAME.txt")
error_log = os.path.join(root_folder, "error_log.txt")
backup_folder = os.path.join(root_folder, "backup")
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]
NUM_THREADS = 8
FFPROBE_PATH = "ffprobe"
FFPROBE_TIMEOUT = 11
NUMBER_PATTERN = r'\d+'
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ============================== CONFIGURATION ==============================
# ============================== GLOBAL ERROR COLLECTOR ==============================

error_messages = []

def log_error(msg):
    error_messages.append(msg)

# ============================== GLOBAL ERROR COLLECTOR ==============================
# ============================== HELPER FUNCTIONS ==============================

def extract_number(filename):
    match = re.search(NUMBER_PATTERN, filename)
    return int(match.group()) if match else 0

def get_video_length(filepath):
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

if os.path.exists(output_file):
    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime(BACKUP_TIMESTAMP_FORMAT)
    backup_path = os.path.join(backup_folder, f"NAME_backup_{timestamp}.txt")
    shutil.copy2(output_file, backup_path)

# ============================== BACKUP EXISTING OUTPUT FILE ==============================
# ============================== DISCOVER ALL VIDEO FILES ==============================

all_videos = []

for dirpath, dirnames, filenames in os.walk(root_folder):
    video_files = [
        f for f in filenames
        if any(f.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)
    ]
    if video_files:
        relative_path = os.path.relpath(dirpath, root_folder)
        sorted_videos = sorted(video_files, key=extract_number)
        for video in sorted_videos:
            full_path = os.path.join(dirpath, video)
            all_videos.append((relative_path, video, full_path))

# ============================== DISCOVER ALL VIDEO FILES ==============================
# ============================== MULTITHREADING PREPARATION ==============================

video_queue = queue.Queue()
video_info_results = []

def worker():
    while True:
        item = video_queue.get()
        try:
            if item is None:
                break
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

num_threads = NUM_THREADS
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for v in all_videos:
    video_queue.put(v)

video_queue.join()

for i in range(num_threads):
    video_queue.put(None)
for t in threads:
    t.join()

# ============================== START WORKER THREADS ==============================
# ============================== COMPUTE SUMMARY STATISTICS ==============================

series_set = set()
total_size_bytes = 0
total_length_sec = 0

for staffel, video, length, size in video_info_results:
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
    f.write("[Information]\n")
    f.write(f"Anime anzahl : {len(series_set)}\n")
    f.write(f"Gesamtanzahl der Folgen: {total_episodes}\n")
    f.write(f"Ungefähre Laufzeit: {total_minutes} Minuten -> {total_hours:.2f} Stunden -> {total_days:.2f} Tage\n")
    f.write(f"Gesamtgröße der Videos: {total_size_gb:.2f} GB\n\n")

    current_series = None
    current_staffel = None

    video_info_results.sort(key=lambda x: (x[0].split(os.sep)[0], x[0], extract_number(x[1])))

    for staffel, video, length, size in video_info_results:
        series_name = staffel.split(os.sep)[0]

        if series_name != current_series:
            if current_series is not None:
                f.write("\n")
            current_series = series_name
            current_staffel = None

        if staffel != current_staffel:
            current_staffel = staffel
            f.write(f"[{staffel}]\n")

        f.write(f"{video}\n")

# ============================== WRITE OUTPUT FILE ==============================
# ============================== WRITE ERROR LOG ==============================

if error_messages:
    with open(error_log, "w", encoding="utf-8") as ef:
        for msg in error_messages:
            ef.write(msg + "\n")

# ============================== WRITE ERROR LOG ==============================
# ============================== COMPLETION MESSAGE ==============================

print("Skript erfolgreich beendet.")
