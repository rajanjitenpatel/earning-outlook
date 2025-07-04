# Lucid PDF Scraper

This project contains a Python script to download all available PDF documents from the Lucid Motors investor relations website.

The script iterates through node IDs from 1000 to 9999 and attempts to download a PDF from the URL pattern `https://ir.lucidmotors.com/node/<node_id>/pdf`.

## Setup

1.  Make sure you have Python 3 installed.
2.  Create a project directory and the files as described.
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scraper from your terminal:
```bash
python3 scraper.py
```

The script will create a `lucid_pdfs` directory in the project folder and save any found PDF files there. It will print its progress to the console.