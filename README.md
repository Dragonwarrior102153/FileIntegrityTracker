# File Integrity Tracker

A desktop application for tracking files and checking whether their contents have changed. The application stores each file path and its SHA-256 hash in a local SQLite database, then compares the stored hash with a newly calculated hash to report the file's integrity.

## Features

- Add a file and save its path and SHA-256 hash.
- Check a tracked file by comparing its current hash with the saved hash.
- Update or delete the selected database record.
- Navigate records, search by part of a file path, and view all records with their integrity status.

## Requirements

- Python 3.8 or newer.
- Tkinter, which is included with most standard Python installations.

The application uses only Python's standard library; no package installation is required.

## Run

From this directory, run:

```text
python fileIntegrityTracker.py
```

The SQLite database file is named `fileIntegrityTracker.sqlite`. It is created in the current working directory the first time the application connects to the database. Run the command from this project directory to keep the database here.

## Using the application

1. Start the program and select **Connect**.
2. Use **Select File**, then **Insert** and **Commit** to track a file.
3. Navigate between records with the arrow buttons. Use **Search** to find a record by a substring of its path, or **List View** to see all records.
4. Select a tracked file record before using **Update** or **Delete**.

The integrity indicator compares the file's current SHA-256 hash with the hash saved in the selected record. A matching hash is shown with a green check; a mismatch is shown with a red cross.

## Data and implementation

Each row in the `fileIntegrityTrackerDb` table contains:

| Column | Description |
| --- | --- |
| `ID` | SQLite primary key for the record |
| `FilePath` | Path to the tracked file |
| `HashValue` | SHA-256 digest saved for the file |

The database layer is in `fileIntegrityTrackerDb.py`, the Tkinter interface is in `fileIntegrityTrackerGui.py`, and `fileIntegrityTracker.py` starts the application.

## Current limitations

- The application expects at least one database record when connecting and navigating. An empty database is not currently handled throughout the GUI.
- Navigation uses the order returned by SQLite; the query does not specify an explicit sort order.
- Tracked file paths refer to files on the local machine. If a file is moved or becomes inaccessible, its integrity check cannot read it.

`test.py` is a small standalone example script, not an automated test suite.
