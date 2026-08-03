"""
Test script for Excel file creation
"""

import sys
import os
from datetime import datetime

# Get the project root directory (Synaptix folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, PROJECT_ROOT)

from ext_util import create_excel_file, write_to_excel


if __name__ == "__main__":
    # Test creating an Excel file
    folder_path = os.path.join(PROJECT_ROOT, "Rest_API_Data")

    # Generate filename with timestamp: Swagger_Data_YYYY_MM_DD_HH_MM
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"Swagger_Data_{timestamp}"

    sheet_name = "SwaggerData"

    file_path = create_excel_file(folder_path, filename, sheet_name)

    # Test write_to_excel with sample data
    sample_data = [
        ["Name", "Age", "City", "Occupation"],
        ["John Doe", 30, "New York", "Engineer"],
        ["Jane Smith", 28, "Los Angeles", "Designer"],
        ["Bob Johnson", 35, "Chicago", "Manager"],
        ["Alice Brown", 32, "Houston", "Developer"]
    ]

    write_to_excel(file_path, sheet_name, sample_data)

    print(f"\n✅ Test completed!")
    print(f"File created at: {file_path}")
    print(f"Data written to sheet: {sheet_name}")
    print(f"Check the folder: {folder_path}")
