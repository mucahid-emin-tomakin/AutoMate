# Working Time Tracker ⏱️

A simple tool to calculate working hours from Excel/CSV files.

## Features
- Reads Excel (.xlsx) and CSV files with pattern `Zaman*.xlsx` or `Zaman*.csv`
- Detects multiple employees (columns A-B, C-D, etc.)
- Recognizes various time formats
- Automatic night shift detection
- Creates detailed result files

## Usage
1. Place your `Zaman*.xlsx` file in the same folder
2. Run `WorkingTimeTracker.py`
3. Results are saved in `Archive/` folder

## Requirements
- Python 3.6+
- Auto-installs required packages on first run