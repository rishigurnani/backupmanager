backupmanager
=============

backupmanager is a lightweight Python-based backup tool that:

- Removes all files from a specified destination directory.
- Recursively copies files under a certain size threshold from a source directory to a destination directory.
- Checks user inactivity on macOS (using Quartz) and only runs when the user is active.
- Uses a `stop.txt` file as a signal to stop execution gracefully.

Requirements
------------

- Python 3.x
- macOS (due to the Quartz idle time detection; for other operating systems, you'll need a different idle detection mechanism)
- Quartz (part of macOS, no additional installation required)
- `shutil`, `os`, and `time` modules included in the standard library

Installation and Setup
----------------------

1. Clone the repository:
   
   .. code-block:: bash

      git clone https://github.com/rishigurnani/backupmanager.git

2. Navigate into the cloned directory:

   .. code-block:: bash

      cd backupmanager

3. (Optional) Create and activate a virtual environment:
   
   .. code-block:: bash

      python3 -m venv venv
      source venv/bin/activate  # On macOS/Linux
      venv\Scripts\activate     # On Windows

4. Place a `stop.txt` file in the same directory as the script to keep it running. Remove or rename `stop.txt` to stop the program.

Usage
-----

1. Edit the constants at the top of the script (e.g., `COPYTO_FOLDER`, `COPYFROM_FOLDER`, `SIZE_THRESHOLD`) to match your needs.

2. Run the script:
   
   .. code-block:: bash

      python3 run.py

   The script will:
   
   - Continuously run in the background (as long as `stop.txt` is present).
   - Remove all files from the destination directory.
   - Recursively copy files below the defined size threshold from the source directory.
   - Only run these tasks while the user is active on the laptop.

3. To stop the script, remove or rename `stop.txt`. The script will exit gracefully on the next iteration.

Contributing
------------

Contributions are welcome! Feel free to submit issues, fork the repository, and create pull requests.

License
-------

This project is released under the MIT License. See `LICENSE` for details.
