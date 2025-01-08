import os
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='drive_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_os_drive():
    """
    Automatically determine the system drive.
    Returns:
        str: The system drive path (e.g., '/dev/sda').
    """
    try:
        with open('/proc/mounts', 'r') as mounts:
            for line in mounts:
                if ' / ' in line:  # Root filesystem
                    return line.split()[0].replace('1', '')  # Normalize device path
    except Exception as e:
        logging.error(f"Error detecting OS drive: {e}")
        print("Error detecting the OS drive.")
        return None

def validate_drive_path(device_path):
    """
    Validate the specified drive path to ensure it's correct and not the OS drive.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
    Returns:
        bool: True if the path is valid, False otherwise.
    """
    os_drive = get_os_drive()
    if not os_drive:
        return False

    # Check if the device path exists
    if not os.path.exists(device_path):
        logging.error(f"Invalid path: {device_path} does not exist.")
        print("Error: Specified drive does not exist.")
        return False

    # Ensure the drive is not the OS drive
    if device_path == os_drive:
        logging.error("Attempted to erase the OS drive.")
        print("Error: You cannot erase the primary OS drive.")
        return False

    return True

def overwrite_with_pattern(device_path, pattern, pass_num):
    """
    Overwrite the disk with a specific pattern.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
        pattern: Byte pattern to write (e.g., b'\x00' for zeros).
        pass_num: Current pass number for logging.
    """
    try:
        with open(device_path, 'wb') as disk:
            print(f"Pass {pass_num}: Overwriting with {pattern.hex()}...")
            while True:
                try:
                    disk.write(pattern * 4096)
                except OSError:
                    break
        logging.info(f"Pass {pass_num} (pattern {pattern.hex()}) completed.")
        print(f"Pass {pass_num} complete.")
    except PermissionError:
        logging.error("Permission denied. Run the script with elevated privileges (sudo).")
        print("Permission denied. Run the script with elevated privileges (sudo).")
    except Exception as e:
        logging.error(f"Error during overwrite (pattern {pattern.hex()}): {e}")
        print(f"An error occurred: {e}")

def overwrite_disk_dod(device_path):
    """
    Overwrite the disk following DoD and NIST standards.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
    """
    overwrite_with_pattern(device_path, b'\x00', 1)  # Pass 1: Zeros
    overwrite_with_pattern(device_path, b'\xFF', 2)  # Pass 2: Ones
    overwrite_with_pattern(device_path, os.urandom(1), 3)  # Pass 3: Random data

def secure_erase(device_path):
    """
    Perform a Secure Erase on the specified device using hdparm.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
    """
    try:
        subprocess.run(
            ["sudo", "hdparm", "--user-master", "u", "--security-set-pass", "password", device_path],
            check=True
        )
        subprocess.run(
            ["sudo", "hdparm", "--security-erase", "password", device_path],
            check=True
        )
        logging.info("Secure erase completed successfully.")
        print("Secure erase completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Secure erase failed: {e}")
        print(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred during secure erase: {e}")
        print(f"An error occurred: {e}")

def disable_hpa(device_path):
    """
    Disable Host Protected Area (HPA) on the specified device.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
    """
    try:
        subprocess.run(["sudo", "hdparm", "--disable-hpa", device_path], check=True)
        subprocess.run(["sudo", "hdparm", "--dco-restore", device_path], check=True)
        logging.info("HPA disabled and DCO restored to factory defaults.")
        print("HPA disabled and DCO restored to factory defaults.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to disable HPA/DCO: {e}")
        print(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred during HPA/DCO disable: {e}")
        print(f"An error occurred: {e}")

def clean_drive(device_path):
    """
    Securely erase a drive, including remapped sectors and hidden areas.
    Args:
        device_path: The path to the drive (e.g., '/dev/sdX').
    """
    try:
        if not validate_drive_path(device_path):
            return

        print(f"WARNING: This will permanently erase all data on {device_path}.")
        confirmation = input("Type 'ERASE' to confirm: ")
        if confirmation != "ERASE":
            logging.info("Operation cancelled by the user.")
            print("Operation cancelled.")
            return

        print("Disabling hidden areas (HPA/DCO)...")
        disable_hpa(device_path)
        print("Performing Secure Erase...")
        secure_erase(device_path)
        print("Overwriting with DoD standard (zeros, ones, random data)...")
        overwrite_disk_dod(device_path)
        logging.info("Drive cleaning completed successfully.")
        print("Drive cleaned successfully!")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An error occurred: {e}")

# User changes this variable to specify the drive to be cleaned
DRIVE_PATH = '/dev/sdX'
clean_drive(DRIVE_PATH)
