import os
import shutil

def copy_until_full(source_file, target_drive):
    try:
        file_size = os.path.getsize(source_file)
        file_counter = 1

        while True:
            # Check available space on the target drive
            total, used, free = shutil.disk_usage(target_drive)
            if free < file_size:
                print(f"Drive is full or doesn't have enough space for another copy. Free space: {free} bytes.")
                break

            # Generate a unique target file path
            target_file = os.path.join(target_drive, f"copy_{file_counter}.dat")
            shutil.copy(source_file, target_file)
            print(f"Copied to: {target_file}")
            file_counter += 1

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your paths
source_file_path = "C:\\path\\to\\source_file.dat"
target_drive_path = "D:\\"

copy_until_full(source_file_path, target_drive_path)
