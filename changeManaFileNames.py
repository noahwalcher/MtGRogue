import os

def correct_filenames(directory):
    for filename in os.listdir(directory):
        # Check if the filename ends with 'p' after the extension (e.g., .pngp)
        if filename.endswith("p"):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)
            
            # Check if the extension contains an extra 'p' (e.g., .pngp)
            if ext.endswith("p"):
                # Remove the extra 'p' from the extension
                correct_ext = ext[:-1]
                # Construct the new filename by placing 'p' before the correct extension
                new_filename = name + "p" + correct_ext
                
                # Get full file paths
                old_file_path = os.path.join(directory, filename)
                new_file_path = os.path.join(directory, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Corrected: {filename} -> {new_filename}")

# Example usage
directory = "ManaSymbols"
correct_filenames(directory)
