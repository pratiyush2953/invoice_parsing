Invoice Data Extraction and CSV Conversion
This repository contains a Python script that extracts structured invoice data from PDF files and converts it into a CSV format. The process utilizes advanced AI capabilities for data extraction using Groq's language model and PyMuPDF for PDF text extraction. The script provides a user-friendly interface for inputting file paths, performing the data extraction, and saving the structured data in a CSV file format.

Features
PDF Text Extraction: Extracts text content from PDF invoices using the pymupdf4llm library.
Invoice Data Parsing: Uses Groq's large language model (LLM) to analyze and structure the invoice data.
CSV Conversion: Converts structured invoice data into a well-organized CSV format.
Error Handling: Robust error handling for PDF extraction, data parsing, and CSV writing.
Environment Configuration: Loads sensitive configuration values like API keys from environment variables.
Installation
Prerequisites
Before running the script, ensure you have Python 3.x installed on your system. You will also need the following dependencies:

pymupdf
pymupdf4llm
groq
anthropic
instructor
python-dotenv
Step 1: Install Required Libraries
You can install all the necessary libraries by running the following command:

bash
Copy code
!pip install -q pymupdf pymupdf4llm groq anthropic instructor python-dotenv
Step 2: Configure Environment Variables
Create a .env file in the project directory to securely store your API keys. The .env file should contain the following:

env
Copy code
GROQ_API_KEY=your_api_key_here
Replace your_api_key_here with your actual API key from Groq.

Step 3: Ensure Python Environment
Make sure to run the script in an environment where all dependencies are available, such as a virtual environment.

Usage
Running the Script
To run the script, simply execute the Python file. You will be prompted to enter the file path of the PDF you want to extract data from. The structured data will be extracted and saved in a CSV format in the RESULT_CSV folder.

bash
Copy code
python implementation_code.py
Parameters
PDF File Path: The script requires the path to a PDF file containing invoice data.

The PDF should follow a consistent format with invoicing details.
The script extracts key data like invoice number, date, item description, quantity, rate, and total.
Output Folder: The script saves the resulting CSV in a folder called RESULT_CSV. If the folder doesn't exist, it will be created automatically.

Output CSV: The extracted invoice data is saved in a CSV file with a name based on the PDF file (e.g., invoice_123.csv).

Expected Output
After running the script, you will find the CSV file in the RESULT_CSV folder. The CSV file will contain the following columns, extracted from the invoice:

Invoice #: The unique invoice identifier.
Invoice Date: The date the invoice was issued.
Day: The day of the week corresponding to the service date.
Line Item Description: Description of the items/services invoiced.
Employee Name: Name of the employee associated with the invoice.
Service Date: Date when the service was performed.
County: The county where the service was provided.
Location: Specific location details.
Work Order #: Work order number.
Hours/Qty: Number of hours worked or quantity of items.
Units: Units used (e.g., hour, kg).
Rate: Rate charged per unit.
Invoiced Amount: Amount charged for each line item.
Sub-Total: Subtotal before taxes.
Sales-Tax: Sales tax percentage applied to the invoice.
Total: Total invoice amount, including tax.
Original File: The name of the original PDF file.
Invoice Pages: Page numbers of the original invoice.
Example Output
csv
Copy code
Invoice #,Invoice Date,Day,Line Item Description,Employee Name,Service Date,County,Location,Work Order #,Hours/Qty,Units,Rate,Invoiced Amount,Sub-Total,Sales-Tax,Total,Original File,Invoice Pages
INV123,2023-12-25,Monday,Web development services,John Doe,2023-12-20,SomeCounty,Location1,WO456,5,hours,100,500,500,10,550,invoice_123.pdf,1
INV123,2023-12-25,Monday,SEO services,John Doe,2023-12-21,SomeCounty,Location1,WO456,3,hours,80,240,240,10,264,invoice_123.pdf,1
...
Code Explanation
The code is structured as follows:

Environment Setup: The script loads environment variables (such as API keys) using python-dotenv.
PDF Text Extraction: The function extract_text_from_pdf uses pymupdf4llm to extract text from a given PDF file.
Data Parsing: The function parse_with_groq_llm sends the extracted text to Groq's LLM to structure the invoice data based on predefined rules.
CSV Conversion: The function json_to_csv takes the structured JSON data and converts it into a CSV file.
Main Execution: The main function orchestrates the process by calling the extraction, parsing, and CSV conversion functions in sequence.
Error Handling
The script includes error handling for the following:

Text Extraction: If the PDF text extraction fails, the script will print an error message.
Data Parsing: If Groq's LLM fails to parse the invoice data, the script will handle the exception and provide a message.
CSV Conversion: If there are issues in saving the CSV file, the script will display an error message.
Conclusion
This script provides a robust solution for extracting and structuring invoice data from PDF files, converting it into a clean CSV format for further analysis or processing. It integrates advanced AI capabilities for accurate data extraction and can be easily extended or modified for additional use cases.