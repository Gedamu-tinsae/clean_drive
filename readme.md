
# Drive Cleaning Script

This script provides a set of tools for securely erasing data from storage devices in both **Linux** and **Windows** systems. It includes features for overwriting data with specific patterns, performing secure erase operations using `hdparm` on Linux, and using Windows-specific methods to overwrite and clean drives.

> **Warning**: This script will permanently erase all data on the specified drive. Use with caution.

## Features

- **Automatic OS Drive Detection**: The script automatically detects the primary OS drive to ensure it is not accidentally erased.
- **Drive Path Validation**: Validates the specified drive path to prevent accidental deletion of important system drives.
- **DoD Compliant Overwriting**: Overwrites the entire drive with predefined patterns (zeros, ones, and random data) in compliance with the Department of Defense (DoD) 5220.22-M standards.
- **Secure Erase (Linux)**: Uses the `hdparm` tool to perform a secure erase on the drive on Linux systems.
- **Windows Drive Cleaning**: Includes support for overwriting drives and cleaning hidden areas (like Host Protected Area) on Windows systems.
- **Logging**: All operations are logged for tracking and debugging.

## Why?

In today's digital world, securely erasing data from storage devices is a crucial step to ensure privacy and protect sensitive information. Whether you are decommissioning a hard drive, selling an old PC, or simply clearing space on an unused storage device, simply deleting files or formatting a drive is not sufficient.

- **Data recovery tools** can easily recover deleted files, even after formatting, especially on traditional hard drives (HDDs). 
- **Overwriting** data multiple times with patterns like zeros, ones, and random data ensures that the original data cannot be retrieved by recovery software.
- **Compliance with standards** like the Department of Defense (DoD) 5220.22-M ensures that the data sanitization process is robust and follows recognized best practices for data destruction.

This script automates the process of securely erasing drives, providing an easy-to-use solution for both Linux and Windows users. By using a combination of methods like overwriting with patterns and secure erase functionality, the script guarantees that data is completely wiped, including hidden areas like the Host Protected Area (HPA) on Windows systems.

## Prerequisites

### For Linux:

- Python 3
- `hdparm` tool (for secure erase functionality)
- Sudo permissions to execute system-level commands like `hdparm`

### For Windows:

- Python 3
- Administrative privileges to access physical drives
- `psutil` library (install with `pip install psutil`)

### Installing `hdparm` (Linux):
To install `hdparm` on your Linux system, run:

```bash
sudo apt-get install hdparm
```

### Installing `psutil` (Windows):

To install the `psutil` library for Windows, run:

```bash
pip install psutil
```

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/drive-cleaning-script.git
   cd drive-cleaning-script
   ```

2. **Configure the drive to clean** by modifying the `DRIVE_PATH` variable in the script:
   
   For **Linux**, use the drive path like `/dev/sdX`:

   ```python
   DRIVE_PATH = '/dev/sdX'  # Replace with the appropriate device path
   ```

   For **Windows**, use the path format `\\.\PhysicalDriveX` (e.g., `\\.\PhysicalDrive1`):

   ```python
   DRIVE_PATH = r'\\.\PhysicalDriveX'  # Replace 'X' with the appropriate drive number
   ```

3. **Run the script:**

   - For **Linux**:

     ```bash
     sudo python3 drive_cleaning.py
     ```

   - For **Windows** (make sure to run as Administrator):

     ```bash
     python3 drive_cleaning.py
     ```

   **Important**: You need to run the script with elevated privileges (using `sudo` for Linux and as Administrator for Windows) as it interacts with low-level hardware components.

4. **Confirm Drive Cleaning:**

   The script will prompt you for confirmation before proceeding with the erasure:

   ```bash
   WARNING: This will permanently erase all data on /dev/sdX (or \\.\PhysicalDriveX).
   Type 'ERASE' to confirm: 
   ```

   Type **ERASE** to proceed.

## Functions

### Linux-Specific Functions:

- **`get_os_drive()`**: Automatically detects and returns the system drive.
- **`validate_drive_path(device_path)`**: Validates the specified device path, ensuring it exists and is not the OS drive.
- **`overwrite_with_pattern(device_path, pattern, pass_num)`**: Overwrites the specified drive with a given byte pattern.
- **`overwrite_disk_dod(device_path)`**: Performs a DoD-compliant overwrite with three passes (zeros, ones, random data).
- **`secure_erase(device_path)`**: Performs a secure erase on the specified device using the `hdparm` tool.
- **`disable_hpa(device_path)`**: Disables Host Protected Area (HPA) and restores Device Configuration Overlay (DCO) to factory settings.

### Windows-Specific Functions:

- **`is_admin()`**: Checks if the script is running with administrative privileges.
- **`get_os_drive()`**: Returns the system drive letter (e.g., `C:\`).
- **`validate_drive_path(device_path)`**: Validates the specified drive path, ensuring it exists and is not the OS drive.
- **`overwrite_with_pattern(device_path, pattern, pass_num)`**: Overwrites the specified drive with a given byte pattern.
- **`overwrite_disk_dod(device_path)`**: Performs a DoD-compliant overwrite with three passes (zeros, ones, random data).
- **`clean_drive(device_path)`**: Main function for cleaning the drive on Windows, ensuring admin privileges and overwriting the drive.

## Logging

All operations are logged to a file named `drive_cleaning.log` located in the same directory as the script. The log includes timestamps and error messages to help debug any issues.

### Example Log Entry:

```log
2025-01-08 12:00:00 - INFO - Overwriting with pattern 00000000000000000000... completed.
2025-01-08 12:01:00 - ERROR - Invalid path: /dev/sdX does not exist.
```

## Error Handling

If any errors occur during the process (e.g., invalid device path, permission errors), they are logged to `drive_cleaning.log` and printed to the terminal.

### Common Errors:
- **Permission Denied**: Ensure you are running the script with elevated privileges.
- **Invalid Path**: Double-check the device path for correctness.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

