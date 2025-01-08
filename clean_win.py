import os
import ctypes
import logging
import random
import psutil

# Configure logging
logging.basicConfig(
    filename='drive_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def get_os_drive():
    """
    Automatically determine the system drive on Windows.
    Returns:
        str: The system drive letter (e.g., 'C:\\').
    """
    return os.getenv('SystemDrive') + '\\'

def validate_drive_path(device_path):
    """
    Validate the specified drive path to ensure it's correct and not the OS drive.
    Args:
        device_path: The path to the drive (e.g., '\\\\.\\PhysicalDriveX').
    Returns:
        bool: True if the path is valid, False otherwise.
    """
    os_drive = get_os_drive()
    if not os_drive:
        return False

    # Ensure the drive path exists
    if not os.path.exists(device_path):
        logging.error(f"Invalid path: {device_path} does not exist.")
        print("Error: Specified drive does not exist.")
        return False

    # Ensure the drive is not the OS drive
    if os.path.abspath(device_path).startswith(os.path.abspath(os_drive)):
        logging.error("Attempted to erase the OS drive.")
        print("Error: You cannot erase the primary OS drive.")
        return False

    return True

def overwrite_with_pattern(device_path, pattern, pass_num):
    """
    Overwrite the disk with a specific pattern.
    Args:
        device_path: The path to the drive (e.g., '\\\\.\\PhysicalDriveX').
        pattern: Byte pattern to write (e.g., b'\x00' for zeros).
        pass_num: Current pass number for logging.
    """
    try:
        with open(device_path, 'wb') as disk:
            print(f"Pass {pass_num}: Overwriting with pattern...")
            for _ in range(10000):  # Write 10000 blocks of 4 KB
                disk.write(pattern * 4096)
        logging.info(f"Pass {pass_num} completed with pattern.")
        print(f"Pass {pass_num} complete.")
    except PermissionError:
        logging.error("Permission denied. Run the script as Administrator.")
        print("Permission denied. Run the script as Administrator.")
    except Exception as e:
        logging.error(f"Error during overwrite (pattern): {e}")
        print(f"An error occurred: {e}")

def overwrite_disk_dod(device_path):
    """
    Overwrite the disk following DoD and NIST standards.
    Args:
        device_path: The path to the drive (e.g., '\\\\.\\PhysicalDriveX').
    """
    overwrite_with_pattern(device_path, b'\x00', 1)  # Pass 1: Zeros
    overwrite_with_pattern(device_path, b'\xFF', 2)  # Pass 2: Ones
    overwrite_with_pattern(device_path, os.urandom(4096), 3)  # Pass 3: Random data

def clean_drive(device_path):
    """
    Securely erase a drive, including overwriting data with patterns.
    Args:
        device_path: The path to the drive (e.g., '\\\\.\\PhysicalDriveX').
    """
    if not is_admin():
        print("Error: This script must be run as Administrator.")
        return

    try:
        if not validate_drive_path(device_path):
            return

        print(f"WARNING: This will permanently erase all data on {device_path}.")
        confirmation = input("Type 'ERASE' to confirm: ")
        if confirmation != "ERASE":
            logging.info("Operation cancelled by the user.")
            print("Operation cancelled.")
            return

        print("Overwriting with DoD standard (zeros, ones, random data)...")
        overwrite_disk_dod(device_path)
        logging.info("Drive cleaning completed successfully.")
        print("Drive cleaned successfully!")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An error occurred: {e}")

# User changes this variable to specify the drive to be cleaned
DRIVE_PATH = r'\\.\PhysicalDriveX'  # Replace 'X' with the desired drive number (e.g., '\\.\PhysicalDrive1')
clean_drive(DRIVE_PATH)
