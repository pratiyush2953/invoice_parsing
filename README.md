
# Invoice Extraction and Parsing with Groq LLM

This project provides a tool to extract, parse, and convert invoice data from PDF documents into a structured CSV format. It uses a combination of libraries like `pymupdf4llm` for PDF text extraction, `Groq LLM` for natural language processing, and outputs the data as CSV files for further use.

## Features

- **Extract Text from PDF**: Converts text from PDF files to Markdown format using the `pymupdf4llm` library.
- **Parse Invoice Data**: Uses the Groq LLM to process the extracted text and convert it into structured JSON data.
- **Export to CSV**: Converts the structured JSON data into a CSV format that is suitable for further analysis.
- **Folder Management**: Automatically creates a folder if it doesn't already exist for saving the output CSV files.
- **Dynamic Invoice Parsing**: Supports extraction of key invoice fields such as `Invoice #`, `Invoice Date`, `Line Item Description`, `Service Date`, and more.

## Requirements

To run this project, you will need the following Python libraries:

```bash
pip install -q pymupdf pymupdf4llm groq anthropic instructor python-dotenv
```

- `pymupdf`: PDF text extraction library.
- `pymupdf4llm`: Used to convert the extracted PDF text into a markdown format.
- `groq`: A Groq client for interacting with Groq LLM APIs.
- `anthropic`: Required for specific functionalities (if needed).
- `instructor`: Used for integrating Groq with custom functions.
- `python-dotenv`: Loads environment variables from `.env` files.

Additionally, you will need a Groq API key, which should be saved in a `.env` file in your project directory.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/invoice-extraction.git
cd invoice-extraction
```

### 2. Install Dependencies

Use pip to install the required Python packages:

```bash
pip install -q pymupdf pymupdf4llm groq anthropic instructor python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the project with your Groq API key:

```bash
GROQ_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key provided by Groq.

### 4. Run the Application

Run the main Python script to extract and parse data from your PDF file:

```bash
python main.py
```

The script will ask you for the path of the PDF you want to process, and it will save the output as a CSV file in the `RESULT_CSV` folder.

## Code Overview

### `main.py`

This is the main script that orchestrates the workflow:
1. Extracts text from a PDF file.
2. Passes the extracted text to Groq LLM for parsing and structuring the data.
3. Converts the structured data into a CSV format.
4. Saves the CSV file in a specified directory.

### Key Functions

- **`create_folder(folder_path)`**: Creates a folder if it doesn't already exist.
- **`extract_text_from_pdf(pdf_path)`**: Extracts text from the given PDF file using the `pymupdf4llm` library.
- **`parse_with_groq_llm(extracted_text, pdf_file_path)`**: Sends the extracted text to the Groq LLM for structured data extraction.
- **`json_to_csv(json_string, file_name)`**: Converts the extracted JSON data into a CSV file.
- **`main()`**: The entry point that ties everything together—handles user input, file processing, and output.

## How It Works

1. **Text Extraction**: The script begins by extracting the raw text from the provided PDF using the `pymupdf4llm` library. It splits the text into different invoices.
2. **Data Parsing with Groq**: The extracted text is then passed to Groq LLM to extract structured data, such as `Invoice #`, `Service Date`, `Employee Name`, `Item Description`, etc.
3. **Exporting to CSV**: The parsed JSON is then converted into a CSV file, where each row represents a line item in the invoice. The CSV file will have columns like `Invoice #`, `Line Item Description`, `Service Date`, etc.
4. **Folder Creation**: The script checks if the `RESULT_CSV` folder exists and creates it if not. The output CSV is saved inside this folder.

## Sample Output CSV

Here is an example of how the output CSV might look after processing a sample invoice:

| Invoice # | Invoice Date | Day       | Line Item Description | Employee Name | Service Date | County    | Location   | Work Order # | Hours/Qty | Units | Rate | Invoiced Amount | Sub-Total | Sales-Tax | Total | Original File | Invoice Pages |
|-----------|--------------|-----------|-----------------------|---------------|--------------|-----------|------------|--------------|-----------|-------|------|-----------------|-----------|-----------|-------|---------------|---------------|
| 12345     | 2024-12-01   | Monday    | Web Development       | John Doe      | 2024-11-30   | Sample    | Location A | WO123        | 5         | hour  | 50   | 250             | 250       | 15        | 287.5 | invoice.pdf   | 1             |
| 12345     | 2024-12-01   | Monday    | Hosting               | John Doe      | 2024-11-29   | Sample    | Location A | WO123        | 2         | hour  | 75   | 150             | 250       | 15        | 287.5 | invoice.pdf   | 1             |

## Troubleshooting

If you encounter any issues, here are some common solutions:

1. **Invalid Groq API Key**: Ensure that the `GROQ_API_KEY` in your `.env` file is correct and active.
2. **PDF Parsing Errors**: The `pymupdf4llm` library may not be able to extract text properly from certain types of PDFs (e.g., scanned documents). Ensure your PDFs are text-based.
3. **No Output Folder Created**: If the `RESULT_CSV` folder is not created, ensure that you have permission to write to the directory, or modify the path to an existing directory.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests. Contributions are always welcome!

### Steps for Contributing:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Open a pull request.


