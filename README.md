# Standalone Batch EML Extractor

A Python utility to batch extract and process `.eml` files, converting each email into a structured folder with extracted headers, body content, and attachments.

## Features

- **Batch Processing**: Process multiple `.eml` files in a single operation
- **Safe Filename Handling**: Sanitizes attachment filenames that contain path separators and problematic characters
- **Email Content Extraction**:
  - Headers (From, To, Subject, Date, Cc, Message-ID)
  - Plain text body
  - HTML body
  - Attachments with safe filenames
- **Duplicate Handling**: Automatically handles duplicate folder and file names
- **Error Resilience**: Continues processing even if individual emails fail

## Usage

### Basic Usage

```bash
python main.py <input_folder>
```

### With Custom Output Folder

```bash
python main.py <input_folder> <output_folder>
```

### Arguments

- `input_folder` (required): Folder containing `.eml` files
- `output_folder` (optional): Base folder for extracted content (default: `extracted_emails`)

### Examples

```bash
python main.py my_emails/
python main.py my_emails/ output/
```

## Output Structure

For each `.eml` file processed, a separate folder is created with the following structure:

```
output_folder/
├── email_1/
│   ├── headers.txt          # Email headers
│   ├── body_plain.txt       # Plain text body
│   ├── body_html.html       # HTML body
│   └── attachments/         # Attachments folder (if any)
│       └── file_name.pdf
├── email_2/
│   ├── headers.txt
│   └── ...
└── ...
```

## Key Features

### Filename Sanitization

The tool handles problematic attachment filenames that could cause errors, such as:

- `company\materials\file.pdf` → `company_materials_file.pdf`
- `contract:v2.docx` → `contract_v2.docx`
- Files with special characters like `<`, `>`, `:`, `*`, `?`, etc.

### Headers Extracted

Each email's `headers.txt` includes:

- From
- To
- Subject
- Date
- Cc
- Message-ID

### Content Types Supported

- Plain text bodies (`text/plain`)
- HTML bodies (`text/html`)
- Multipart emails with attachments

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Error Handling

- Reports total, successful, and failed extractions
- Continues processing if individual emails encounter errors
- Warns about attachments that couldn't be saved

## Version

v2.0 - Improved filename sanitization for attachment safety
