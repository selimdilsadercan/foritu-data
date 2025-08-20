# Foritu Data Project

This project contains tools for converting and analyzing educational data, including exam schedules, course information, and grade calculations.

## 📁 Project Structure

```
foritu-data/
├── 📂 converters/          # PSV to JSON conversion scripts
├── 📂 data/               # Raw data files (PSV, TXT, PDF)
├── 📂 grade_calculator/   # Grade calculation tools
├── 📂 reports/            # Generated JSON reports
└── 📄 README.md           # This file
```

## 🛠️ Converters

**Location**: `converters/`

Contains Python scripts to convert Pipe-Separated Values (PSV) files to JSON format:

- `convert_final_exams_psv_to_json.py` - Converts final exam schedule data
- `convert_lessons_psv_to_json.py` - Converts lesson schedule data
- `convert_courses_psv_to_json.py` - Converts course information
- `convert_all_plans.py` - Converts all academic plans
- `convert_plan.py` - Converts individual plan data
- `convert_trasncript.py` - Converts transcript data

### Usage Example:

```bash
cd converters
python convert_final_exams_psv_to_json.py
```

## 📊 Data Files

**Location**: `data/`

Raw data files in various formats:

- `final_exams.psv` - Final exam schedule data
- `lessons.psv` - Lesson schedule data
- `courses.psv` - Course information
- `lessons.txt` - Lesson information in text format
- `plan.txt` - Academic plan information
- `course_plans.txt` - Course plan details
- `transkript.pdf` - Student transcript (PDF)

## 🧮 Grade Calculator

**Location**: `grade_calculator/`

A comprehensive grade calculation tool that processes exam data and calculates final grades using statistical methods.

### Files:

- `grade_calculator.py` - Main grade calculation script
- `detailed_exam_data.json` - Your exam data with statistics

### Features:

- **Weighted Grade Calculation**: Calculates final grades based on component percentages
- **Statistical Analysis**: Z-scores, percentile ranks, and class comparisons
- **Letter Grade Assignment**: Converts numerical grades to letter grades
- **Detailed Reporting**: Generates comprehensive analysis reports

### Usage:

```bash
cd grade_calculator
python grade_calculator.py --input detailed_exam_data.json --output your_grade_report.json
```

### Your Current Grade Summary:

- **Final Grade**: 68.90 (DC)
- **Components**: Q (15%), H (15%), V (30%), F (40%)
- **Best Performance**: V (Midterm) - 88th percentile
- **Weakest Performance**: Q (Quiz) - 4.4th percentile

## 📈 Reports

**Location**: `reports/`

Generated JSON reports from various conversions and calculations:

- `final_exams.json` - Converted final exam schedule
- `lessons.json` - Converted lesson schedule
- `courses_simple.json` - Converted course information
- `all_plans.json` - Converted academic plans
- `transcript_simple.json` - Converted transcript data
- `plan.json` - Converted plan data
- `your_grade_report.json` - Your detailed grade analysis
- `sample_grade_report.json` - Sample grade report

## 🚀 Quick Start

1. **Convert Data**:

   ```bash
   cd converters
   python convert_final_exams_psv_to_json.py
   ```

2. **Calculate Grades**:

   ```bash
   cd grade_calculator
   python grade_calculator.py --input detailed_exam_data.json --output your_grade_report.json
   ```

3. **View Results**:
   Check the `reports/` folder for generated JSON files.

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## 🔧 Customization

### Adding New Exam Data:

1. Edit `grade_calculator/detailed_exam_data.json`
2. Update your scores, percentages, and statistics
3. Run the grade calculator to see updated results

### Converting New Data:

1. Place your PSV file in the `data/` folder
2. Create a new converter script in `converters/`
3. Run the conversion to generate JSON reports

## 📊 Data Formats

### PSV Format:

```
Column1|Column2|Column3
Value1|Value2|Value3
```

### Exam Data JSON Format:

```json
{
  "components": [
    {
      "name": "Q",
      "score": 40.0,
      "percentage": 15.0,
      "average": 68.06,
      "standard_deviation": 16.41,
      "student_count": 78,
      "rank": 66
    }
  ]
}
```

## 📝 Notes

- All converters handle UTF-8 encoding for Turkish characters
- Grade calculator includes comprehensive error handling
- Reports are generated with timestamps and metadata
- Statistical calculations use standard normal distribution assumptions

## 🤝 Contributing

When adding new files:

1. Place raw data in `data/`
2. Add converters in `converters/`
3. Generate reports in `reports/`
4. Update this README with new functionality
