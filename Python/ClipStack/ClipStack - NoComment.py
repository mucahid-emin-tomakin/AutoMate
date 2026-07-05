#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ClipStack - NoComment.py

# ============================== IMPORTS ==============================

import os
import subprocess
import json
import shutil
from pathlib import Path
import sys

# ============================== HELPER FUNCTIONS ==============================

def check_ffmpeg():
    if shutil.which('ffmpeg') is None:
        print("Error: ffmpeg not found. Please install ffmpeg and add it to your PATH.")
        sys.exit(1)
    if shutil.which('ffprobe') is None:
        print("Error: ffprobe not found. Please install ffmpeg (includes ffprobe).")
        sys.exit(1)

def get_video_info(file_path):
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-show_format',
        str(file_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        duration = float(data.get('format', {}).get('duration', 0))
        if duration == 0:
            for stream in data.get('streams', []):
                if stream.get('duration'):
                    duration = max(duration, float(stream['duration']))

        width = 0
        height = 0
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                width = int(stream.get('width', 0))
                height = int(stream.get('height', 0))
                break

        if width == 0 or height == 0 or duration == 0:
            raise ValueError(f"No valid video data found for {file_path}")

        return width, height, duration

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)

def copy_video_directly(input_path, output_path):
    shutil.copy2(input_path, output_path)

# ============================== CORE FUNCTIONS ==============================

def resize_video_with_padding(input_path, output_path, target_width, target_height):
    print(f"  Scaling + padding: {input_path.name}")
    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_path),
        '-vf', f'scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        str(output_path)
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_path.name}:")
        print(e.stderr.decode())
        sys.exit(1)

# ============================== MAIN EXECUTION ==============================

def main():
    script_dir = Path(__file__).parent.resolve()
    print(f"Working directory: {script_dir}")

    check_ffmpeg()

    video_files = sorted(script_dir.glob('*.mp4'))
    if not video_files:
        print("No .mp4 files found in the directory.")
        sys.exit(1)

    print(f"Analyzing {len(video_files)} video files...")
    infos = []
    for v in video_files:
        w, h, d = get_video_info(v)
        infos.append({'path': v, 'width': w, 'height': h, 'duration': d})
        print(f"  {v.name}: {w}x{h}, {d:.2f}s")

    max_width = max(info['width'] for info in infos)
    max_height = max(info['height'] for info in infos)
    print(f"Target resolution (largest): {max_width}x{max_height}")

    temp_dir = script_dir / 'temp_scaled'
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    print("Preparing videos...")
    scaled_files = []
    for idx, info in enumerate(infos):
        out_path = temp_dir / f'scaled_{idx:03d}.mp4'
        if info['width'] == max_width and info['height'] == max_height:
            print(f"  Copying (unchanged): {info['path'].name}")
            copy_video_directly(info['path'], out_path)
        else:
            resize_video_with_padding(info['path'], out_path, max_width, max_height)
        scaled_files.append(out_path)

    concat_list_path = temp_dir / 'concat_list.txt'
    with open(concat_list_path, 'w', encoding='utf-8') as f:
        for sf in scaled_files:
            f.write(f"file '{sf.as_posix()}'\n")

    chapters = []
    cumulative_time = 0.0
    for info in infos:
        start = cumulative_time
        end = cumulative_time + info['duration']
        chapters.append({
            'start': start,
            'end': end,
            'title': info['path'].stem
        })
        cumulative_time = end

    metadata_path = temp_dir / 'chapters.txt'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(";FFMETADATA1\n")
        f.write("title=Mathematik Grundlagen Komplett\n")
        for ch in chapters:
            f.write("[CHAPTER]\n")
            f.write("TIMEBASE=1/1\n")
            f.write(f"START={ch['start']:.6f}\n")
            f.write(f"END={ch['end']:.6f}\n")
            f.write(f"title={ch['title']}\n")

    output_path = script_dir / 'Gesamtvideo_mit_Kapiteln.mp4'
    print(f"Merging into: {output_path.name}")
    cmd_concat = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_list_path),
        '-i', str(metadata_path),
        '-map_metadata', '1',
        '-c', 'copy',
        str(output_path)
    ]
    try:
        subprocess.run(cmd_concat, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("Error during concatenation:")
        print(e.stderr.decode())
        sys.exit(1)

    shutil.rmtree(temp_dir)

    print(f"✅ Done! Video created: {output_path}")
    print(f"   Contains {len(chapters)} chapters for easy navigation.")

# ============================== PROGRAM START ==============================

if __name__ == "__main__":
    main()