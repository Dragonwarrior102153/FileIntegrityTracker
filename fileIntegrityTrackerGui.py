# Connects the Tkinter interface to the SQLite-backed file integrity tracker.
from fileIntegrityTrackerDb import FileIntegrityTrackerDb
import tkinter as tk
from tkinter import filedialog
import hashlib
import tkinter.messagebox


# Provides the application's windows, file actions, and record navigation.
class FileIntegrityTrackerGui:
    # Creates the database client and starts the main application window.
    def __init__(self):
        # Initialize the GUI components here
        self.fitDb = FileIntegrityTrackerDb()

        self.mainWin = tk.Tk()
        self.mainWin.title("File Integrity Tracker")
        self.mainWin.config(background="black")

        self.defaultView()
        
        self.mainWin.mainloop()

    # Builds the main window's controls and connects them to their handlers.
    def defaultView(self):
        self.check = tk.Label(self.mainWin, text="", font=("Arial", 16))
        self.check.place(relx=0.3, rely=0.5, anchor="center")
        
        self.connectBtn = tk.Button(self.mainWin, text="Connect", command=self.connect)
        self.connectBtn.place(relx=0.3, rely=0.65, anchor="center")
        
        self.fileLbl = tk.Label(self.mainWin)
        self.fileLbl.place(relx=0.5, rely=0.5, anchor="center")
        self.chooseFileBtn = tk.Button(self.mainWin, text = "Select File", command=self.chooseFile)
        self.chooseFileBtn.place(relx=0.7, rely=0.5, anchor="center")
        
        self.insertBtn = tk.Button(self.mainWin, text="Insert", command=self.clearForInsert)
        self.insertBtn.place(relx=0.4, rely=0.65, anchor="center")
        
        updateBtn = tk.Button(self.mainWin, text="Update", command=self.update)
        updateBtn.place(relx=0.5, rely=0.65, anchor="center")
        
        deleteBtn = tk.Button(self.mainWin, text="Delete", command=self.delete)
        deleteBtn.place(relx=0.6, rely=0.65, anchor="center")

        listViewBtn = tk.Button(self.mainWin, text="List View", command=self.listView)
        listViewBtn.place(relx=0.5, rely=0.75, anchor="center")
        
        self.searchBar = tk.Entry(self.mainWin)
        self.searchBar.place(relx=0.5, rely=0.8, anchor="center")
        searchBtn = tk.Button(self.mainWin, text="Search", command=self.searchForVal)
        searchBtn.place(relx=0.5, rely=0.85, anchor="center")
        
        right1Btn = tk.Button(self.mainWin, text=">", command=self.right1)
        right1Btn.place(relx=0.5, rely=0.575, anchor="center")    
        right3Btn = tk.Button(self.mainWin, text=">>>", command=self.right3)    
        right3Btn.place(relx=0.55, rely=0.575, anchor="center")
        fullRightBtn = tk.Button(self.mainWin, text=">|", command=self.fullRight)
        fullRightBtn.place(relx=0.6, rely=0.575, anchor="center")
        left1Btn = tk.Button(self.mainWin, text="<", command=self.left1)
        left1Btn.place(relx=0.45, rely=0.575, anchor="center")
        left3Btn = tk.Button(self.mainWin, text="<<<", command=self.left3)
        left3Btn.place(relx=0.4, rely=0.575, anchor="center")
        fullLeftBtn = tk.Button(self.mainWin, text="|<", command=self.fullLeft)
        fullLeftBtn.place(relx=0.35, rely=0.575, anchor="center")
        

    # Calculates a file's SHA-256 digest while reading it in bounded chunks.
    def hashFile(self, filePath):
        hasher = hashlib.sha256()
        with open(filePath, "rb") as file:
            while chunk := file.read(64 * 1024):
                hasher.update(chunk)

        return hasher.hexdigest() 

    # Opens a file picker and displays the chosen path.
    def chooseFile(self):
        file_path = filedialog.askopenfilename(
            parent=self.mainWin,
            title="Select a file",
        )
        if (file_path):
            self.fileLbl.config(text=file_path)

    # Opens or closes the database connection using the Connect button.
    def connect(self):
        if (self.connectBtn["text"] == "Connect"):
            self.fitDb.connect()
            print(self.fitDb.selectAll())
            self.id = self.fitDb.selectAll()[0][0]
            self.connectBtn.config(text="Disconnect")
            self.reset()
            print(self.fitDb.selectAll())

        else:
            self.fitDb.disconnect()
            self.connectBtn.config(text="Connect")
            self.fileLbl.config(text="Choose File")

    # Displays the selected record and updates its integrity indicator.
    def reset(self):
        self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))
        if (self.checkIntegrity()):
            self.check.config(text="✓", fg="green")
        else:
            self.check.config(text="✗", fg="red")

    # Prepares the interface to choose a file for a new record.
    def clearForInsert(self):
        self.fileLbl.config(text="Choose new file")
        self.insertBtn.config(text="Commit", command=self.insert)


    # Saves the selected file path and its current hash as a database record.
    def insert(self):
        #ensure that the path isnt already in the database
        values = self.fitDb.selectAll()
        for row in values:
            if (row[1] == self.fileLbl["text"]):
                tkinter.messagebox.showerror("Error", "File already exists in database.")
                return
        
        #ensure user doesnt insert empty file path
        if (self.fileLbl["text"] == "Choose new file"):
            tkinter.messagebox.showerror("Error", "Please select a file to insert.")
            return
        else:
            self.fitDb.insert(self.fileLbl["text"], self.hashFile(self.fileLbl["text"]))
            self.insertBtn.config(text="Insert", command=self.clearForInsert)

        
    # Compares the selected record's saved hash with the file's current hash.
    def checkIntegrity(self):
        oldHash = self.fitDb.select(self.id, "HashValue")
        newHash = self.hashFile(self.fileLbl["text"])
        return (oldHash == newHash)

    # Replaces the selected record's path and saved hash with the current file.
    def update(self):
        self.fitDb.update(self.id, self.fileLbl["text"], self.hashFile(self.fileLbl["text"]))
        self.reset()

    # Deletes the selected row and selects its position in the refreshed rows.
    def delete(self):
        if (tkinter.messagebox.askyesno("Delete", f"Are you sure you want to delete {self.fileLbl['text']}?")):
            values = self.fitDb.selectAll() 
            currentIndex = self.findValInList(self.id, values)
            self.fitDb.delete(self.id) 
            values = self.fitDb.selectAll()
            if (currentIndex is not None):          
                self.id = values[min(currentIndex, len(values) - 1)][0]
            self.reset()

    # Opens a window listing each stored path and its current integrity status.
    def listView(self):
        #show all the files in the database in a new window, and their integrity status
        values = self.fitDb.selectAll()
        if (isinstance(values, str)):
            raise RuntimeError(f"Could not load database rows: {values}")
        else:
            dbWin = tk.Toplevel(self.mainWin)
            dbWin.title("Database")
            dbWin.config(background="black")
            for i, row in enumerate(values):
                fileLbl = tk.Label(dbWin, text=row[1])
                fileLbl.grid(row=i, column=0)
                if (self.hashFile(row[1]) == row[2]):
                    check = tk.Label(dbWin, text="✓", fg="green", font=("Arial", 16))
                else:
                    check = tk.Label(dbWin, text="✗", fg="red", font=("Arial", 16))
                #have spacing between the file name and the check mark
                fileLbl.grid(padx=10, pady=5)
                check.grid(row=i, column=1)
                check.grid(padx=10, pady=5)
        
    # Selects the first record whose file path contains the entered text.
    def searchForVal(self):
        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")
        else:
            for row in values:
                #check if the file is in the db (the user doesnt need to put in the whole file path, just the last part is enough)
                if (self.searchBar.get() in row[1]):
                    self.id = row[0]
                    self.reset()    
                    return
            tkinter.messagebox.showerror("Error", "File not found in database.")

    #navigation buttons (ensure that the id exists in the database before changing it)

    # Returns the row index for a database ID, or None if no row matches.
    def findValInList(self, id, list):
        for i in range(len(list)):
            if (list[i][0] == id):
                return i

    # Moves to the next record, stopping at the final row.
    def right1(self):   
        values = self.fitDb.selectAll()
        currentIndex = self.findValInList(self.id, values)

        if (currentIndex is not None):
            diffInIds = len(values) - currentIndex - 1
            if (diffInIds >= 1):
                self.id = values[currentIndex + 1][0]
                
            else:
                self.id = values[currentIndex + diffInIds][0]
                            
        self.reset()

    # Moves forward by up to three records, stopping at the final row.
    def right3(self):
        values = self.fitDb.selectAll()
        currentIndex = self.findValInList(self.id, values)

        if (currentIndex is not None):
            diffInIds = len(values) - currentIndex - 1
            if (diffInIds >= 3):
                self.id = values[currentIndex + 3][0]
                
            else:
                self.id = values[currentIndex + diffInIds][0]
                            
        self.reset()

    # Selects the record with the greatest database ID.
    def fullRight(self):

        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")

        self.id = max((row[0] for row in values), default=self.id)

        self.reset()
        

    # Moves to the previous record, stopping at the first row.
    def left1(self):
        values = self.fitDb.selectAll()
        currentIndex = self.findValInList(self.id, values)

        if (currentIndex is not None):
            if (currentIndex >= 1):
                self.id = values[currentIndex - 1][0]         

        self.reset()

    # Moves backward by up to three records, stopping at the first row.
    def left3(self):
        values = self.fitDb.selectAll()
        currentIndex = self.findValInList(self.id, values)

        if (currentIndex is not None):
            if (currentIndex >= 3):
                self.id = values[currentIndex - 3][0]
        
            else:
                self.id = values[0][0]            

        self.reset()

    # Selects the first row returned by the database.
    def fullLeft(self):
        values = self.fitDb.selectAll()
        self.id = values[0][0]
        self.reset()
        
            

    
        
