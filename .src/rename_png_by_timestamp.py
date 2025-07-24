import os
import glob
from pathlib import Path
import time


def rename_png_files_by_timestamp(folder_path):
    """
    Rename PNG files in the given folder based on their creation timestamp.
    Files created earlier get lower numbers (1, 2, 3, etc.).
    """
    # Get all PNG files in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    
    if not png_files:
        print(f"No PNG files found in {folder_path}")
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
    
    # Rename files with sequential numbers
    for index, (file_path, creation_time) in enumerate(files_with_times, 1):
        # Get the directory and file extension
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        # Create new filename with number
        new_filename = f"{index}{ext}"
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
            print(f"Renamed: {filename} -> {os.path.basename(new_file_path)}")
        except OSError as e:
            print(f"Error renaming {filename}: {e}")
    
    print(f"\nRenamed {len(files_with_times)} PNG files in {folder_path}")


if __name__ == "__main__":
    # You can change this to your desired folder path
    folder_path = "/Users/matthewng/Desktop/-dse.life-past-paper-collection"
    
    # Ask user for folder path
    user_path = input(f"Enter folder path (or press Enter to use default: {folder_path}): ").strip()
    if user_path:
        folder_path = user_path
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
    else:
        rename_png_files_by_timestamp(folder_path) 