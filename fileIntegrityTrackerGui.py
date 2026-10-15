#imports
from fileIntegrityTrackerDb import FileIntegrityTrackerDb
import tkinter as tk
from tkinter import filedialog
import hashlib
import tkinter.messagebox

class FileIntegrityTrackerGui:
    def __init__(self):
        # Initialize the GUI components here
        self.fitDb = FileIntegrityTrackerDb()

        self.mainWin = tk.Tk()
        self.mainWin.title("File Integrity Tracker")
        self.mainWin.config(background="black")

        self.id = 1

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

        self.mainWin.mainloop()

    def hashFile(self, file):
        # Implement the hashing logic here
        with open(file, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()

    def chooseFile(self):
        file_path = filedialog.askopenfilename(
            parent=self.mainWin,
            title="Select a file",
        )
        if (file_path):
            self.fileLbl.config(text=file_path)

    def connect(self):
        # Implement the database connection logic here
        if (self.connectBtn["text"] == "Connect"):
            self.fitDb.connect()
            self.connectBtn.config(text="Disconnect")
            self.reset()
            print(self.fitDb.selectAll())

        else:
            self.fitDb.disconnect()
            self.connectBtn.config(text="Connect")
            self.fileLbl.config(text="Choose File")

    def reset(self):
        self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))
        if (self.checkIntegrity()):
            self.check.config(text="✓", fg="green")
        else:
            self.check.config(text="✗", fg="red")

    def clearForInsert(self):
        self.fileLbl.config(text="Choose new file")
        self.insertBtn.config(text="Commit", command=self.insert)


    def insert(self):
        #ensure user doesnt insert empty file path
        if (self.fileLbl["text"] == "Choose new file"):
            tkinter.messagebox.showerror("Error", "Please select a file to insert.")
            return
        else:
            self.fitDb.insert(self.fileLbl["text"], self.hashFile(self.fileLbl["text"]))
            self.insertBtn.config(text="Insert", command=self.clearForInsert)

        #ensure that the path isnt already in the database
        values = self.fitDb.selectAll()
        for row in values:
            if (row[1] == self.fileLbl["text"]):
                tkinter.messagebox.showerror("Error", "File already exists in database.")
                return

    def checkIntegrity(self):
        oldHash = self.fitDb.select(self.id, "HashValue")
        newHash = self.hashFile(self.fileLbl["text"])
        return (oldHash == newHash)

    def update(self):
        self.fitDb.update(self.id, self.fileLbl["text"], self.hashFile(self.fileLbl["text"]))
        self.reset()

    def delete(self):
        if (self.id == len(self.fitDb.selectAll())):
            self.id -= 1
        if (tkinter.messagebox.askyesno("Delete", f"Are you sure you want to delete {self.fileLbl['text']}?")):
            self.fitDb.delete(self.id)
        self.reset()

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
        
    def searchForVal(self):
        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")
        else:
            for row in values:
                #check if the file is in the db (the user doesnt need to put in the whole file path, just the last part is enough)
                if (self.searchBar["text"] in row[1]):
                    self.id = row[0]
                    self.reset()    
                    return
            tkinter.messagebox.showerror("Error", "File not found in database.")

    #navigation buttons (ensure that the id exists in the database before changing it)

    def right1(self):
        if (self.id < len(self.fitDb.selectAll())):
            self.id += 1
            self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))
        

        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")
        
        last_id = max((row[0] for row in values), default=self.id)
        while (self.fileLbl["text"] == "" and self.id < last_id):
            self.id += 1

        self.reset()

    def right3(self):
        if (self.id < len(self.fitDb.selectAll()) - 2):
            self.id += 3
        else:
            self.id = len(self.fitDb.selectAll())
        self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))
    

        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")
        
        last_id = max((row[0] for row in values), default=self.id)
        while (self.fileLbl["text"] == "" and self.id < last_id):
            self.id += 1
        
        self.reset()

    def fullRight(self):

        values = self.fitDb.selectAll()
        if isinstance(values, str):
            raise RuntimeError(f"Could not load database rows: {values}")
        
        last_id = max((row[0] for row in values), default=self.id)
        while (self.fileLbl["text"] == "" and self.id < last_id):
            self.id += 1
            self.reset()

        self.reset()
        

    def left1(self):
        if (self.id > 1):
            self.id -= 1
            self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))
        

        while (self.fileLbl["text"] == "" and self.id > 0):
            self.id -= 1
            self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))

        self.reset()

    def left3(self):
        if (self.id > 3):
            self.id -= 3
        else:
            self.id = 1
        self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))

        while (self.fileLbl["text"] == "" and self.id > 0):
            self.id -= 1
            self.fileLbl.config(text=self.fitDb.select(self.id, "FilePath"))

        self.reset()

    def fullLeft(self):
        self.id = 1
        self.reset()
        
            

    
        
