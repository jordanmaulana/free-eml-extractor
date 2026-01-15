#!/usr/bin/env python3
"""
Modern GUI for EML Batch Extractor
A user-friendly interface for batch processing .eml files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
from main import EMLBatchProcessor


class EMLExtractorGUI:
    """Modern GUI for EML Batch Extractor"""

    def __init__(self, root):
        self.root = root
        self.root.title("EML Batch Extractor")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar(value="extracted_emails")
        self.is_processing = False
        self.progress_queue = queue.Queue()

        # Create UI
        self.create_widgets()
        self.setup_layout()

        # Start queue checker
        self.root.after(100, self.check_queue)

    def create_widgets(self):
        """Create all UI widgets"""

        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")

        # Title
        title_label = ttk.Label(
            self.main_frame, text="EML Batch Extractor", font=("Arial", 16, "bold")
        )

        # Input section
        input_frame = ttk.LabelFrame(
            self.main_frame, text="Input Settings", padding="10"
        )

        ttk.Label(input_frame, text="Input Folder:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.input_entry = ttk.Entry(
            input_frame, textvariable=self.input_folder, width=50
        )
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.input_browse_btn = ttk.Button(
            input_frame, text="Browse...", command=self.browse_input_folder
        )
        self.input_browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Output section
        output_frame = ttk.LabelFrame(
            self.main_frame, text="Output Settings", padding="10"
        )

        ttk.Label(output_frame, text="Output Folder:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.output_entry = ttk.Entry(
            output_frame, textvariable=self.output_folder, width=50
        )
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.output_browse_btn = ttk.Button(
            output_frame, text="Browse...", command=self.browse_output_folder
        )
        self.output_browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Control buttons
        control_frame = ttk.Frame(self.main_frame)

        self.start_btn = ttk.Button(
            control_frame,
            text="Start Extraction",
            command=self.start_extraction,
            style="Accent.TButton",
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(
            control_frame, text="Stop", command=self.stop_extraction, state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(
            control_frame, text="Clear Log", command=self.clear_log
        )
        self.clear_btn.pack(side="left", padx=5)

        # Progress section
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.pack(fill="x", pady=5)

        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(anchor="w")

        self.stats_label = ttk.Label(progress_frame, text="")
        self.stats_label.pack(anchor="w")

        # Log section
        log_frame = ttk.LabelFrame(self.main_frame, text="Processing Log", padding="10")

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=15, width=80, wrap=tk.WORD, font=("Consolas", 9)
        )
        self.log_text.pack(fill="both", expand=True)

        # Store widgets for layout
        self.widgets = {
            "title": title_label,
            "input_frame": input_frame,
            "output_frame": output_frame,
            "control_frame": control_frame,
            "progress_frame": progress_frame,
            "log_frame": log_frame,
        }

    def setup_layout(self):
        """Setup the layout of all widgets"""
        self.main_frame.pack(fill="both", expand=True)

        # Title
        self.widgets["title"].pack(pady=(0, 10))

        # Input and output frames
        self.widgets["input_frame"].pack(fill="x", pady=5)
        self.widgets["output_frame"].pack(fill="x", pady=5)

        # Configure grid weights
        self.widgets["input_frame"].columnconfigure(1, weight=1)
        self.widgets["output_frame"].columnconfigure(1, weight=1)

        # Control buttons
        self.widgets["control_frame"].pack(pady=10)

        # Progress
        self.widgets["progress_frame"].pack(fill="x", pady=5)

        # Log
        self.widgets["log_frame"].pack(fill="both", expand=True, pady=5)

    def browse_input_folder(self):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)

    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def log_message(self, message, level="info"):
        """Add message to log with color coding"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

        # Color coding based on level
        if level == "error":
            # Color last line red
            line_start = self.log_text.index("end-2c linestart")
            line_end = self.log_text.index("end-1c")
            self.log_text.tag_add("error", line_start, line_end)
            self.log_text.tag_config("error", foreground="red")
        elif level == "success":
            # Color last line green
            line_start = self.log_text.index("end-2c linestart")
            line_end = self.log_text.index("end-1c")
            self.log_text.tag_add("success", line_start, line_end)
            self.log_text.tag_config("success", foreground="green")
        elif level == "warning":
            # Color last line orange
            line_start = self.log_text.index("end-2c linestart")
            line_end = self.log_text.index("end-1c")
            self.log_text.tag_add("warning", line_start, line_end)
            self.log_text.tag_config("warning", foreground="orange")

    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)

    def start_extraction(self):
        """Start the extraction process"""
        input_path = self.input_folder.get().strip()
        output_path = self.output_folder.get().strip()

        # Validation
        if not input_path:
            messagebox.showerror("Error", "Please select an input folder")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"Input folder does not exist: {input_path}")
            return

        if not output_path:
            messagebox.showerror("Error", "Please specify an output folder")
            return

        # Update UI state
        self.is_processing = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.input_browse_btn.config(state="disabled")
        self.output_browse_btn.config(state="disabled")

        # Clear previous log and reset progress
        self.clear_log()
        self.progress_var.set(0)
        self.status_label.config(text="Starting extraction...")
        self.stats_label.config(text="")

        # Start processing in separate thread
        thread = threading.Thread(
            target=self.process_emails, args=(input_path, output_path)
        )
        thread.daemon = True
        thread.start()

    def stop_extraction(self):
        """Stop the extraction process"""
        self.is_processing = False
        self.log_message("Extraction stopped by user", "warning")
        self.reset_ui_state()

    def reset_ui_state(self):
        """Reset UI to initial state"""
        self.is_processing = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.input_browse_btn.config(state="normal")
        self.output_browse_btn.config(state="normal")
        self.status_label.config(text="Ready")

    def process_emails(self, input_folder, output_folder):
        """Process emails in background thread"""
        try:
            # Create processor
            processor = EMLBatchProcessor(input_folder, output_folder)

            # Check input folder
            if not processor.input_folder.exists():
                self.progress_queue.put(
                    ("error", f"✗ Error: Folder not found - {processor.input_folder}")
                )
                return

            # Find all .eml files
            eml_files = list(processor.input_folder.glob("*.eml"))

            if not eml_files:
                self.progress_queue.put(
                    ("error", f"✗ No .eml files found in {processor.input_folder}")
                )
                return

            total_files = len(eml_files)
            self.progress_queue.put(("info", f"\n{'=' * 70}"))
            self.progress_queue.put(("info", "BATCH EML EXTRACTION"))
            self.progress_queue.put(("info", f"{'=' * 70}"))
            self.progress_queue.put(
                ("info", f"Input folder: {processor.input_folder.absolute()}")
            )
            self.progress_queue.put(
                ("info", f"Output folder: {processor.output_base.absolute()}")
            )
            self.progress_queue.put(("info", f"Found {total_files} .eml file(s)"))
            self.progress_queue.put(("info", f"{'=' * 70}\n"))

            # Create output base folder
            processor.output_base.mkdir(exist_ok=True)

            # Process each file
            successful = 0
            failed = 0

            for idx, eml_file in enumerate(eml_files, 1):
                if not self.is_processing:
                    break

                self.progress_queue.put(
                    ("info", f"[{idx}/{total_files}] Processing: {eml_file.name}")
                )
                self.progress_queue.put(("info", "-" * 70))

                try:
                    # Create output folder name
                    folder_name = processor.sanitize_folder_name(eml_file.name)
                    output_folder_path = processor.output_base / folder_name

                    # Handle duplicate folder names
                    counter = 1
                    original_name = folder_name
                    while output_folder_path.exists():
                        folder_name = f"{original_name}_{counter}"
                        output_folder_path = processor.output_base / folder_name
                        counter += 1

                    # Extract the email
                    info = processor.extract_single_email(eml_file, output_folder_path)

                    # Print summary
                    self.progress_queue.put(
                        ("info", f"From: {info['headers']['From']}")
                    )
                    self.progress_queue.put(
                        ("info", f"Subject: {info['headers']['Subject']}")
                    )
                    self.progress_queue.put(
                        ("info", f"Date: {info['headers']['Date']}")
                    )
                    self.progress_queue.put(
                        (
                            "success",
                            f"Plain text body: {'✓' if info['has_plain'] else '✗'}",
                        )
                    )
                    self.progress_queue.put(
                        ("success", f"HTML body: {'✓' if info['has_html'] else '✗'}")
                    )
                    self.progress_queue.put(
                        ("info", f"Attachments: {info['attachment_count']}")
                    )
                    self.progress_queue.put(
                        ("success", f"✓ Extracted to: {output_folder_path.name}/")
                    )

                    successful += 1

                except Exception as e:
                    self.progress_queue.put(("error", f"✗ Error: {e}"))
                    failed += 1

                # Update progress
                progress = (idx / total_files) * 100
                self.progress_queue.put(("progress", progress))
                self.progress_queue.put(
                    ("status", f"Processing {idx}/{total_files}...")
                )
                self.progress_queue.put(
                    ("stats", f"Successful: {successful} | Failed: {failed}")
                )

                self.progress_queue.put(("info", ""))

            # Final summary
            self.progress_queue.put(("info", f"{'=' * 70}"))
            self.progress_queue.put(("info", "EXTRACTION COMPLETE"))
            self.progress_queue.put(("info", f"{'=' * 70}"))
            self.progress_queue.put(("info", f"Total files: {total_files}"))
            self.progress_queue.put(("success", f"Successful: {successful} ✓"))
            if failed > 0:
                self.progress_queue.put(("error", f"Failed: {failed} ✗"))
            self.progress_queue.put(
                ("info", f"\nAll content saved to: {processor.output_base.absolute()}")
            )
            self.progress_queue.put(("info", f"{'=' * 70}\n"))

            self.progress_queue.put(("complete", None))

        except Exception as e:
            self.progress_queue.put(("error", f"Unexpected error: {e}"))
            self.progress_queue.put(("complete", None))

    def check_queue(self):
        """Check for messages from background thread"""
        try:
            while True:
                msg_type, msg_data = self.progress_queue.get_nowait()

                if msg_type == "info":
                    self.log_message(msg_data)
                elif msg_type == "error":
                    self.log_message(msg_data, "error")
                elif msg_type == "success":
                    self.log_message(msg_data, "success")
                elif msg_type == "warning":
                    self.log_message(msg_data, "warning")
                elif msg_type == "progress":
                    self.progress_var.set(msg_data)
                elif msg_type == "status":
                    self.status_label.config(text=msg_data)
                elif msg_type == "stats":
                    self.stats_label.config(text=msg_data)
                elif msg_type == "complete":
                    self.reset_ui_state()
                    if msg_data is None:
                        self.status_label.config(text="Extraction complete!")
                    break

        except queue.Empty:
            pass

        # Continue checking
        self.root.after(100, self.check_queue)


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = EMLExtractorGUI(root)

    # Handle window closing
    def on_closing():
        if app.is_processing:
            if messagebox.askokcancel(
                "Quit", "Extraction is in progress. Are you sure you want to quit?"
            ):
                app.is_processing = False
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
