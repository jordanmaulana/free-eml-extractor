#!/usr/bin/env python3
"""
Build script for Windows executable
Creates standalone .exe files for both GUI and CLI versions
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
    """Build Windows executables"""
    print("\n" + "="*60)
    print("BUILDING WINDOWS EXECUTABLES")
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
        "--windowed",
        "--name=EMLExtractorGUI",
        "--icon=NONE",
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=spec/windows",
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
        "--console",
        "--name=EMLExtractorCLI",
        "--icon=NONE",
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=spec/windows",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cli_cmd)
        print("✓ CLI executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ CLI build failed: {e}")
        return False
    
    # Create output directory with proper structure
    output_dir = Path("dist/windows/EML_Extractor")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executables
    gui_exe = Path("dist/windows/EMLExtractorGUI.exe")
    cli_exe = Path("dist/windows/EMLExtractorCLI.exe")
    
    if gui_exe.exists():
        shutil.copy2(gui_exe, output_dir / "EMLExtractorGUI.exe")
        print(f"✓ Copied GUI executable to {output_dir}")
    
    if cli_exe.exists():
        shutil.copy2(cli_exe, output_dir / "EMLExtractorCLI.exe")
        print(f"✓ Copied CLI executable to {output_dir}")
    
    # Create README for the package
    readme_content = """# EML Extractor - Windows Version

## Files
- **EMLExtractorGUI.exe**: Graphical user interface version (recommended)
- **EMLExtractorCLI.exe**: Command line interface version

## Usage

### GUI Version
Double-click `EMLExtractorGUI.exe` to launch the graphical interface.

### CLI Version
Open Command Prompt and run:
```
EMLExtractorCLI.exe <input_folder> [output_folder]
```

## Requirements
- Windows 10 or later
- No additional dependencies required

## Features
- Batch extract .eml files
- Extract attachments, headers, and body content
- Safe filename handling
- Modern GUI with progress tracking
"""
    
    with open(output_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n✓ Windows executables created in: {output_dir.absolute()}")
    print(f"  - EMLExtractorGUI.exe: {gui_exe.stat().st_size / (1024*1024):.1f} MB")
    print(f"  - EMLExtractorCLI.exe: {cli_exe.stat().st_size / (1024*1024):.1f} MB")
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n✓ Build completed successfully!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)
