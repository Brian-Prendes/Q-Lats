import os
import glob
import pandas as pd

def process_osa_files_pandas():
    # Detect the script's exact folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_files = glob.glob(os.path.join(script_dir, '*.txt'))
    
    #In case nothing is there
    if not txt_files:
        print("No .txt files found.")
        return

    all_dataframes = []

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        metadata = {'Date': 'Unknown', 'Resolution_Bandwidth': 'Unknown'}
        data_start_line = 0
        
        # 1. Quickly scan the top of the file to grab metadata and find the data
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line.startswith('Date'):
                    metadata['Date'] = line.split(':', 1)[-1].strip()
                elif 'resolution bandwidth' in line.lower() or 'res bw' in line.lower():
                    metadata['Resolution_Bandwidth'] = line.split(':', 1)[-1].strip()
                
                # Stop looking once we hit the first number (the start of the data)
                if line and (line[0].isdigit() or line.startswith('-')):
                    data_start_line = i
                    break
        
        # 2. Let Pandas parse the massive block of numbers
        # sep=r'[,\s]+' tells Pandas to automatically handle commas OR spaces cleanly
        df = pd.read_csv(
            file_path, 
            skiprows=data_start_line, 
            sep=r'[,\s]+', 
            engine='python',
            names=['Wavelength', 'Measurement_Value'],
            usecols=[0, 1] # Ignore any accidental extra columns
        )
        
        # 3. Add our metadata as new columns (Pandas does this to the whole dataset instantly)
        df.insert(0, 'Filename', filename)
        df.insert(1, 'Date', metadata['Date'])
        df.insert(2, 'Resolution_Bandwidth', metadata['Resolution_Bandwidth'])
        
        all_dataframes.append(df)
        print(f"Processed: {filename} ({len(df)} rows)")

    # 4. Combine everything and export to CSV in one shot
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        output_csv = os.path.join(script_dir, 'OSA_Combined_Data.csv')
        combined_df.to_csv(output_csv, index=False)
        print(f"\nSuccess! Exported {len(combined_df)} total rows to: {output_csv}")

if __name__ == "__main__":
    process_osa_files_pandas()