# Provides SQLite operations for the file integrity tracker.
import sqlite3


# Reads and writes tracked file paths and their saved SHA-256 hashes.
class FileIntegrityTrackerDb:
    # Initializes the database client; the connection is opened by connect().
    def __init__(self):
        # Initialize the database connection here
        pass
        

    # Opens the SQLite database and creates its table if it does not exist.
    def connect(self):
        try:
            self.conn = sqlite3.connect('fileIntegrityTracker.sqlite')
            self.cursor = self.conn.cursor()

            query = """
                    CREATE TABLE IF NOT EXISTS fileIntegrityTrackerDb(
                    ID INTEGER PRIMARY KEY,
                    FilePath TEXT,
                    HashValue TEXT)
                    """
            self.cursor.execute(query)
            self.conn.commit()
            return "connected to fileIntegrityTracker db"
        
        except sqlite3.Error as error:
            return str(error)

    # Inserts a file path and its hash as a new database row.
    def insert(self, file, hashVal):
        try:
            query = """
                    INSERT INTO fileIntegrityTrackerDb 
                    (FilePath, HashValue) VALUES(?, ?)
                    """
            self.cursor.execute(query, (file, hashVal))
            self.conn.commit()
            return f"inserted file {file}"
        
        except sqlite3.Error as err:
            return str(err)

    # Deletes the row with the given database ID.
    def delete(self, ID):
        try:
            query = """
                    DELETE FROM fileIntegrityTrackerDb WHERE (ID = ?)
                    """
            self.cursor.execute(query, (ID,))
            self.conn.commit()
            return "deleted"

        except sqlite3.Error as err:
            return str(err)

    # Updates the file path and hash for the row with the given database ID.
    def update(self, ID, fileNew, hashNew):
        try:
            query = """
                    UPDATE fileIntegrityTrackerDb SET FilePath = ?, HashValue = ? WHERE (ID = ?)
                    """
            self.cursor.execute(query, (fileNew, hashNew, ID))
            self.conn.commit()
            return "updated"

        except sqlite3.Error as err:
            return str(err)

    # Returns one column value for an ID, or an error string on SQLite failure.
    def select(self, ID, column):
        try:
            query = f"""
                    SELECT {column} FROM fileIntegrityTrackerDb WHERE (ID = ?)
                    """
            self.cursor.execute(query, (ID,))
            row = self.cursor.fetchone()
            
            return row[0] if row else ""

        except sqlite3.Error as err:
            return str(err)

    # Returns all database rows, or an error string on SQLite failure.
    def selectAll(self):
            try:
                query = """
                        SELECT * FROM fileIntegrityTrackerDb
                        """
                self.cursor.execute(query)
                value = self.cursor.fetchall()
    
                return value
    
            except sqlite3.Error as err:
                return str(err)

    # Closes the active SQLite connection.
    def disconnect(self):
        try:
            self.conn.close()
            return "disconnected from fileIntegrityTracker db"
        
        except sqlite3.Error as error:
            return str(error)