import os
import glob
from pathlib import Path
import time
import argparse


def rename_png_files_recursive(root_path, recursive=False, prefix="", start_number=1):
    """
    Rename PNG files based on their creation timestamp.
    
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
    
    # Get creation times and sort files by creation time
    files_with_times = []
    for file_path in png_files:
        try:
            # Get creation time (birth time on macOS)
            creation_time = os.path.getctime(file_path)
            files_with_times.append((file_path, creation_time))
        except OSError as e:
            print(f"Error getting creation time for {file_path}: {e}")
            continue
    
    # Sort by creation time (earliest first)
    files_with_times.sort(key=lambda x: x[1])
    
    # Group files by directory
    files_by_directory = {}
    for file_path, creation_time in files_with_times:
        directory = os.path.dirname(file_path)
        if directory not in files_by_directory:
            files_by_directory[directory] = []
        files_by_directory[directory].append((file_path, creation_time))
    
    total_renamed = 0
    
    # Process each directory separately
    for directory, files in files_by_directory.items():
        print(f"\nProcessing directory: {directory}")
        
        # Sort files in this directory by creation time
        files.sort(key=lambda x: x[1])
        
        # Rename files with sequential numbers
        for index, (file_path, creation_time) in enumerate(files, start_number):
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            # Create new filename with number
            new_filename = f"{prefix}{index}{ext}"
            new_file_path = os.path.join(directory, new_filename)
            
            # Check if target filename already exists
            counter = 1
            original_new_file_path = new_file_path
            while os.path.exists(new_file_path):
                name_without_ext = os.path.splitext(original_new_file_path)[0]
                ext = os.path.splitext(original_new_file_path)[1]
                new_file_path = f"{name_without_ext}_{counter}{ext}"
                counter += 1
            
            try:
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"  Renamed: {filename} -> {os.path.basename(new_file_path)}")
                total_renamed += 1
            except OSError as e:
                print(f"  Error renaming {filename}: {e}")
    
    print(f"\nTotal: Renamed {total_renamed} PNG files")


def main():
    parser = argparse.ArgumentParser(description="Rename PNG files by creation timestamp")
    parser.add_argument("path", nargs="?", default=".", help="Path to directory containing PNG files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search subdirectories recursively")
    parser.add_argument("-p", "--prefix", default="", help="Prefix to add before the number")
    parser.add_argument("-s", "--start", type=int, default=1, help="Starting number for renaming")
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
        print(f"Would start numbering from: {args.start}")
        return
    
    rename_png_files_recursive(args.path, args.recursive, args.prefix, args.start)
    
# List of directories that need to be sorted/handled
list_needed_to_be_handled = [
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2022/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2021/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2019/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2018/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2017/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2016/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2015/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2014/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2013/photo", 
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2012/photo", 
]

# Example usage: process all directories in the list
if __name__ == "__main__":
    for dir_path in list_needed_to_be_handled:
        if not os.path.exists(dir_path):
            print(f"Directory does not exist: {dir_path}")
            continue
        print(f"\nProcessing directory: {dir_path}")
        # You can adjust the arguments as needed (recursive, prefix, start_number)
        rename_png_files_recursive(dir_path, recursive=False, prefix="", start_number=1)