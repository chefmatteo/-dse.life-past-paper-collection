import os
import glob
import re

def clean_png_filenames(folder_path):
    """
    Clean PNG filenames by removing _1 suffixes and ensuring clean numeric names.
    """
    # Get all PNG files in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    
    if not png_files:
        print(f"No PNG files found in {folder_path}")
        return
    
    print(f"Found {len(png_files)} PNG files in {folder_path}")
    
    # Process each file
    for file_path in png_files:
        filename = os.path.basename(file_path)
        directory = os.path.dirname(file_path)
        
        # Extract the number from the filename
        # Match patterns like: 1_1.png, 2_1.png, 45_1.png, etc.
        match = re.match(r'(\d+)_1\.png$', filename)
        
        if match:
            # Extract the number and create clean filename
            number = match.group(1)
            new_filename = f"{number}.png"
            new_file_path = os.path.join(directory, new_filename)
            
            # Check if the target filename already exists
            if os.path.exists(new_file_path):
                print(f"Warning: {new_filename} already exists, skipping {filename}")
                continue
            
            try:
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} → {new_filename}")
            except OSError as e:
                print(f"Error renaming {filename}: {e}")
        else:
            # Check if it's already a clean numeric filename
            clean_match = re.match(r'^\d+\.png$', filename)
            if clean_match:
                print(f"Already clean: {filename}")
            else:
                print(f"Unexpected filename format: {filename}")
    
    print(f"Finished cleaning filenames in {folder_path}\n")

def main():
    """
    Main function to clean PNG filenames in multiple directories.
    """
    # List of directories to process
    directories_to_clean = [
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
    
    print("Starting PNG filename cleanup...\n")
    
    for dir_path in directories_to_clean:
        if os.path.exists(dir_path):
            print(f"Processing directory: {dir_path}")
            clean_png_filenames(dir_path)
        else:
            print(f"Directory does not exist: {dir_path}")
    
    print("PNG filename cleanup completed!")

if __name__ == "__main__":
    main()
