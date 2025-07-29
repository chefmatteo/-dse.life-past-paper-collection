import os
import re

def cleanup_suffixes(directory_path):
    """
    Remove _1, _2, etc. suffixes from filenames in the given directory.
    """
    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return

    # Get all files in the directory
    files = os.listdir(directory_path)
    png_files = [f for f in files if f.endswith('.png')]

    if not png_files:
        print(f"No PNG files found in {directory_path}")
        return

    print(f"Found {len(png_files)} PNG files in {directory_path}")

    # Pattern to match _1, _2, etc. before .png
    pattern = r'^(.+)_\d+\.png$'

    for filename in png_files:
        match = re.match(pattern, filename)
        if match:
            # Extract the base name without the _number suffix
            base_name = match.group(1)
            new_filename = f"{base_name}.png"

            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, new_filename)

            # Check if the target filename already exists
            if os.path.exists(new_path):
                print(f"Warning: {new_filename} already exists, skipping {filename}")
                continue

            try:
                os.rename(old_path, new_path)
                print(f"Cleaned: {filename} → {new_filename}")
            except OSError as e:
                print(f"Error renaming {filename}: {e}")

    print(f"Cleanup completed for {directory_path}\n")

# Directories to clean up
directories_to_clean = [
    "/Users/matthewng/Desktop/-dse.life-past-paper-collection/dse_files/econ/2017/photo",
]

if __name__ == "__main__":
    for dir_path in directories_to_clean:
        cleanup_suffixes(dir_path) 