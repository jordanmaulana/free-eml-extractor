#!/usr/bin/env python3
"""
Standalone Batch EML Extractor (Updated)
All-in-one script to extract all .eml files from a folder into separate folders.
Now with improved filename sanitization to prevent directory creation errors.
"""

from email import policy
from email.parser import BytesParser
import os
import sys
from pathlib import Path


class EMLBatchProcessor:
    """Process multiple .eml files and extract to separate folders."""

    def __init__(self, input_folder, output_base="extracted_emails"):
        self.input_folder = Path(input_folder)
        self.output_base = Path(output_base)
        self.stats = {"total": 0, "successful": 0, "failed": 0}

    @staticmethod
    def sanitize_folder_name(filename):
        """Convert filename to safe folder name."""
        name = filename[:-4] if filename.lower().endswith(".eml") else filename
        invalid_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name.strip(". ")

    @staticmethod
    def sanitize_attachment_filename(filename):
        """
        Sanitize attachment filename to prevent directory creation.
        Replaces path separators and other problematic characters.
        """
        if not filename:
            return "unnamed_attachment"

        # Replace path separators (most common issue)
        safe_name = filename.replace("\\", "_").replace("/", "_")

        # Replace other invalid characters
        invalid_chars = [":", "*", "?", '"', "<", ">", "|"]
        for char in invalid_chars:
            safe_name = safe_name.replace(char, "_")

        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(". ")

        # If filename is empty after sanitization, use default
        if not safe_name:
            safe_name = "unnamed_attachment"

        return safe_name

    def extract_single_email(self, eml_path, output_folder):
        """Extract a single .eml file to a folder."""
        # Load email
        with open(eml_path, "rb") as f:
            message = BytesParser(policy=policy.default).parse(f)

        # Create output folder
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        # Extract headers
        headers = {
            "From": message.get("From", "N/A"),
            "To": message.get("To", "N/A"),
            "Subject": message.get("Subject", "N/A"),
            "Date": message.get("Date", "N/A"),
            "Cc": message.get("Cc", "N/A"),
            "Message-ID": message.get("Message-ID", "N/A"),
        }

        # Save headers
        with open(output_path / "headers.txt", "w", encoding="utf-8") as f:
            for key, value in headers.items():
                f.write(f"{key}: {value}\n")

        # Extract body
        plain_body = None
        html_body = None
        attachments = []

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # Handle attachments
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(
                            {
                                "filename": filename,
                                "content": part.get_payload(decode=True),
                            }
                        )
                # Handle body content
                elif content_type == "text/plain" and plain_body is None:
                    plain_body = part.get_content()
                elif content_type == "text/html" and html_body is None:
                    html_body = part.get_content()
        else:
            content_type = message.get_content_type()
            if content_type == "text/plain":
                plain_body = message.get_content()
            elif content_type == "text/html":
                html_body = message.get_content()

        # Save body
        if plain_body:
            with open(output_path / "body_plain.txt", "w", encoding="utf-8") as f:
                f.write(plain_body)

        if html_body:
            with open(output_path / "body_html.html", "w", encoding="utf-8") as f:
                f.write(html_body)

        # Save attachments with sanitized filenames
        if attachments:
            attachments_dir = output_path / "attachments"
            attachments_dir.mkdir(exist_ok=True)

            for att in attachments:
                # Sanitize the attachment filename
                safe_filename = self.sanitize_attachment_filename(att["filename"])
                filepath = attachments_dir / safe_filename

                # Handle duplicate filenames
                counter = 1
                original_safe_name = safe_filename
                while filepath.exists():
                    name, ext = os.path.splitext(original_safe_name)
                    filepath = attachments_dir / f"{name}_{counter}{ext}"
                    counter += 1

                # Save the attachment
                try:
                    with open(filepath, "wb") as f:
                        f.write(att["content"])
                except Exception as e:
                    print(
                        f"  ⚠ Warning: Could not save attachment '{att['filename']}': {e}"
                    )

        return {
            "headers": headers,
            "has_plain": plain_body is not None,
            "has_html": html_body is not None,
            "attachment_count": len(attachments),
        }

    def process_all(self):
        """Process all .eml files in the input folder."""
        # Check input folder
        if not self.input_folder.exists():
            print(f"✗ Error: Folder not found - {self.input_folder}")
            return

        # Find all .eml files
        eml_files = list(self.input_folder.glob("*.eml"))

        if not eml_files:
            print(f"✗ No .eml files found in {self.input_folder}")
            return

        self.stats["total"] = len(eml_files)

        print(f"\n{'=' * 70}")
        print("BATCH EML EXTRACTION")
        print(f"{'=' * 70}")
        print(f"Input folder: {self.input_folder.absolute()}")
        print(f"Output folder: {self.output_base.absolute()}")
        print(f"Found {len(eml_files)} .eml file(s)")
        print(f"{'=' * 70}\n")

        # Create output base folder
        self.output_base.mkdir(exist_ok=True)

        # Process each file
        for idx, eml_file in enumerate(eml_files, 1):
            print(f"[{idx}/{len(eml_files)}] Processing: {eml_file.name}")
            print("-" * 70)

            try:
                # Create output folder name
                folder_name = self.sanitize_folder_name(eml_file.name)
                output_folder = self.output_base / folder_name

                # Handle duplicate folder names
                counter = 1
                original_name = folder_name
                while output_folder.exists():
                    folder_name = f"{original_name}_{counter}"
                    output_folder = self.output_base / folder_name
                    counter += 1

                # Extract the email
                info = self.extract_single_email(eml_file, output_folder)

                # Print summary
                print(f"From: {info['headers']['From']}")
                print(f"Subject: {info['headers']['Subject']}")
                print(f"Date: {info['headers']['Date']}")
                print(f"Plain text body: {'✓' if info['has_plain'] else '✗'}")
                print(f"HTML body: {'✓' if info['has_html'] else '✗'}")
                print(f"Attachments: {info['attachment_count']}")
                print(f"✓ Extracted to: {output_folder.name}/")

                self.stats["successful"] += 1

            except Exception as e:
                print(f"✗ Error: {e}")
                self.stats["failed"] += 1

            print()

        # Print final summary
        self.print_summary()

    def print_summary(self):
        """Print extraction summary."""
        print(f"{'=' * 70}")
        print("EXTRACTION COMPLETE")
        print(f"{'=' * 70}")
        print(f"Total files: {self.stats['total']}")
        print(f"Successful: {self.stats['successful']} ✓")
        print(f"Failed: {self.stats['failed']} ✗")
        print(f"\nAll content saved to: {self.output_base.absolute()}")
        print(f"{'=' * 70}\n")


def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("STANDALONE BATCH EML EXTRACTOR v2.0")
    print("(With improved filename sanitization)")
    print("=" * 70)

    if len(sys.argv) < 2:
        print(
            "\nUsage: python batch_extract_standalone.py <input_folder> [output_folder]"
        )
        print("\nArguments:")
        print("  input_folder   - Folder containing .eml files (required)")
        print("  output_folder  - Base folder for output (default: extracted_emails)")
        print("\nExample:")
        print("  python batch_extract_standalone.py my_emails/")
        print("  python batch_extract_standalone.py my_emails/ output/")
        print("\nFeatures:")
        print("  ✓ Handles attachments with path separators (e.g., 'folder\\file.pdf')")
        print("  ✓ Sanitizes all problematic characters")
        print("  ✓ Prevents 'file not found' errors")
        print("\nOutput structure:")
        print("  output_folder/")
        print("  ├── email_1/")
        print("  │   ├── headers.txt")
        print("  │   ├── body_plain.txt")
        print("  │   ├── body_html.html")
        print("  │   └── attachments/")
        print("  │       └── company_materials_file.pdf  (sanitized)")
        print("  ├── email_2/")
        print("  └── ...")
        print("=" * 70 + "\n")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "extracted_emails"

    processor = EMLBatchProcessor(input_folder, output_folder)
    processor.process_all()


if __name__ == "__main__":
    main()
