#!/usr/bin/env python3
"""
Converter script to convert final_exams.psv to JSON format.
This script reads a pipe-separated values (PSV) file and converts it to JSON format.
"""

import json
import sys
from typing import List, Dict, Any

def read_psv_file(file_path: str) -> List[Dict[str, str]]:
    """
    Read a PSV file and return a list of dictionaries.
    
    Args:
        file_path (str): Path to the PSV file
        
    Returns:
        List[Dict[str, str]]: List of dictionaries where each dictionary represents a row
    """
    data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        if not lines:
            print("Error: File is empty")
            return data
            
        # Get headers from the first line
        headers = [header.strip() for header in lines[0].split('|')]
        
        # Process data rows
        for line_num, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            values = line.split('|')
            
            # Ensure we have the same number of values as headers
            if len(values) != len(headers):
                print(f"Warning: Line {line_num} has {len(values)} values but expected {len(headers)}")
                # Pad with empty strings if needed
                while len(values) < len(headers):
                    values.append("")
                # Truncate if too many values
                values = values[:len(headers)]
            
            # Create dictionary for this row
            row_dict = {}
            for i, header in enumerate(headers):
                row_dict[header] = values[i].strip()
            
            data.append(row_dict)
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return data

def save_json_file(data: List[Dict[str, str]], output_file: str) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data (List[Dict[str, str]]): Data to save
        output_file (str): Output file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False

def main():
    """Main function to convert PSV to JSON."""
    input_file = "../data/final_exams.psv"
    output_file = "../reports/final_exams.json"
    
    print(f"Converting {input_file} to {output_file}...")
    
    # Read PSV data
    data = read_psv_file(input_file)
    
    if not data:
        print("No data to convert. Exiting.")
        sys.exit(1)
    
    print(f"Read {len(data)} records from {input_file}")
    
    # Save as JSON
    if save_json_file(data, output_file):
        print(f"Successfully converted to {output_file}")
        print(f"Total records: {len(data)}")
        
        # Show sample of the converted data
        if data:
            print("\nSample of converted data:")
            print(json.dumps(data[0], ensure_ascii=False, indent=2))
    else:
        print("Failed to save JSON file")
        sys.exit(1)

if __name__ == "__main__":
    main()
