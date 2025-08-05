import csv
import os
from datetime import datetime

def truncate_text(text, max_length=20):
    """Truncate text to max_length characters and add '...' if longer."""
    if not text:
        return text
    # Convert to string and strip whitespace
    text_str = str(text).strip()
    if len(text_str) <= max_length:
        return text_str
    return text_str[:max_length] + "..."

def truncate_csv(input_file, output_file=None):
    """Truncate all text fields in CSV to 20 characters plus '...'."""
    
    if output_file is None:
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_truncated_{timestamp}.csv"
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                # Truncate all fields
                truncated_row = {}
                for field, value in row.items():
                    truncated_row[field] = truncate_text(value)
                writer.writerow(truncated_row)
    
    print(f"Truncated CSV saved as: {output_file}")
    return output_file

if __name__ == "__main__":
    # Use the current CSV file
    input_csv = "ragas_results_20250805_130807.csv"
    
    if os.path.exists(input_csv):
        output_csv = truncate_csv(input_csv)
        print(f"Successfully truncated {input_csv} to {output_csv}")
    else:
        print(f"File {input_csv} not found in current directory") 