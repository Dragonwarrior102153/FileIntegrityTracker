
# Starts the File Integrity Tracker desktop application.
from fileIntegrityTrackerGui import FileIntegrityTrackerGui


# Creates the GUI application and enters its Tkinter event loop.
def main():
    fileIntegrityTrackerGui = FileIntegrityTrackerGui()


# Run the application only when this script is executed directly.
if (__name__ == "__main__"):
    main()