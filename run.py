import os
import shutil
import time
import datetime
import Quartz  # For macOS idle time detection

# Print the starting time
start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"Program started at {start_time}.")

# Define constants
COPYTO_FOLDER = ""  # edit this to meet your needs
COPYFROM_FOLDER = ""  # edit this to meet your needs
SIZE_THRESHOLD = 10 * 1024 * 1024  # Maximum file size in bytes (e.g., 1024 * 1024 = 1MB)
CHECK_INTERVAL = 60  # Time in seconds to wait between each check
IDLE_THRESHOLD = 300  # Time in seconds of allowed idle time (e.g., 5 minutes)
VERBOSE = False  # Set to False to suppress print/log output

# Dynamically set the path to the stop file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STOP_FILE = os.path.join(SCRIPT_DIR, "stop.txt")

def get_idle_duration():
    """Get idle time on macOS."""
    idle = Quartz.CGEventSourceSecondsSinceLastEventType(
        Quartz.kCGEventSourceStateCombinedSessionState,
        Quartz.kCGAnyInputEventType
    )
    return idle

def log(message):
    """Prints the message if VERBOSE is True."""
    if VERBOSE:
        print(message)

def remove_all_files(folder_path):
    """
    Remove all files (and symlinks) recursively from the specified folder.
    This will not remove directories themselves, just the files within them.
    """
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    log(f"Removed file: {file_path}")
            except Exception as e:
                log(f"Failed to delete {file_path}. Reason: {e}")

def copy_files_below_size(src_folder, dest_folder, max_size):
    """
    Recursively copy files from src_folder to dest_folder if their size is below max_size.
    Directory structure is replicated in the destination.
    """
    for root, dirs, files in os.walk(src_folder):
        # Compute the corresponding target directory by preserving the relative structure
        relative_path = os.path.relpath(root, src_folder)
        if relative_path == ".":
            target_path = dest_folder
        else:
            target_path = os.path.join(dest_folder, relative_path)

        # Ensure the target directory exists
        os.makedirs(target_path, exist_ok=True)

        for filename in files:
            src_file_path = os.path.join(root, filename)
            dest_file_path = os.path.join(target_path, filename)

            # Attempt to copy files below the size threshold
            try:
                if os.path.isfile(src_file_path) and os.path.getsize(src_file_path) < max_size:
                    shutil.copy2(src_file_path, dest_file_path)
                    log(f"Copied file: {src_file_path} to {dest_file_path}")
            except Exception as e:
                log(f"Failed to copy {src_file_path}. Reason: {e}")

# Main loop
while True:
    # Check if the stop file has been removed
    if not os.path.exists(STOP_FILE):
        exit_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Stop file missing. Exiting program at {exit_time}.")
        break

    # Check for user activity
    idle_duration = get_idle_duration()
    if idle_duration < IDLE_THRESHOLD:
        log("User active, proceeding with task...")

        # Step 1: Remove all files from COPYTO_FOLDER recursively
        remove_all_files(COPYTO_FOLDER)

        # Step 2: Recursively copy files below size threshold from COPYFROM_FOLDER to COPYTO_FOLDER
        copy_files_below_size(COPYFROM_FOLDER, COPYTO_FOLDER, SIZE_THRESHOLD)
    else:
        log("User inactive, pausing task...")

    # Wait for the specified interval before repeating
    time.sleep(CHECK_INTERVAL)
