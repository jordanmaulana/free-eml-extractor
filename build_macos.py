#!/usr/bin/env python3
"""
Build script for macOS executable
Creates standalone .app bundle and command line executable
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
    """Build macOS executables"""
    print("\n" + "="*60)
    print("BUILDING MACOS EXECUTABLES")
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
    
    # Build GUI app bundle
    print("\nBuilding GUI app bundle...")
    gui_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=EML Extractor",
        "--icon=NONE",
        "--distpath=dist/macos",
        "--workpath=build/macos",
        "--specpath=spec/macos",
        "gui.py"
    ]
    
    try:
        subprocess.check_call(gui_cmd)
        print("✓ GUI app bundle built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ GUI build failed: {e}")
        return False
    
    # Build CLI executable
    print("\nBuilding CLI executable...")
    cli_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name=eml-extractor-cli",
        "--icon=NONE",
        "--distpath=dist/macos",
        "--workpath=build/macos",
        "--specpath=spec/macos",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cli_cmd)
        print("✓ CLI executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ CLI build failed: {e}")
        return False
    
    # Create output directory with proper structure
    output_dir = Path("dist/macos/EML_Extractor")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy app bundle
    gui_app = Path("dist/macos/EML Extractor.app")
    if gui_app.exists():
        shutil.copytree(gui_app, output_dir / "EML Extractor.app", dirs_exist_ok=True)
        print(f"✓ Copied GUI app to {output_dir}")
    
    # Copy CLI executable
    cli_exe = Path("dist/macos/eml-extractor-cli")
    if cli_exe.exists():
        shutil.copy2(cli_exe, output_dir / "eml-extractor-cli")
        # Make executable
        os.chmod(output_dir / "eml-extractor-cli", 0o755)
        print(f"✓ Copied CLI executable to {output_dir}")
    
    # Create README for the package
    readme_content = """# EML Extractor - macOS Version

## Files
- **EML Extractor.app**: Graphical user interface version (recommended)
- **eml-extractor-cli**: Command line interface version

## Usage

### GUI Version
Double-click `EML Extractor.app` to launch the graphical interface.

### CLI Version
Open Terminal and run:
```
./eml-extractor-cli <input_folder> [output_folder]
```

## Requirements
- macOS 10.14 (Mojave) or later
- No additional dependencies required

## Features
- Batch extract .eml files
- Extract attachments, headers, and body content
- Safe filename handling
- Modern GUI with progress tracking
- Native macOS app bundle
"""
    
    with open(output_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Get file sizes
    gui_size = 0
    cli_size = 0
    
    if gui_app.exists():
        gui_size = sum(f.stat().st_size for f in gui_app.rglob('*') if f.is_file()) / (1024*1024)
    
    if cli_exe.exists():
        cli_size = cli_exe.stat().st_size / (1024*1024)
    
    print(f"\n✓ macOS executables created in: {output_dir.absolute()}")
    print(f"  - EML Extractor.app: {gui_size:.1f} MB")
    print(f"  - eml-extractor-cli: {cli_size:.1f} MB")
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n✓ Build completed successfully!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)
