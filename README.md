# Q-Lats OSA Data Converter

A Python script built with Pandas to parse Optical Spectrum Analyzer (OSA) text files and aggregate metadata (Date, Resolution Bandwidth) and trace measurements into a structured CSV dataset (`OSA_Combined_Data.csv`).

## Requirements
* Python 3.x
* `pandas`

## Usage
1. Place `.txt` OSA files in the directory alongside the script.
2. Run the converter:
   ```bash
   python Txt_To_CSV_Converter.py
