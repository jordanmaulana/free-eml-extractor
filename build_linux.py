#!/usr/bin/env python3
"""
Build script for Linux executable
Creates standalone executables for both GUI and CLI versions
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"])
        print("✓ PyInstaller installed successfully")

def build_executable():
    """Build Linux executables"""
    print("\n" + "="*60)
    print("BUILDING LINUX EXECUTABLES")
    print("="*60)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Clean previous builds
    dist_dir = Path("dist")
    build_dir = Path("build")
    spec_dir = Path("spec")
    
    for dir_path in [dist_dir, build_dir, spec_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✓ Cleaned {dir_path}")
    
    # Build GUI executable
    print("\nBuilding GUI executable...")
    gui_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=eml-extractor-gui",
        "--icon=NONE",
        "--distpath=dist/linux",
        "--workpath=build/linux",
        "--specpath=spec/linux",
        "gui.py"
    ]
    
    try:
        subprocess.check_call(gui_cmd)
        print("✓ GUI executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ GUI build failed: {e}")
        return False
    
    # Build CLI executable
    print("\nBuilding CLI executable...")
    cli_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=eml-extractor-cli",
        "--icon=NONE",
        "--distpath=dist/linux",
        "--workpath=build/linux",
        "--specpath=spec/linux",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cli_cmd)
        print("✓ CLI executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ CLI build failed: {e}")
        return False
    
    # Create output directory with proper structure
    output_dir = Path("dist/linux/EML_Extractor")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executables
    gui_exe = Path("dist/linux/eml-extractor-gui")
    cli_exe = Path("dist/linux/eml-extractor-cli")
    
    if gui_exe.exists():
        shutil.copy2(gui_exe, output_dir / "eml-extractor-gui")
        # Make executable
        os.chmod(output_dir / "eml-extractor-gui", 0o755)
        print(f"✓ Copied GUI executable to {output_dir}")
    
    if cli_exe.exists():
        shutil.copy2(cli_exe, output_dir / "eml-extractor-cli")
        # Make executable
        os.chmod(output_dir / "eml-extractor-cli", 0o755)
        print(f"✓ Copied CLI executable to {output_dir}")
    
    # Create desktop entry for GUI
    desktop_entry = """[Desktop Entry]
Version=1.0
Type=Application
Name=EML Extractor
Comment=Batch extract .eml files with attachments
Exec=eml-extractor-gui
Icon=application-x-eml
Terminal=false
Categories=Office;Utility;
MimeType=application/x-eml;
"""
    
    with open(output_dir / "eml-extractor.desktop", "w", encoding="utf-8") as f:
        f.write(desktop_entry)
    
    # Create installation script
    install_script = """#!/bin/bash
# Installation script for EML Extractor

set -e

INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Create directories if they don't exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"

# Install executables
echo "Installing executables to $INSTALL_DIR..."
cp eml-extractor-gui "$INSTALL_DIR/"
cp eml-extractor-cli "$INSTALL_DIR/"

# Install desktop entry
echo "Installing desktop entry..."
cp eml-extractor.desktop "$DESKTOP_DIR/"

# Update desktop database
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "Installation complete!"
echo "You can now run 'eml-extractor-gui' from the terminal or find it in your applications menu."
"""
    
    with open(output_dir / "install.sh", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    # Make install script executable
    os.chmod(output_dir / "install.sh", 0o755)
    
    # Create README for the package
    readme_content = """# EML Extractor - Linux Version

## Files
- **eml-extractor-gui**: Graphical user interface version (recommended)
- **eml-extractor-cli**: Command line interface version
- **eml-extractor.desktop**: Desktop entry file
- **install.sh**: Installation script

## Quick Install

Run the installation script:
```bash
./install.sh
```

This will install the executables to ~/.local/bin and add a desktop entry.

## Manual Install

### GUI Version
```bash
cp eml-extractor-gui ~/.local/bin/
chmod +x ~/.local/bin/eml-extractor-gui
```

Then run from terminal:
```bash
eml-extractor-gui
```

### CLI Version
```bash
cp eml-extractor-cli ~/.local/bin/
chmod +x ~/.local/bin/eml-extractor-cli
```

Then run from terminal:
```bash
eml-extractor-cli <input_folder> [output_folder]
```

## Requirements
- Linux with X11 or Wayland
- Python 3.8+ (embedded in executable)
- Tkinter (usually included with Python)

## Features
- Batch extract .eml files
- Extract attachments, headers, and body content
- Safe filename handling
- Modern GUI with progress tracking
- Desktop integration
"""
    
    with open(output_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n✓ Linux executables created in: {output_dir.absolute()}")
    print(f"  - eml-extractor-gui: {gui_exe.stat().st_size / (1024*1024):.1f} MB")
    print(f"  - eml-extractor-cli: {cli_exe.stat().st_size / (1024*1024):.1f} MB")
    print(f"  - Installation script: install.sh")
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n✓ Build completed successfully!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)
