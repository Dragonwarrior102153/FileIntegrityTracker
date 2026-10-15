#imports
import sqlite3

class FileIntegrityTrackerDb:
    def __init__(self):
        # Initialize the database connection here
        pass
        

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

    def disconnect(self):
        try:
            self.conn.close()
            return "disconnected from fileIntegrityTracker db"
        
        except sqlite3.Error as error:
            return str(error)