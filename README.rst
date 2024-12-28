backupmanager
=============

backupmanager is a lightweight Python-based backup tool that:

- Recursively copies files under a certain size threshold from a source directory (e.g., a directory that isn't being backed up) to a destination directory (e.g., a directory that is being backed up).
- Checks user inactivity on macOS (using Quartz) and only runs when the user is active.
- Uses a stop.txt file as a signal to stop execution gracefully.

Requirements
------------

- Python 3.x
- macOS (due to Quartz-based idle time detection)
- Quartz (included with macOS, no separate install required)
- Standard Python libraries: os, shutil, time, datetime, Quartz

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
      venv\Scripts\activate     # On Windows (only if using a different OS environment)

4. Place a stop.txt file in the same directory as your main script (run.py). This file signals the script to keep running. Removing or renaming stop.txt will stop the script gracefully.

Usage
-----

Manual Launch
-------------

1. Edit Script Constants:
   
   Open run.py and adjust the constants at the top:
   
   - COPYTO_FOLDER: The destination folder where files will be copied.
   - COPYFROM_FOLDER: The source folder from which files will be copied.
   - SIZE_THRESHOLD: The maximum file size (in bytes) for files to be copied.
   - IDLE_THRESHOLD: The idle time in seconds before the script pauses tasks if the user is inactive.
   - CHECK_INTERVAL: How often (in seconds) the script checks for idle time and performs tasks.

2. Run the Script:
   
   Ensure stop.txt is present. Then run:
   
   .. code-block:: bash

      python3 run.py

   The script will:
   - Continuously monitor the user’s activity.
   - When the user is active, remove all files from the destination folder and then recursively copy files below SIZE_THRESHOLD from the source to the destination.
   - Sleep for CHECK_INTERVAL seconds between checks.
   - Stop when stop.txt is removed or renamed.

3. Stopping the Script:
   
   Simply delete or rename stop.txt. The script will detect its absence on the next loop and exit gracefully.

Launch at Startup (Optional)
----------------------------

If you want the script to run automatically when your Mac starts up, you can use launchd:

1. Create a Launch Agent Plist File:
   
   In ~/Library/LaunchAgents/, create a plist file (for example, com.yourusername.backupmanager.plist) with content similar to:
   
   .. code-block:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
         "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
      <plist version="1.0">
      <dict>
          <key>Label</key>
          <string>com.yourusername.backupmanager</string>
          <key>ProgramArguments</key>
          <array>
              <string>/usr/bin/python3</string>
              <string>/path/to/run.py</string>
          </array>
          <key>RunAtLoad</key>
          <true/>
          <key>StandardOutPath</key>
          <string>/path/to/output.log</string>
          <key>StandardErrorPath</key>
          <string>/path/to/error.log</string>
      </dict>
      </plist>

2. Load the Launch Agent:

   .. code-block:: bash

      launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yourusername.backupmanager.plist

3. Verify and Reboot:
   
   After loading the plist, reboot your Mac. The script should now run automatically at startup. To stop it, remove stop.txt as described above.

Contributing
------------

Contributions are welcome. Feel free to submit issues, fork the repository, and create pull requests.

License
-------

This project is released under the MIT License. See LICENSE for details.
