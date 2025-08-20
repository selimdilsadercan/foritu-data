#!/usr/bin/env python3
"""
Converter script to convert lessons.psv file to JSON format with sessions array.
Each line in the PSV file contains 11 fields separated by pipe (|) characters.
Location, days, times, and room fields will be parsed into sessions array.
"""

import json
import sys
from typing import List, Dict, Any

def parse_sessions(location: str, days: str, times: str, room: str) -> List[Dict[str, str]]:
    """
    Parse location, days, times, and room fields into sessions array.
    
    Args:
        location (str): Location field from PSV
        days (str): Days field from PSV
        times (str): Times field from PSV
        room (str): Room field from PSV
        
    Returns:
        List[Dict[str, str]]: Array of session objects
    """
    sessions = []
    
    # Split the fields by spaces to get individual values
    locations = location.split()
    days_list = days.split()
    times_list = times.split()
    rooms = room.split()
    
    # Find the maximum length to handle cases where some fields have more values
    max_length = max(len(locations), len(days_list), len(times_list), len(rooms))
    
    # Pad shorter lists with the last value or empty string
    while len(locations) < max_length:
        locations.append(locations[-1] if locations else "")
    while len(days_list) < max_length:
        days_list.append(days_list[-1] if days_list else "")
    while len(times_list) < max_length:
        times_list.append(times_list[-1] if times_list else "")
    while len(rooms) < max_length:
        rooms.append(rooms[-1] if rooms else "")
    
    # Create session objects
    for i in range(max_length):
        session = {
            "location": locations[i] if i < len(locations) else "",
            "day": days_list[i] if i < len(days_list) else "",
            "time": times_list[i] if i < len(times_list) else "",
            "room": rooms[i] if i < len(rooms) else ""
        }
        sessions.append(session)
    
    return sessions

def parse_psv_line(line: str) -> Dict[str, Any]:
    """
    Parse a single line from the PSV file and return a dictionary.
    
    Args:
        line (str): A line from the PSV file
        
    Returns:
        Dict[str, Any]: Parsed data as a dictionary
    """
    # Split the line by pipe character
    fields = line.strip().split('|')
    
    # Ensure we have exactly 11 fields
    if len(fields) != 11:
        print(f"Warning: Line has {len(fields)} fields instead of 11: {line[:100]}...")
        return None
    
    # Extract fields
    lesson_id = fields[0].strip()
    course_code = fields[1].strip()
    delivery_mode = fields[2].strip()
    instructor = fields[3].strip()
    location = fields[4].strip()
    days = fields[5].strip()
    times = fields[6].strip()
    room = fields[7].strip()
    capacity = fields[8].strip()
    enrolled = fields[9].strip()
    allowed_programs_str = fields[10].strip()
    
    # Parse allowed programs
    allowed_programs = [prog.strip() for prog in allowed_programs_str.split(',') if prog.strip()]
    
    # Parse sessions
    sessions = parse_sessions(location, days, times, room)
    
    # Create lesson object
    lesson = {
        "lesson_id": lesson_id,
        "course_code": course_code,
        "delivery_mode": delivery_mode,
        "instructor": instructor,
        "sessions": sessions,
        "capacity": capacity,
        "enrolled": enrolled,
        "allowed_programs": allowed_programs
    }
    
    return lesson

def convert_psv_to_json(input_file: str, output_file: str) -> None:
    """
    Convert PSV file to JSON format with sessions array.
    
    Args:
        input_file (str): Path to input PSV file
        output_file (str): Path to output JSON file
    """
    lessons = []
    line_count = 0
    error_count = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                lesson = parse_psv_line(line)
                if lesson:
                    lessons.append(lesson)
                    line_count += 1
                else:
                    error_count += 1
                    print(f"Error parsing line {line_num}")
        
        # Create the final JSON structure
        json_data = {
            "metadata": {
                "source_file": input_file,
                "total_lessons": len(lessons),
                "conversion_notes": "Location, days, times, and room fields parsed into sessions array"
            },
            "lessons": lessons
        }
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"Conversion completed successfully!")
        print(f"Total lessons processed: {line_count}")
        print(f"Errors encountered: {error_count}")
        print(f"Output file: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

def main():
    """Main function to run conversion with fixed input filename."""
    input_file = "../data/lessons.psv"
    output_file = "../reports/lessons.json"
    
    convert_psv_to_json(input_file, output_file)

if __name__ == "__main__":
    main()
