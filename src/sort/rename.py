import os
import glob
from pathlib import Path
import time
import argparse
import re
from datetime import datetime

def rename_png_files_by_creation_time(root_path, recursive=False, prefix="", start_number=1):
    """
    Rename PNG files based on their creation timestamp.
    The earliest created file gets the lowest number (1), latest gets highest number.
    Args:
        root_path: The root directory to search for PNG files
        recursive: If True, search subdirectories recursively
        prefix: Optional prefix to add before the number
        start_number: Starting number for renaming (default: 1)
    """
    # Get all PNG files
    if recursive:
        pattern = os.path.join(root_path, "**", "*.png")
        png_files = glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(root_path, "*.png")
        png_files = glob.glob(pattern)
    
    if not png_files:
        print(f"No PNG files found in {root_path}")
        return
    
    # Get creation times and sort files by creation time (earliest first)
    files_with_times = []
    for file_path in png_files:
        try:
            # Get creation time (birth time on macOS)
            creation_time = os.path.getctime(file_path)
            files_with_times.append((file_path, creation_time, os.path.basename(file_path)))
        except OSError as e:
            print(f"Error getting creation time for {file_path}: {e}")
            continue
    
    if not files_with_times:
        print(f"No files with valid creation times found in {root_path}")
        return
    
    # Sort by creation time (earliest first)
    files_with_times.sort(key=lambda x: x[1])
    
    total_files = len(files_with_times)
    print(f"Found {total_files} PNG files in {root_path}")
    
    # Rename files with ascending numbering (earliest created gets 1)
    for i, (file_path, creation_time, original_filename) in enumerate(files_with_times):
        # Calculate the new number (earliest created file gets 1)
        new_number = i + start_number
        
        # Get file extension
        file_ext = os.path.splitext(file_path)[1]
        
        # Create new filename
        new_filename = f"{prefix}{new_number}{file_ext}"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        
        # Handle filename conflicts
        counter = 1
        original_new_file_path = new_file_path
        while os.path.exists(new_file_path):
            name_without_ext = os.path.splitext(original_new_file_path)[0]
            new_file_path = f"{name_without_ext}_{counter}{file_ext}"
            counter += 1
        
        try:
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {original_filename} → {os.path.basename(new_file_path)} (created: {datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')})")
        except OSError as e:
            print(f"Error renaming {file_path}: {e}")
    
    print(f"Successfully renamed {total_files} files in {root_path}\n")

def main():
    parser = argparse.ArgumentParser(description="Rename PNG files by creation timestamp (earliest created is 1, etc.)")
    parser.add_argument("path", nargs="?", default=".", help="Path to directory containing PNG files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search subdirectories recursively")
    parser.add_argument("-p", "--prefix", default="", help="Prefix to add before the number")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be renamed without actually renaming")

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        return

    if args.dry_run:
        print("DRY RUN MODE - No files will be renamed")
        print(f"Would process PNG files in: {args.path}")
        if args.recursive:
            print("Would search subdirectories recursively")
        print(f"Would use prefix: '{args.prefix}'")
        print("Would number files so that the earliest created is 1, next is 2, etc.")
        return

    rename_png_files_by_creation_time(args.path, args.recursive, args.prefix)

# List of directories that need to be sorted
list_needed_to_be_handled = [
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2022/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2021/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2019/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2018/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2017/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2016/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2015/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2014/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2013/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/phys/2012/photo", 
]

if __name__ == "__main__":
    # Process all directories in the list
    for dir_path in list_needed_to_be_handled:
        if not os.path.exists(dir_path):
            print(f"Directory does not exist: {dir_path}")
            continue
        print(f"\nProcessing directory: {dir_path}")
        # You can adjust the arguments as needed (recursive, prefix, start_number)
        rename_png_files_by_creation_time(dir_path, recursive=False, prefix="", start_number=1)