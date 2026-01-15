#!/usr/bin/env python3
"""
Universal build script for EML Extractor
Detects platform and builds appropriate executables
"""

import platform
import subprocess
import sys
from pathlib import Path


def detect_platform():
    """Detect the current platform"""
    system = platform.system().lower()

    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        print(f"Unsupported platform: {system}")
        return None


def build_for_platform(platform_name):
    """Build executables for the specified platform"""
    print(f"Building for platform: {platform_name}")

    build_scripts = {
        "windows": "build_windows.py",
        "macos": "build_macos.py",
        "linux": "build_linux.py",
    }

    script_path = build_scripts.get(platform_name)
    if not script_path:
        print(f"No build script available for platform: {platform_name}")
        return False

    if not Path(script_path).exists():
        print(f"Build script not found: {script_path}")
        return False

    try:
        print(f"Running {script_path}...")
        subprocess.check_call([sys.executable, script_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False


def build_all():
    """Build executables for all platforms (cross-platform build)"""
    print("\n" + "=" * 60)
    print("CROSS-PLATFORM BUILD")
    print("=" * 60)
    print("Note: This will attempt to build for all platforms.")
    print("Some builds may fail if you're not on the target platform.")
    print()

    platforms = ["windows", "macos", "linux"]
    results = {}

    for platform_name in platforms:
        print(f"\n{'-' * 40}")
        print(f"Building for {platform_name.upper()}")
        print(f"{'-' * 40}")

        success = build_for_platform(platform_name)
        results[platform_name] = success

        if success:
            print(f"✓ {platform_name} build completed")
        else:
            print(f"✗ {platform_name} build failed")

    # Summary
    print(f"\n{'=' * 60}")
    print("BUILD SUMMARY")
    print(f"{'=' * 60}")

    for platform_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{platform_name.upper():10} : {status}")

    total_success = sum(results.values())
    print(f"\nTotal: {total_success}/{len(platforms)} platforms built successfully")

    return total_success > 0


def main():
    """Main build function"""
    print("EML Extractor - Universal Build Script")
    print("=" * 60)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "all":
            success = build_all()
        elif command in ["windows", "macos", "linux"]:
            success = build_for_platform(command)
        else:
            print(f"Unknown command: {command}")
            print_usage()
            return
    else:
        # Auto-detect platform
        platform_name = detect_platform()
        if platform_name:
            success = build_for_platform(platform_name)
        else:
            success = False

    if success:
        print("\n✓ Build completed successfully!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)


def print_usage():
    """Print usage information"""
    print("\nUsage:")
    print("  python build.py              # Auto-detect platform and build")
    print("  python build.py windows     # Build Windows executables")
    print("  python build.py macos       # Build macOS executables")
    print("  python build.py linux       # Build Linux executables")
    print("  python build.py all         # Build for all platforms")


if __name__ == "__main__":
    main()
