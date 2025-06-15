from pathlib import Path

def delete_all_jpg_files(folder_path: str):
    """
    Delete all .jpg files inside the given folder and its subfolders.
    
    Args:
        folder_path (str): Path to the folder where .jpg files will be deleted.
    """
    folder = Path(folder_path)
    print(f"Deleting all .jpg files in: {folder}")
    extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
    count = 0
    for ext in extensions:
        for jpg_file in folder.rglob(ext):
            try:
                jpg_file.unlink()
                print(f"Deleted: {jpg_file}")
                count += 1
            except Exception as e:
                print(f"Failed to delete {jpg_file}: {e}")
    print(f"Total image files deleted: {count}")