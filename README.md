# Standalone Batch EML Extractor

A Python utility to batch extract and process `.eml` files, converting each email into a structured folder with extracted headers, body content, and attachments. Now includes a modern graphical user interface!

## Features

- **Modern GUI Interface**: User-friendly graphical interface with progress tracking
- **Batch Processing**: Process multiple `.eml` files in a single operation
- **Safe Filename Handling**: Sanitizes attachment filenames that contain path separators and problematic characters
- **Email Content Extraction**:
  - Headers (From, To, Subject, Date, Cc, Message-ID)
  - Plain text body
  - HTML body
  - Attachments with safe filenames
- **Duplicate Handling**: Automatically handles duplicate folder and file names
- **Error Resilience**: Continues processing even if individual emails fail
- **Real-time Progress**: Live progress bar and processing log
- **Folder Browser**: Built-in folder selection dialogs

## Usage

### Windows Executable Download (Easiest)

Download the pre-built Windows executables:

**[📥 Download Windows Executables](https://github.com/jordanmaulana/eml-extractor/releases/EMLExtractorGUI.exe)**

- **EMLExtractorGUI.exe**: Graphical interface (recommended)
- No Python installation required
- Simply download, extract, and run

### Graphical User Interface (Recommended)

Launch the modern GUI application:

```bash
python gui.py
```

The GUI provides:
- **Folder Selection**: Browse buttons for input and output folders
- **Progress Tracking**: Real-time progress bar and status updates
- **Processing Log**: Color-coded log showing extraction details
- **Error Handling**: Clear error messages and warnings
- **Statistics**: Live count of successful and failed extractions

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

- Python 3.8+
- Standard library only (no external dependencies)
- Tkinter (included with Python)

## Installation

### Option 1: Windows Executable (Easiest)

**[📥 Download Windows Executables](https://github.com/yourusername/eml-extractor/releases/latest)**

1. Download the latest Windows release
2. Extract the ZIP file
3. Double-click `EMLExtractorGUI.exe` to launch the GUI
4. No Python installation required!

### Option 2: Run from Source (Recommended for developers)

1. Clone or download this repository
2. Run the GUI directly:
   ```bash
   python gui.py
   ```
   
The GUI provides:
- **Folder Selection**: Browse buttons for input and output folders
- **Progress Tracking**: Real-time progress bar and status updates
- **Processing Log**: Color-coded log showing extraction details
- **Error Handling**: Clear error messages and warnings
- **Statistics**: Live count of successful and failed extractions
   
### Option 3: Install as Package
```bash
pip install -e .
eml-extractor-gui  # Launch GUI
```

### Option 4: Build Executables

#### Quick Build (Auto-detect platform)
```bash
python build.py
```

#### Platform-specific Builds
```bash
python build.py windows    # Build Windows .exe files
python build.py macos      # Build macOS .app bundle
python build.py linux      # Build Linux executables
python build.py all        # Build for all platforms
```

#### Manual Build with PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="EML Extractor" gui.py
```

## Executable Distributions

After building, executables will be available in the `dist/` directory:

### Windows
- **EMLExtractorGUI.exe**: Graphical interface

### macOS
- **EML Extractor.app**: Native app bundle

### Linux
- **eml-extractor-gui**: Graphical executable
- **install.sh**: Installation script for system-wide installation

## Error Handling

- Reports total, successful, and failed extractions
- Continues processing if individual emails encounter errors
- Warns about attachments that couldn't be saved

## Version

v2.2 - Added cross-platform executable builds
v2.1 - Added modern graphical user interface
v2.0 - Improved filename sanitization for attachment safety
