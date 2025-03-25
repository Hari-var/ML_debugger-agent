import os

def directory_contents(path):
    structure=f" "
    for root,dir, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure+=(f"{os.path.basename(root)}/\n")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure+=(f"{subindent}{f}\n")
    return structure
# Replace 'your_folder_path' with the path to your folder
if __name__ == "__main__":
    
    path=input ("Enter the path of the folder: ")
    print(directory_contents(path))
