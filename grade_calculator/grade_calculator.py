#!/usr/bin/env python3
"""
Grade Calculator - Calculates final grades based on exam results and statistics.
This script processes exam data from JSON files and calculates grades using various methods.
"""

import json
import math
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ExamComponent:
    """Represents an exam component with its score and statistics."""
    name: str
    score: float
    percentage: float
    average: float
    standard_deviation: float
    student_count: int
    rank: Optional[int] = None

class GradeCalculator:
    """Grade calculator that processes exam data and calculates final grades."""
    
    def __init__(self):
        self.exam_components: List[ExamComponent] = []
        self.final_grade: Optional[float] = None
        self.grade_letter: Optional[str] = None
        self.statistics: Dict[str, Any] = {}
    
    def load_data_from_json(self, json_file: str) -> bool:
        """
        Load exam data from a JSON file.
        
        Args:
            json_file (str): Path to the JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Clear existing data
            self.exam_components.clear()
            
            # Process the data based on expected format
            if isinstance(data, list):
                # Format: [{"Ad": "Q", "Not": 40.00}, ...]
                for item in data:
                    if "Ad" in item and "Not" in item:
                        component = ExamComponent(
                            name=item["Ad"],
                            score=float(item["Not"]),
                            percentage=0.0,  # Will be calculated later
                            average=0.0,     # Will be provided or calculated
                            standard_deviation=0.0,  # Will be provided or calculated
                            student_count=0,  # Will be provided
                            rank=None
                        )
                        self.exam_components.append(component)
            
            elif isinstance(data, dict):
                # Format: {"components": [...], "statistics": {...}}
                if "components" in data:
                    for comp_data in data["components"]:
                        component = ExamComponent(
                            name=comp_data.get("name", ""),
                            score=float(comp_data.get("score", 0)),
                            percentage=float(comp_data.get("percentage", 0)),
                            average=float(comp_data.get("average", 0)),
                            standard_deviation=float(comp_data.get("standard_deviation", 0)),
                            student_count=int(comp_data.get("student_count", 0)),
                            rank=comp_data.get("rank")
                        )
                        self.exam_components.append(component)
                
                # Store additional statistics
                if "statistics" in data:
                    self.statistics = data["statistics"]
            
            print(f"Loaded {len(self.exam_components)} exam components from {json_file}")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format - {e}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def calculate_percentages(self, total_percentage: float = 100.0) -> None:
        """
        Calculate percentages for each component if not provided.
        
        Args:
            total_percentage (float): Total percentage to distribute
        """
        if not self.exam_components:
            return
        
        # If percentages are not set, distribute equally
        equal_percentage = total_percentage / len(self.exam_components)
        
        for component in self.exam_components:
            if component.percentage == 0.0:
                component.percentage = equal_percentage
    
    def calculate_weighted_grade(self) -> float:
        """
        Calculate weighted final grade based on component scores and percentages.
        
        Returns:
            float: Weighted final grade
        """
        if not self.exam_components:
            return 0.0
        
        weighted_sum = 0.0
        total_percentage = 0.0
        
        for component in self.exam_components:
            weighted_sum += (component.score * component.percentage / 100.0)
            total_percentage += component.percentage
        
        if total_percentage > 0:
            self.final_grade = weighted_sum * (100.0 / total_percentage)
        else:
            self.final_grade = 0.0
        
        return self.final_grade
    
    def calculate_z_scores(self) -> Dict[str, float]:
        """
        Calculate Z-scores for each component based on average and standard deviation.
        
        Returns:
            Dict[str, float]: Z-scores for each component
        """
        z_scores = {}
        
        for component in self.exam_components:
            if component.standard_deviation > 0:
                z_score = (component.score - component.average) / component.standard_deviation
                z_scores[component.name] = z_score
            else:
                z_scores[component.name] = 0.0
        
        return z_scores
    
    def calculate_percentile_rank(self) -> Dict[str, float]:
        """
        Calculate percentile rank for each component.
        
        Returns:
            Dict[str, float]: Percentile ranks (0-100)
        """
        percentile_ranks = {}
        
        for component in self.exam_components:
            if component.standard_deviation > 0:
                z_score = (component.score - component.average) / component.standard_deviation
                # Convert Z-score to percentile using normal distribution
                percentile = 0.5 * (1 + math.erf(z_score / math.sqrt(2))) * 100
                percentile_ranks[component.name] = percentile
            else:
                percentile_ranks[component.name] = 50.0  # Default to median
        
        return percentile_ranks
    
    def assign_letter_grade_catalog(self, grade: float) -> str:
        """
        Assign letter grade using catalog method (fixed grade boundaries).
        
        Args:
            grade (float): Numerical grade
            
        Returns:
            str: Letter grade
        """
        if grade >= 90:
            return "AA"
        elif grade >= 85:
            return "BA"
        elif grade >= 80:
            return "BB"
        elif grade >= 75:
            return "CB"
        elif grade >= 70:
            return "CC"
        elif grade >= 65:
            return "DC"
        elif grade >= 60:
            return "DD"
        elif grade >= 50:
            return "FD"
        else:
            return "FF"
    
    def assign_letter_grade_sd_method(self, grade: float, average: float, standard_deviation: float) -> str:
        """
        Assign letter grade using +/- SD method (standard deviation based).
        
        Args:
            grade (float): Numerical grade
            average (float): Class average
            standard_deviation (float): Class standard deviation
            
        Returns:
            str: Letter grade
        """
        if standard_deviation <= 0:
            # Fallback to catalog method if no standard deviation
            return self.assign_letter_grade_catalog(grade)
        
        # Calculate Z-score
        z_score = (grade - average) / standard_deviation
        
        # SD-based grading scale
        if z_score >= 1.5:
            return "AA"
        elif z_score >= 1.0:
            return "BA"
        elif z_score >= 0.5:
            return "BB"
        elif z_score >= 0.0:
            return "CB"
        elif z_score >= -0.5:
            return "CC"
        elif z_score >= -1.0:
            return "DC"
        elif z_score >= -1.5:
            return "DD"
        elif z_score >= -2.0:
            return "FD"
        else:
            return "FF"
    
    def assign_letter_grade(self, grade: float, method: str = "catalog", average: float = None, standard_deviation: float = None) -> str:
        """
        Assign letter grade using specified method.
        
        Args:
            grade (float): Numerical grade
            method (str): Grading method ("catalog" or "sd_method")
            average (float): Class average (required for sd_method)
            standard_deviation (float): Class standard deviation (required for sd_method)
            
        Returns:
            str: Letter grade
        """
        if method.lower() == "sd_method":
            if average is None or standard_deviation is None:
                print("Warning: Average and standard deviation required for SD method. Falling back to catalog method.")
                return self.assign_letter_grade_catalog(grade)
            return self.assign_letter_grade_sd_method(grade, average, standard_deviation)
        else:
            # Default to catalog method
            return self.assign_letter_grade_catalog(grade)
    
    def calculate_final_grade_with_letter(self, method: str = "catalog") -> Dict[str, Any]:
        """
        Calculate final grade and assign letter grade.
        
        Args:
            method (str): Grading method ("catalog" or "sd_method")
            
        Returns:
            Dict[str, Any]: Final grade information
        """
        final_grade = self.calculate_weighted_grade()
        
        # Calculate overall class statistics for SD method
        overall_average = None
        overall_std_dev = None
        
        if method.lower() == "sd_method" and self.exam_components:
            # Calculate weighted average of class averages
            total_weight = sum(comp.percentage for comp in self.exam_components)
            if total_weight > 0:
                overall_average = sum(comp.average * comp.percentage for comp in self.exam_components) / total_weight
                
                # Calculate weighted standard deviation (simplified approach)
                weighted_variance = sum(comp.standard_deviation**2 * comp.percentage for comp in self.exam_components) / total_weight
                overall_std_dev = math.sqrt(weighted_variance)
        
        letter_grade = self.assign_letter_grade(final_grade, method, overall_average, overall_std_dev)
        
        self.final_grade = final_grade
        self.grade_letter = letter_grade
        
        return {
            "final_grade": final_grade,
            "letter_grade": letter_grade,
            "grading_method": method,
            "overall_average": overall_average,
            "overall_standard_deviation": overall_std_dev,
            "components": [
                {
                    "name": comp.name,
                    "score": comp.score,
                    "percentage": comp.percentage,
                    "average": comp.average,
                    "standard_deviation": comp.standard_deviation,
                    "rank": comp.rank
                }
                for comp in self.exam_components
            ]
        }
    
    def generate_detailed_report(self) -> Dict[str, Any]:
        """
        Generate a detailed report with all calculations.
        
        Returns:
            Dict[str, Any]: Detailed report
        """
        z_scores = self.calculate_z_scores()
        percentile_ranks = self.calculate_percentile_rank()
        
        # Get grading method from statistics or default to catalog
        grading_method = self.statistics.get("grading_method", "catalog")
        final_grade_info = self.calculate_final_grade_with_letter(grading_method)
        
        report = {
            "calculation_date": datetime.now().isoformat(),
            "final_grade_info": final_grade_info,
            "component_analysis": [],
            "statistics": {
                "total_components": len(self.exam_components),
                "total_percentage": sum(comp.percentage for comp in self.exam_components),
                "average_score": statistics.mean(comp.score for comp in self.exam_components),
                "score_range": {
                    "min": min(comp.score for comp in self.exam_components),
                    "max": max(comp.score for comp in self.exam_components)
                },
                "grading_method": grading_method
            }
        }
        
        # Add detailed component analysis
        for component in self.exam_components:
            analysis = {
                "name": component.name,
                "score": component.score,
                "percentage": component.percentage,
                "weighted_contribution": component.score * component.percentage / 100.0,
                "average": component.average,
                "standard_deviation": component.standard_deviation,
                "z_score": z_scores.get(component.name, 0.0),
                "percentile_rank": percentile_ranks.get(component.name, 50.0),
                "rank": component.rank,
                "student_count": component.student_count
            }
            report["component_analysis"].append(analysis)
        
        return report
    
    def print_summary(self) -> None:
        """Print a summary of the grade calculation."""
        if not self.exam_components:
            print("No exam components loaded.")
            return
        
        # Get grading method from statistics or default to catalog
        grading_method = self.statistics.get("grading_method", "catalog")
        
        print("\n" + "="*50)
        print("GRADE CALCULATION SUMMARY")
        print("="*50)
        print(f"Grading Method: {grading_method.upper()}")
        
        # Print component details
        print("\nExam Components:")
        print("-" * 30)
        for comp in self.exam_components:
            print(f"{comp.name:2} | Score: {comp.score:6.2f} | Percentage: {comp.percentage:5.1f}% | "
                  f"Avg: {comp.average:6.2f} | StdDev: {comp.standard_deviation:6.2f}")
        
        # Calculate and print final grade
        final_grade_info = self.calculate_final_grade_with_letter(grading_method)
        
        print("\nFinal Grade:")
        print("-" * 30)
        print(f"Numerical Grade: {final_grade_info['final_grade']:.2f}")
        print(f"Letter Grade:    {final_grade_info['letter_grade']}")
        
        if grading_method.lower() == "sd_method":
            print(f"Class Average:   {final_grade_info.get('overall_average', 0):.2f}")
            print(f"Class StdDev:    {final_grade_info.get('overall_standard_deviation', 0):.2f}")
        
        # Print Z-scores and percentiles
        z_scores = self.calculate_z_scores()
        percentile_ranks = self.calculate_percentile_rank()
        
        print("\nComponent Analysis:")
        print("-" * 30)
        for comp in self.exam_components:
            z_score = z_scores.get(comp.name, 0.0)
            percentile = percentile_ranks.get(comp.name, 50.0)
            print(f"{comp.name}: Z-score = {z_score:+.2f}, Percentile = {percentile:.1f}%")
    
    def save_report_to_json(self, output_file: str) -> bool:
        """
        Save detailed report to JSON file.
        
        Args:
            output_file (str): Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            report = self.generate_detailed_report()
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(report, file, ensure_ascii=False, indent=2)
            
            print(f"Detailed report saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return False

def main():
    """Main function to run the grade calculator."""
    # Fixed input and output paths
    input_file = "grade_calculator/detailed_exam_data.json"
    output_file = "grade_calculator/your_grade_report.json"
    total_percentage = 100.0
    
    print(f"Loading exam data from: {input_file}")
    print(f"Output report will be saved to: {output_file}")
    
    # Create calculator
    calculator = GradeCalculator()
    
    # Load data
    if not calculator.load_data_from_json(input_file):
        print("Failed to load data. Exiting.")
        return
    
    # Calculate percentages if needed
    calculator.calculate_percentages(total_percentage)
    
    # Print summary
    calculator.print_summary()
    
    # Save detailed report
    calculator.save_report_to_json(output_file)

if __name__ == "__main__":
    main()
