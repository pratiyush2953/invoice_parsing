import pymupdf4llm
import csv
from groq import Groq
import os
from pydantic import BaseModel, Field
from typing import List, Optional
import instructor
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)


class InvoiceData(BaseModel):
    invoice_number: List[str] = Field(..., description="List of invoice numbers")
    invoice_date: List[str] = Field(..., description="List of invoice dates")
    line_item_description: List[str] = Field(..., description="List of descriptions of the line item")
    employee_name: Optional[List[str]] = None  # Can be None if not available
    service_date: Optional[List[str]] = None  # Can be None if not available
    county: List[str] = Field(..., description="List of counties")
    location: List[str] = Field(..., description="List of locations")
    work_order_number: List[str] = Field(..., description="List of work order numbers")
    hours_qty: Optional[List[str]] = None  # Can be None if not available
    unit: Optional[List[str]] = None  # Can be None if not available
    rate: Optional[List[str]] = None  # Can be None if not available
    invoiced_amount: List[str] = Field(..., description="List of invoiced amounts")
    sub_total: Optional[List[str]] = None  # Can be None if not available
    sales_tax: Optional[List[str]] = None  # Can be None if not available
    total: Optional[List[str]] = None  # Can be None if not available
    original_file: Optional[List[str]] = None  # Can be None if not available
    invoice_pages: Optional[List[str]] = None  # Can be None if not available


# Function to create folder if not exists
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pymupdf4llm.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        text = pymupdf4llm.to_markdown(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def parse_with_groq_llm(extracted_text, pdf_file_path):
    """
    Extract structured invoice data from the extracted text using a Groq LLM.

    Args:
        extracted_text (str): The invoice text extracted from the PDF.
        pdf_file_path (str): The file path of the PDF being analyzed.

    Returns:
        str: JSON-formatted structured data or None in case of an error.
    """
    try:
        # System prompts consolidated to reduce redundancy and token usage
        prompt_messages = [
            {
                "role": "system",
                "content": (
                    "You are an intelligent invoice analyzer. Extract structured data for each row of an invoice "
                    "into a JSON format compatible with CSV. Follow these guidelines:\n\n"
                    "- Missing values should be represented as 'nan'.\n"
                    "- Repetitive/static values should be repeated to maintain consistent column lengths.\n"
                    "- Output must be valid JSON with keys as column names and lists as values.\n"
                    "- Ensure all columns have equal-length lists.\n"
                    """
                    Item price * units = invoiced amount
                    Sum of invoiced amounts = sub-total
                    Total = sub-total + sales tax
                    """
                    "- Only return the VALID JSON STRING **STARTING WITH { AND ENDING WITH }** -  not the code"
                ),
            },
            {
                "role": "system",
                "content": (
                    "Column Descriptions:\n"
                    "- Invoice #: Unique identifier, repeat to fill column length. It will be same for all - Repeat it\n"
                    "- Invoice Date: Issue date, repeat to fill column length. It is on the top of every page, Near to invoice number\n"
                    "- Day: Day of the week, repeat to fill column length. It relevant to Service Date - do it according to service date\n"
                    "- Line Item Description: Details of services/items invoiced.\n"
                    "- Employee Name: Name of the associated employee.\n"
                    "- Service Date: Date service was performed, repeat to fill column length.The changing dates are service dates \n"
                    "- County: County of service, repeat to fill column length. It will be same for all - Repeat it\n"
                    "- Location: Specific location details, repeat to fill column length. It will be same for all - Repeat it\n"
                    "- Work Order #: Work order number, repeat to fill column length.It will be same for all - Repeat it\n"
                    "- Hours/Qty: Number of hours worked or items provided.Quantity\n"
                    "- Units: It is the measure of quantity (eg. hour/ kg ), If you don't find any - write UNKNOWN in it's place - Don't put any other unit"
                    "- Rate: Rate charged per unit.\n"
                    "- Invoiced Amount: Amount charged for the line item.\n"
                    "- Sub-Total: Subtotal before taxes, repeat to fill column length.\n"
                    "- Sales-Tax: Sales tax percentage, repeat to fill column length. It will be same for all - Repeat it\n"
                    "- Total: Total invoice amount, including tax. Near to TOTAL word in context - Repeat it\n"
                    "- Original File: Name of the original file, repeat to fill column length.\n"
                    "- Invoice Pages: It is the page number passed on with the context, repeat to fill column length.\n\n"
                    "Ensure the response is in valid JSON format with equal-length lists for all columns."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Extract the invoice details from the following text:\n\n"
                    f"Text:\n{extracted_text}\n\n"
                    f"File Path: {pdf_file_path}"
                ),
            },
        ]

        # Call to Groq LLM API
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=prompt_messages,
        )
        
        # llama-3.1-8b-instant
        # mixtral-8x7b-32768
        # Parse and return the response content
        return resp.choices[0].message.content

    except Exception as e:
        # Improved error handling
        print(f"Error in parse_invoice_with_groq_llm: {str(e)}")
        return None

def json_to_csv(json_string, file_name):
    """
    Converts a JSON string to a CSV file.

    Args:
        json_string (str): The JSON string containing the data.
        file_name (str): The name of the output CSV file.

    Returns:
        None
    """
    try:
        # Load the JSON string into a Python dictionary
        data = json.loads(json_string)

        # Extract the keys (column names) from the dictionary
        columns = list(data.keys())

        # Get the number of rows (assuming all lists are of the same length)
        num_rows = len(data[columns[0]])

        # Open the CSV file for writing
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header row (column names)
            writer.writerow(columns)

            # Write the data rows
            for i in range(num_rows):
                row = [data[column][i] for column in columns]
                writer.writerow(row)

        print(f"CSV file '{file_name}' has been successfully created.")

    except Exception as e:
        print(f"Error: {e}")

def main():
    """
    Main function to extract text, parse it, and save to CSV.
    """
    try:
        # Input and output file paths
        pdf_file_path = input("Please enter the file path : ")
        output_csv_path = "output.csv"
        json_array = []
        folder_path = "RESULT_CSV"

        # Step 1: Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_file_path).split("-----")
        if not extracted_text:
            print("Failed to extract text from the PDF.")
            return

        content = ""
        count = 1
        for invoice in extracted_text[1:]:
            if "invoice #" in invoice.lower():
                content = content + '\n' + invoice
            
        structured_data = parse_with_groq_llm(content, pdf_file_path)
        
        # Extract file name without extension
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

        # Create folder if it does not exist
        create_folder(folder_path)

        # Construct the full path for the CSV file
        csv_file_path = os.path.join(folder_path, file_name + ".csv")
                
        json_to_csv(structured_data, file_name+".csv")
        return "Success"
    
    except Exception as e:
        return f"Error : {e}"

if __name__ == "__main__":
    print(main())
