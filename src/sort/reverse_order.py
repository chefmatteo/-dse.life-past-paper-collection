import os
import glob
from pathlib import Path

def reverse_png_numbering(directory_path):
    """
    Reverse the numbering of PNG files in a directory.
    If there are 45 files numbered 1-45, then:
    1.png becomes 45.png
    2.png becomes 44.png
    ...
    45.png becomes 1.png
    """
    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return
    
    # Get all PNG files and sort them numerically
    png_files = glob.glob(os.path.join(directory_path, "*.png"))
    
    if not png_files:
        print(f"No PNG files found in {directory_path}")
        return
    
    # Extract numbers from filenames and sort them
    files_with_numbers = []
    for file_path in png_files:
        filename = os.path.basename(file_path)
        if filename.endswith('.png'):
            # Extract the number from the filename
            try:
                number = int(filename.replace('.png', ''))
                files_with_numbers.append((file_path, number, filename))
            except ValueError:
                print(f"Skipping {filename} - not a numbered file")
                continue
    
    if not files_with_numbers:
        print(f"No numbered PNG files found in {directory_path}")
        return
    
    # Sort by the extracted number
    files_with_numbers.sort(key=lambda x: x[1])
    
    total_files = len(files_with_numbers)
    print(f"Found {total_files} numbered PNG files in {directory_path}")
    
    # Create a mapping of old numbers to new numbers (reverse order)
    number_mapping = {}
    for i, (file_path, old_number, filename) in enumerate(files_with_numbers):
        new_number = total_files - i  # Reverse the numbering
        number_mapping[old_number] = new_number
    
    # First, rename all files to temporary names to avoid conflicts
    temp_files = []
    for file_path, old_number, filename in files_with_numbers:
        new_number = number_mapping[old_number]
        temp_filename = f"temp_{new_number}.png"
        temp_path = os.path.join(directory_path, temp_filename)
        
        try:
            os.rename(file_path, temp_path)
            temp_files.append((temp_path, new_number))
            print(f"Temporary rename: {filename} → {temp_filename}")
        except OSError as e:
            print(f"Error renaming {filename}: {e}")
    
    # Now rename from temporary names to final names
    for temp_path, new_number in temp_files:
        final_filename = f"{new_number}.png"
        final_path = os.path.join(directory_path, final_filename)
        
        try:
            os.rename(temp_path, final_path)
            print(f"Final rename: temp_{new_number}.png → {final_filename}")
        except OSError as e:
            print(f"Error renaming temp_{new_number}.png: {e}")
    
    print(f"Successfully reversed numbering for {total_files} files in {directory_path}\n")

# Directory to process
target_directory = "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2022/photo"

if __name__ == "__main__":
    reverse_png_numbering(target_directory) 