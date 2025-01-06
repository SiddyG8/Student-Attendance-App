"""
Codebase is outdated and needs to be completely overhauled to work with the new versions of customtkinter as it was
made for a much older version of the library (v4). The codebase is also very messy and needs to be cleaned up.
"""
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
import datetime as dt
import ctypes
import math
import csv

# Filepaths
DATA_FILE = "data/data.csv"
ROLL_FILE = "data/roll.csv"
NOTES_FILE = "data/notes.csv"

# Scale factor to support dynamic scaling
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

# Searching and sorting algorithms
class Sort:
    # Input: Unsorted array (Integer or String Array)
    # Process: Starts looping through the array and comparing every value unitl it finds
    # the minimum value and swaps it with the current element. This is repeated until the
    # array is sorted.
    # Output: Sorted array (Integer or String Array)
    @staticmethod
    def selectionSort(array):
        for i in range(len(array)):
            minIndex = i
            for j in range(i + 1, len(array)):
                if array[minIndex] > array[j]:
                    minIndex = j
            array[minIndex], array[i] = array[i], array[minIndex]
        return array

    # Input: Unsorted array (Integer or String Array)
    # Process: Sorts array by using a pivot and re-arranging the array so that all values
    # lower than the pivot are below it and vice versa, then it recursively calls itself
    # until the array is sorted.
    # Output: Sorted array (Integer or String Array)
    @staticmethod
    def quickSort(array, start, end):
        if start < end:
            # Generate partitions
            partition = Sort.partition(array, start, end)

            # Sort elements before pivot
            Sort.quickSort(array, start, partition - 1)

            # Sort elements after pivot
            Sort.quickSort(array, partition + 1, end)
        return array

    @staticmethod
    def partition(array, start, end):
        pivotIndex = start
        pivot = array[pivotIndex]

        # Find pivot index to create partiions with
        while start < end:
            # Find end of 1st partition
            while start < len(array) and array[start] <= pivot:
                start += 1

            # Find start of 2nd partition
            while array[end] > pivot:
                end -= 1

            # Insert pivot into the correct postion
            if start < end:
                array[start], array[end] = array[end], array[start]

        # Insert pivot into the correction position
        array[end], array[pivotIndex] = array[pivotIndex], array[end]
        return end

class Search:
    # Input: Array and item to be found (Integer or String Array, Integer or String)
    # Process: Loops through the array until item is found or the end is reached
    # Output: Index of item in array or -1 if item is not in array (Integer)
    @staticmethod
    def linearSearch(array, item):
        for i in range(len(array)):
            if array[i] == item:
                return i
        return -1

    # Input: Sorted array and item to be found (Integer or String Array, Integer or String)
    # Process: Selects mid point in array and compares it to the desired item,
    # if item is lower than the mid point then the upper half is discarded and vice versa.
    # This is repeated until the value is found in the array or it is does not exist.
    # Output: Index of item in array or -1 if item is not in array (Integer)
    @staticmethod
    def binarySearch(array, item):
        low = 0
        high = len(array) - 1
        while low <= high:
            mid = (low + high) // 2
            if item == array[mid]:
                return mid
            elif item > array[mid]:
                low = mid + 1
            else:
                high = mid - 1
        return -1

# Custom widget
class Messagebox(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Variables
        self.value = None

    @classmethod
    def showinfo(cls, title=None, text=None, *args, **kwargs):
        self = cls(*args, **kwargs)

        # Window setup
        self.width = 250
        self.height = max(math.ceil(len(text) / (15 * scale_factor)), len(text.split("\n"))) * 15 + 100
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title(f"{title if title is not None else ''}")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Images
        open = Image.open("images/info_icon.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgIcon = ImageTk.PhotoImage(resize)

        # Fonts
        self.fontMain = ("Inter", -13)

        # Labels
        self.lblIcon = CTkLabel(
            self,
            image=self.imgIcon,
            width=50,
            height=50,
            corner_radius=0
        )
        self.lblMessage = CTkLabel(
            self,
            width=180,
            text=text,
            text_font=self.fontMain,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )

        # Buttons
        self.btnOK = CTkButton(
            self,
            text="OK",
            width=90,
            command=self.close,
            text_font=self.fontMain
        )

        # Widget placement
        self.lblIcon.grid(row=1, column=1)
        self.lblMessage.grid(row=1, column=2)
        self.btnOK.grid(row=2, column=1, columnspan=2, pady=(20, 0))

        # Grid configuration
        self.columnconfigure((0, 3), weight=1, uniform="columns")
        self.rowconfigure((0, 3), weight=1, uniform="rows")

        # System binds
        self.bind("<Escape>", lambda x: self.close())
        self.bind("<Return>", lambda x: self.close())
        self.mainloop()

        # Return value
        return self.value

    @classmethod
    def showwarning(cls, title=None, text=None, *args, **kwargs):
        self = cls(*args, **kwargs)

        # Window setup
        self.width = 250
        self.height = max(math.ceil(len(text) / (15 * scale_factor)), len(text.split("\n"))) * 15 + 100
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title(f"{title if title is not None else ''}")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Images
        open = Image.open("images/warning_icon.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgIcon = ImageTk.PhotoImage(resize)

        # Fonts
        self.fontMain = ("Inter", -13)

        # Labels
        self.lblIcon = CTkLabel(
            self,
            image=self.imgIcon,
            width=50,
            height=50,
            corner_radius=0
        )
        self.lblMessage = CTkLabel(
            self,
            width=180,
            text=text,
            text_font=self.fontMain,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )

        # Buttons
        self.btnOK = CTkButton(
            self,
            text="OK",
            width=90,
            command=self.close,
            text_font=self.fontMain
        )

        # Widget placement
        self.lblIcon.grid(row=1, column=1)
        self.lblMessage.grid(row=1, column=2)
        self.btnOK.grid(row=2, column=1, columnspan=2, pady=(20, 0))

        # Grid configuration
        self.columnconfigure((0, 3), weight=1, uniform="columns")
        self.rowconfigure((0, 3), weight=1, uniform="rows")

        # System binds
        self.bind("<Escape>", lambda x: self.close())
        self.bind("<Return>", lambda x: self.close())
        self.mainloop()

        # Return value
        return self.value

    @classmethod
    def showerror(cls, title=None, text=None, *args, **kwargs):
        self = cls(*args, **kwargs)

        # Window setup
        self.width = 250
        self.height = max(math.ceil(len(text) / (15 * scale_factor)), len(text.split("\n"))) * 15 + 100
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title(f"{title if title is not None else ''}")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Images
        open = Image.open("images/error_icon.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgIcon = ImageTk.PhotoImage(resize)

        # Fonts
        self.fontMain = ("Inter", -13)

        # Labels
        self.lblIcon = CTkLabel(
            self,
            image=self.imgIcon,
            width=50,
            height=50,
            corner_radius=0
        )
        self.lblMessage = CTkLabel(
            self,
            width=180,
            text=text,
            text_font=self.fontMain,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )

        # Buttons
        self.btnOK = CTkButton(
            self,
            text="OK",
            width=90,
            command=self.close,
            text_font=self.fontMain
        )

        # Widget placement
        self.lblIcon.grid(row=1, column=1)
        self.lblMessage.grid(row=1, column=2)
        self.btnOK.grid(row=2, column=1, columnspan=2, pady=(20, 0))

        # Grid configuration
        self.columnconfigure((0, 3), weight=1, uniform="columns")
        self.rowconfigure((0, 3), weight=1, uniform="rows")

        # System binds
        self.bind("<Escape>", lambda x: self.close())
        self.bind("<Return>", lambda x: self.close())
        self.mainloop()

        # Return value
        return self.value

    @classmethod
    def askyesno(cls, title=None, text=None, *args, **kwargs):
        self = cls(*args, **kwargs)

        # Window setup
        self.width = 200
        self.height = max(math.ceil(len(text) / (15 * scale_factor)), len(text.split("\n"))) * 15 + 100
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title(f"{title if title is not None else ''}")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Fonts
        self.fontTitle = ("Inter", -18, "bold")
        self.fontMain = ("Inter", -13)

        self.lblMessage = CTkLabel(
            self,
            width=180,
            text=text,
            text_font=self.fontMain,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )

        # Buttons
        self.btnYes = CTkButton(
            self,
            text="Y\u0332es",
            width=60,
            text_font=self.fontMain,
            command=lambda: self.close(True)
        )
        self.btnNo = CTkButton(
            self,
            text="N\u0332o",
            width=60,
            text_font=self.fontMain,
            command=lambda: self.close(False)
        )

        # Widget placement
        self.lblMessage.grid(row=1, column=1, columnspan=2)
        self.btnYes.grid(row=2, column=1, pady=(20, 0))
        self.btnNo.grid(row=2, column=2, pady=(20, 0))

        # Grid configuration
        self.columnconfigure((0, 3), weight=1, uniform="columns")
        self.rowconfigure((0, 3), weight=1, uniform="rows")

        # System binds
        self.protocol("WM_DELETE_WINDOW", lambda: self.close(False))
        self.bind("<Return>", lambda x: self.close(True))
        self.bind("<y>", lambda x: self.close(True))
        self.bind("<n>", lambda x: self.close(False))
        self.mainloop()

        # Return value
        return self.value

    def close(self, value=None):
        self.value = value
        self.destroy()
        self.quit()

class Note(CTkFrame):
    def __init__(self, *args, title=None, content=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 10, "bold")

        # Labels
        self.lblTitle = CTkLabel(
            self,
            width=kwargs["width"] - 10,
            text=title,
            text_font=self.font2,
            wraplength=self.winfo_reqwidth() - 15,
            justify="left",
            anchor="w",
            corner_radius=0
        )
        self.lblTitle.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblContent = CTkLabel(
            self,
            width=kwargs["width"] - 10,
            text=content,
            text_font=self.font1,
            wraplength=self.winfo_reqwidth() - 15,
            justify="left",
            anchor="w",
            corner_radius=0
        )
        self.lblContent.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix

        # Widget placement
        self.lblTitle.grid(row=0, column=0, padx=(10, 0), pady=(5, 0), sticky="w")
        self.lblContent.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="w")

    def setTitle(self, title):
        self.lblTitle.configure(text=title)

    def setContent(self, content):
        self.lblContent.configure(text=content)

# Users
class User:
    roles = {
        0: "Student",
        1: "Parent",
        2: "Teacher",
        3: "Administrator"
    }

    def __init__(self, username, password, first, last, email, tier):
        self.username = username
        self.password = password
        self.first = first
        self.last = last
        self.email = email
        self.tier = int(tier)

    @property
    def role(self):
        return User.roles[self.tier]

class Student(User):
    rollStates = {
        0: "Unmarked",
        1: "Present",
        2: "Late",
        3: "Absent"
    }
    rollColours = {
        0: "#BEBEBE",
        1: "#50C878",
        2: "#FFBF00",
        3: "#AA4A44"
    }

    def __init__(self, username, password, first, last, email, tier, _dob, group):
        super().__init__(username, password, first, last, email, tier)

        self._dob = dt.date.fromisoformat(_dob)
        self.group = group

    @property
    def dob(self):
        return self._dob.strftime("%d/%m/%Y")

    @property
    def age(self):
        today = dt.date.today()
        age = today.year - self._dob.year

        # Month/day correction
        if dt.date(1, today.month, today.day) < dt.date(1, self._dob.month, self._dob.day):
            age -= 1

        return age

    @property
    def today(self):
        today = dt.date.today()
        status = 0

        # Read data from roll file
        with open(ROLL_FILE) as rollFile:
            reader = csv.reader(rollFile)
            for row in reader:
                if row[0] == self.username and dt.date.fromisoformat(row[2]) == today:
                    status = int(row[3])

        # Return roll state
        return status

    @property
    def notes(self):
        notes = {}
        with open(NOTES_FILE) as notesFile:
            reader = csv.reader(notesFile)
            for row in reader:
                if row[0] == self.username:
                    notes[row[1]] = row[2]

        return notes

    def weekView(self, date=None):
        if date is None:
            date = dt.date.today()

        # Starting and ending dates
        start = date - dt.timedelta(date.weekday())
        end = start + dt.timedelta(4)

        # Read roll from file
        states = {}
        with open(ROLL_FILE) as rollFile:
            reader = csv.reader(rollFile)
            for row in reader:
                date = dt.date.fromisoformat(row[2])
                if row[0] == self.username and start <= date <= end:
                    states[date.weekday()] = int(row[3])

        # Add any missing elements
        for i in range(5):
            if i not in states:
                states[i] = 0

        # Return dictionary of roll for the week
        return states

    @classmethod
    def fromParent(cls, child):
        with open(DATA_FILE) as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                if row[0] == child:
                    return cls(*row)

class Parent(User):
    def __init__(self, username, password, first, last, email, tier, child):
        super().__init__(username, password, first, last, email, tier)

        self.child = Student.fromParent(child)

# User/Class data
class ChangePassword(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.width = 300
        self.height = 300
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title("Password Management")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Fonts
        self.font1 = ("Inter", -19, "bold")
        self.font2 = ("Consolas", -18)
        self.font3 = ("Inter", -16)

        # Labels
        self.lblTitle = CTkLabel(
            self,
            text="Change Password",
            text_font=self.font1
        )

        # Entries
        self.entPassword = CTkEntry(
            self,
            width=200,
            height=30,
            placeholder_text="New Password",
            text_font=self.font2,
            show="•"
        )
        self.entConfirm = CTkEntry(
            self,
            width=200,
            height=30,
            placeholder_text="Confirm Password",
            text_font=self.font2,
            show="•"
        )

        # Buttons
        self.switchShowPassword = CTkSwitch(
            self,
            text="Show Passwords",
            command=self.showPassword
        )
        self.btnCancel = CTkButton(
            self,
            width=80,
            height=35,
            text="Cancel",
            text_font=self.font3,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.destroy
        )
        self.btnSubmit = CTkButton(
            self,
            width=80,
            height=35,
            text="Submit",
            text_font=self.font3,
            command=self.submit
        )

        # Widget placement
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=(20, 15))
        self.entPassword.grid(row=1, column=0, columnspan=2, pady=15)
        self.entConfirm.grid(row=2, column=0, columnspan=2, pady=15)
        self.switchShowPassword.grid(row=3, column=0, columnspan=2, pady=0)
        self.btnCancel.grid(row=4, column=0, padx=10, pady=30, sticky="e")
        self.btnSubmit.grid(row=4, column=1, padx=10, pady=30, sticky="w")

        # Grid configuration
        self.columnconfigure((0, 1), weight=1, uniform="columns")

        # System binds
        self.bind("<Return>", lambda x: self.submit())
        self.bind("<Escape>", lambda x: self.destroy())
        self.entPassword.bind("<FocusIn>", lambda x: self.accent(self.entPassword, 1), add=True)
        self.entPassword.bind("<FocusOut>", lambda x: self.accent(self.entPassword, 0), add=True)
        self.entConfirm.bind("<FocusIn>", lambda x: self.accent(self.entConfirm, 1), add=True)
        self.entConfirm.bind("<FocusOut>", lambda x: self.accent(self.entConfirm, 0), add=True)

    def submit(self):
        global user
        password = self.entPassword.get()
        confirm = self.entConfirm.get()

        if not password or not confirm:
            Messagebox.showwarning("Fields Blank", "Please enter a password.", master=self)
        elif password != confirm:
            Messagebox.showerror("Password Mismatch", "Passwords do not match.", master=self)
        elif password == user.password:
            message = "New password cannot be the same as the current password."
            Messagebox.showerror("Old Password", message, master=self)
        else:
            # Reading old data
            oldData = []
            userData = []
            with open(DATA_FILE) as dataFile:
                reader = csv.reader(dataFile)
                for row in reader:
                    if row[0] == user.username:
                        userData = row
                    else:
                        oldData.append(row)

            # Writing new data
            user.password = password
            userData[1] = user.password
            with open(DATA_FILE, "w") as dataFile:
                writer = csv.writer(dataFile, quoting=csv.QUOTE_ALL, lineterminator="\n")
                for row in oldData:
                    writer.writerow(row)
                writer.writerow(userData)

            # Show message and exit
            Messagebox.showinfo("Success", "Password was changed successfully.", master=self)
            self.destroy()

    def showPassword(self):
        state = self.switchShowPassword.get()
        if state == 1:
            self.entPassword.configure(show="")
            self.entConfirm.configure(show="")
        else:
            self.entPassword.configure(show="•")
            self.entConfirm.configure(show="•")

    @staticmethod
    def accent(widget, state):
        colours = {
            1: ("#0969DA", "#58A6FF"),
            0: ("#979DA2", "#565B5E")
        }
        widget.configure(border_color=colours[state])

class CreateNote(CTkToplevel):
    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.width = 400
        self.height = 400
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title("Note Creation")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Variables
        self.student = student
        self.placeholderActive = True

        # Fonts
        self.font1 = ("Inter", 12)
        self.font2 = ("Inter", 14, "bold")
        self.font3 = ("Consolas", 14)

        # Labels
        self.lblTitle = CTkLabel(
            self,
            text="Create Note",
            text_font=self.font2
        )

        # Entries
        self.entTitle = CTkEntry(
            self,
            width=300,
            height=30,
            placeholder_text="Note Title",
            text_font=self.font3
        )
        self.frameContent = CTkFrame(
            self,
            fg_color=("#F9F9FA", "#343638"),
            border_color=("#979DA2", "#565B5E"),
            border_width=2
        )
        self.textContent = Text(
            self.frameContent,
            width=29,
            height=8,
            font=self.font3,
            bg="#F9F9FA",
            fg="gray52",
            insertbackground="gray10",
            relief="flat",
            highlightthickness=0,
            bd=0
        )
        self.textContent.insert(1.0, "Note Content")

        # Buttons
        self.btnCancel = CTkButton(
            self,
            width=80,
            height=35,
            text="Cancel",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.destroy
        )
        self.btnSubmit = CTkButton(
            self,
            width=80,
            height=35,
            text="Submit",
            text_font=self.font1,
            command=self.submit
        )

        # Widget placement
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=20)
        self.entTitle.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.frameContent.grid(row=2, column=0, columnspan=2, pady=10)
        self.textContent.grid(row=0, column=0, padx=6, pady=6)
        self.btnCancel.grid(row=3, column=0, padx=10, pady=20, sticky="e")
        self.btnSubmit.grid(row=3, column=1, padx=10, pady=20, sticky="w")

        # Grid configuration
        self.columnconfigure((0, 1), weight=1, uniform="columns")

        # System binds
        self.bind("<Escape>", lambda x: self.destroy())
        self.entTitle.bind("<FocusIn>", lambda x: self.accent(self.entTitle, 1), add=True)
        self.entTitle.bind("<FocusOut>", lambda x: self.accent(self.entTitle, 0), add=True)
        self.textContent.bind("<FocusIn>", lambda x: self.accent(self.frameContent, 1))
        self.textContent.bind("<FocusOut>", lambda x: self.accent(self.frameContent, 0))
        self.textContent.bind("<FocusIn>", lambda x: self.focusIn(), add=True)
        self.textContent.bind("<FocusOut>", lambda x: self.focusOut(), add=True)
        if get_appearance_mode() == "Dark":
            self.textContent.configure(bg="#343638")
            self.textContent.configure(fg="gray62")
            self.textContent.configure(insertbackground="#DCE4EE")

    def submit(self):
        title = self.entTitle.get()
        content = self.textContent.get(1.0, END)

        # Reading old data
        oldData = []
        with open(NOTES_FILE) as rollFile:
            reader = csv.reader(rollFile)
            for row in reader:
                oldData.append(row)
        titles = [row[0] for row in oldData]

        if not title or content == "\n" or self.placeholderActive:
            message = "Please enter a message and title."
            Messagebox.showwarning("Fields Blank", message, master=self)
        elif title in titles:
            message = "A note with this title already exists, please choose a new title."
            Messagebox.showerror("Title Taken", message, master=self)
        elif len(title) > 28:
            message = "The title cannot be longer than 28 characters."
            Messagebox.showerror("Title Too Long", message, master=self)
        elif len(content) > 233:
            message = "The message cannot be longer than 232 characters."
            Messagebox.showerror("Message Too Long", message, master=self)
        else:
            # Writing new data
            noteData = [self.student.username, title, content[:-1]]
            with open(NOTES_FILE, "w") as rollFile:
                writer = csv.writer(rollFile, quoting=csv.QUOTE_ALL, lineterminator="\n")
                for row in oldData:
                    writer.writerow(row)
                writer.writerow(noteData)

            # Show message and exit
            Messagebox.showinfo("Success", "Note was created successfully.", master=self)
            self.master.createNotes(update=True)
            self.destroy()

    def focusIn(self):
        if self.placeholderActive:
            self.placeholderActive = False
            self.textContent.delete(1.0, END)
            if get_appearance_mode() == "Dark":
                self.textContent.configure(fg="#DCE4EE")
            else:
                self.textContent.configure(fg="gray10")

    def focusOut(self):
        if self.textContent.get(1.0, END) == "\n":
            self.placeholderActive = True
            self.textContent.insert(1.0, "Note Content")
            if get_appearance_mode() == "Dark":
                self.textContent.configure(fg="gray62")
            else:
                self.textContent.configure(fg="gray52")

    @staticmethod
    def accent(widget, state):
        colours = {
            1: ("#0969DA", "#58A6FF"),
            0: ("#979DA2", "#565B5E")
        }
        widget.configure(border_color=colours[state])

# Roll/Attendance
class ViewAttendance(CTkToplevel):
    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.width = 350
        self.height = 400
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title("Attendance Records")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Variables
        self.student = student
        self.weekview = self.student.weekView()
        self.start = dt.date.today() - dt.timedelta(dt.date.today().weekday())
        self.end = self.start + dt.timedelta(4)

        # Images
        open = Image.open("images/arrow_left.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgLeft = ImageTk.PhotoImage(resize)
        open = Image.open("images/arrow_right.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgRight = ImageTk.PhotoImage(resize)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 12, "bold")
        self.font3 = ("Inter", 10, "bold")

        # Frames
        self.frameStatus1 = CTkFrame(
            self,
            width=75,
            height=25,
            fg_color=Student.rollColours[self.weekview[0]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.frameStatus2 = CTkFrame(
            self,
            width=75,
            height=25,
            fg_color=Student.rollColours[self.weekview[1]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.frameStatus3 = CTkFrame(
            self,
            width=75,
            height=25,
            fg_color=Student.rollColours[self.weekview[2]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.frameStatus4 = CTkFrame(
            self,
            width=75,
            height=25,
            fg_color=Student.rollColours[self.weekview[3]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.frameStatus5 = CTkFrame(
            self,
            width=75,
            height=25,
            fg_color=Student.rollColours[self.weekview[4]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )

        # Labels
        self.lblUserInfo = CTkLabel(
            self,
            text=f"{user.first} {user.last} ({user.username})",
            text_font=self.font3,
            text_color=("#0969DA", "#58A6FF"),
            justify=LEFT,
            anchor=W
        )
        self.lblUserInfo.text_label.grid_configure(sticky=W) # <- CTkLabel anchor fix
        self.lblTitle = CTkLabel(
            self,
            text=f"""{"Your" if user.tier == 0 else f"{student.first}'s"} Weekly Attendance""",
            text_font=self.font2
        )
        self.lblDates = CTkLabel(
            self,
            text=f"{self.start.strftime('%d/%m/%Y')} - {self.end.strftime('%d/%m/%Y')}",
            text_font=self.font1
        )
        self.lblDay1 = CTkLabel(
            self,
            text="Monday:",
            text_font=self.font1
        )
        self.lblDay2 = CTkLabel(
            self,
            text="Tuesday:",
            text_font=self.font1
        )
        self.lblDay3 = CTkLabel(
            self,
            text="Wednesday:",
            text_font=self.font1
        )

        self.lblDay4 = CTkLabel(
            self,
            text="Thursday:",
            text_font=self.font1
        )
        self.lblDay5 = CTkLabel(
            self,
            text="Friday:",
            text_font=self.font1
        )

        # Buttons
        self.btnExit = CTkButton(
            self,
            width=50,
            text="Exit",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.destroy
        )
        self.btnLeft = CTkButton(
            self,
            width=50,
            text=None,
            image=self.imgLeft,
            bg_color=("#EBEBEC", "#212325"),
            fg_color=("#EBEBEC", "#212325"),
            hover=False,
            corner_radius=0,
            command=lambda: self.scroll(-7)
        )
        self.btnRight = CTkButton(
            self,
            width=50,
            text=None,
            image=self.imgRight,
            bg_color=("#EBEBEC", "#212325"),
            fg_color=("#EBEBEC", "#212325"),
            hover=False,
            corner_radius=0,
            command=lambda: self.scroll(7)
        )
        self.btnToday = CTkButton(
            self,
            width=100,
            text="Today",
            command=lambda: self.scroll(0, today=True)
        )

        # Widget placement
        self.lblUserInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.btnExit.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="e")
        self.lblTitle.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        self.btnLeft.grid(row=2, column=0, padx=(10, 0))
        self.lblDates.grid(row=2, column=1, columnspan=2)
        self.btnRight.grid(row=2, column=3, padx=(0, 10))
        self.lblDay1.grid(row=3, column=1)
        self.lblDay2.grid(row=4, column=1)
        self.lblDay3.grid(row=5, column=1)
        self.lblDay4.grid(row=6, column=1)
        self.lblDay5.grid(row=7, column=1)
        self.frameStatus1.grid(row=3, column=2, pady=8)
        self.frameStatus2.grid(row=4, column=2, pady=8)
        self.frameStatus3.grid(row=5, column=2, pady=8)
        self.frameStatus4.grid(row=6, column=2, pady=8)
        self.frameStatus5.grid(row=7, column=2, pady=8)
        self.btnToday.grid(row=8, column=1, columnspan=2, pady=12)

        # Grid configuration
        self.columnconfigure((1, 2), weight=1, uniform="columns")

        # System binds
        self.bind("<Escape>", lambda x: self.destroy())

    def scroll(self, days, *, today=False):
        # Today functionality
        if today:
            self.start = dt.date.today() - dt.timedelta(dt.date.today().weekday())
        else:
            self.start += dt.timedelta(days)

        # New data
        self.end = self.start + dt.timedelta(4)
        self.weekview = self.student.weekView(self.start)

        newDate = dt.date.today() + dt.timedelta(days)
        newData = self.student.weekView(newDate)

        # Updating GUI
        self.frameStatus1.configure(fg_color=Student.rollColours[self.weekview[0]])
        self.frameStatus2.configure(fg_color=Student.rollColours[self.weekview[1]])
        self.frameStatus3.configure(fg_color=Student.rollColours[self.weekview[2]])
        self.frameStatus4.configure(fg_color=Student.rollColours[self.weekview[3]])
        self.frameStatus5.configure(fg_color=Student.rollColours[self.weekview[4]])
        self.lblDates.configure(text=f"{self.start.strftime('%d/%m/%Y')} - {self.end.strftime('%d/%m/%Y')}")

class EditAttendance(CTkToplevel):
    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.width = 620
        self.height = 400
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title("Attendance Records")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Variables
        self.student = student
        self.weekview = self.student.weekView()
        self.start = dt.date.today() - dt.timedelta(dt.date.today().weekday())
        self.end = self.start + dt.timedelta(4)

        # Images
        open = Image.open("images/arrow_left.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgLeft = ImageTk.PhotoImage(resize)
        open = Image.open("images/arrow_right.png")
        resize = open.resize((int(40 * scale_factor), int(40 * scale_factor)))
        self.imgRight = ImageTk.PhotoImage(resize)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 12, "bold")
        self.font3 = ("Inter", 10, "bold")

        # Frames
        self.btnStatus1 = CTkButton(
            self,
            width=75,
            height=25,
            text=None,
            fg_color=Student.rollColours[self.weekview[0]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            hover=False,
            command=lambda: self.changeState(0),
            state="disabled"
        )
        self.btnStatus2 = CTkButton(
            self,
            width=75,
            height=25,
            text=None,
            fg_color=Student.rollColours[self.weekview[1]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            hover=False,
            command=lambda: self.changeState(1),
            state="disabled"
        )
        self.btnStatus3 = CTkButton(
            self,
            width=75,
            height=25,
            text=None,
            fg_color=Student.rollColours[self.weekview[2]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            hover=False,
            command=lambda: self.changeState(2),
            state="disabled"
        )
        self.btnStatus4 = CTkButton(
            self,
            width=75,
            height=25,
            text=None,
            fg_color=Student.rollColours[self.weekview[3]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            hover=False,
            command=lambda: self.changeState(3),
            state="disabled"
        )
        self.btnStatus5 = CTkButton(
            self,
            width=75,
            height=25,
            text=None,
            fg_color=Student.rollColours[self.weekview[4]],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            hover=False,
            command=lambda: self.changeState(4),
            state="disabled"
        )

        # Labels
        self.lblUserInfo = CTkLabel(
            self,
            text=f"{user.first} {user.last} ({user.username})",
            text_font=self.font3,
            text_color=("#0969DA", "#58A6FF"),
            justify=LEFT,
            anchor=W
        )
        self.lblUserInfo.text_label.grid_configure(sticky=W) # <- CTkLabel anchor fix
        self.lblTitle = CTkLabel(
            self,
            text=f"{self.student.first}'s Weekly Attendance",
            text_font=self.font2
        )
        self.lblDates = CTkLabel(
            self,
            text=f"{self.start.strftime('%d/%m/%Y')} - {self.end.strftime('%d/%m/%Y')}",
            text_font=self.font1
        )
        self.lblDay1 = CTkLabel(
            self,
            text="Monday:",
            text_font=self.font1
        )
        self.lblDay2 = CTkLabel(
            self,
            text="Tuesday:",
            text_font=self.font1
        )
        self.lblDay3 = CTkLabel(
            self,
            text="Wednesday:",
            text_font=self.font1
        )

        self.lblDay4 = CTkLabel(
            self,
            text="Thursday:",
            text_font=self.font1
        )
        self.lblDay5 = CTkLabel(
            self,
            text="Friday:",
            text_font=self.font1
        )

        # Buttons
        self.btnExit = CTkButton(
            self,
            width=50,
            text="Exit",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.destroy
        )
        self.btnLeft = CTkButton(
            self,
            width=50,
            text=None,
            image=self.imgLeft,
            bg_color=("#EBEBEC", "#212325"),
            fg_color=("#EBEBEC", "#212325"),
            hover=False,
            corner_radius=0,
            command=lambda: self.scroll(-7)
        )
        self.btnRight = CTkButton(
            self,
            width=50,
            text=None,
            image=self.imgRight,
            bg_color=("#EBEBEC", "#212325"),
            fg_color=("#EBEBEC", "#212325"),
            hover=False,
            corner_radius=0,
            command=lambda: self.scroll(7)
        )
        self.lblData = CTkLabel(
            self,
            text=f"{self.student.first}'s Attendance Notes",
            text_font=self.font2
        )
        self.frameNote = CTkFrame(
            self,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )
        self.note = Note(
            self.frameNote,
            width=180,
            height=180,
            title="No Notes",
            content="There are no notes to display.",
            fg_color=("#C0C2C5", "#343638"),
            corner_radius=10
        )
        self.btnBack = CTkButton(
            self.frameNote,
            width=80,
            text="Previous",
            text_font=self.font1,
            command=lambda: self.scrollNote(-1)
        )
        self.btnNext = CTkButton(
            self.frameNote,
            width=80,
            text="Next",
            text_font=self.font1,
            command=lambda: self.scrollNote(1)
        )
        self.btnCreateNote = CTkButton(
            self.frameNote,
            width=110,
            height=28,
            text="Create Note",
            text_font=self.font1,
            command=lambda: CreateNote(self.student, master=self)
        )
        self.btnDeleteNote = CTkButton(
            self.frameNote,
            width=110,
            height=28,
            text="Delete Note",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.deleteNote
        )
        self.btnEditAndSave = CTkButton(
            self,
            width=100,
            text="Edit",
            command=self.edit
        )
        self.btnTodayAndCancel = CTkButton(
            self,
            width=100,
            text="Today",
            command=lambda: self.scroll(0, today=True)
        )

        # Widget placement
        self.lblUserInfo.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        self.btnExit.grid(row=0, column=4, columnspan=2, padx=10, pady=10, sticky="e")
        self.lblTitle.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        self.btnLeft.grid(row=2, column=0, padx=(10, 0))
        self.lblDates.grid(row=2, column=1, columnspan=2)
        self.btnRight.grid(row=2, column=3, padx=(0, 10))
        self.lblDay1.grid(row=3, column=1)
        self.lblDay2.grid(row=4, column=1)
        self.lblDay3.grid(row=5, column=1)
        self.lblDay4.grid(row=6, column=1)
        self.lblDay5.grid(row=7, column=1)
        self.btnStatus1.grid(row=3, column=2, pady=8)
        self.btnStatus2.grid(row=4, column=2, pady=8)
        self.btnStatus3.grid(row=5, column=2, pady=8)
        self.btnStatus4.grid(row=6, column=2, pady=8)
        self.btnStatus5.grid(row=7, column=2, pady=8)
        self.btnEditAndSave.grid(row=8, column=0, columnspan=2, padx=10, pady=12, sticky="e")
        self.btnTodayAndCancel.grid(row=8, column=2, columnspan=2, padx=10, pady=12, sticky="w")
        self.lblData.grid(row=1, column=4, pady=(0, 10))
        self.frameNote.grid(row=1, rowspan=8, column=4)
        self.note.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btnBack.grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.btnNext.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        self.btnCreateNote.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.btnDeleteNote.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Grid configuration
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="columns")
        self.columnconfigure(4, weight=3, uniform="columns")

        # System binds
        self.bind("<Escape>", lambda x: self.destroy())
        self.createNotes()

    def scroll(self, days, *, today=False):
        # Today functionality
        if today:
            self.start = dt.date.today() - dt.timedelta(dt.date.today().weekday())
        else:
            self.start += dt.timedelta(days)

        # New data
        self.end = self.start + dt.timedelta(4)
        self.weekview = self.student.weekView(self.start)

        # Updating GUI
        self.btnStatus1.configure(fg_color=Student.rollColours[self.weekview[0]])
        self.btnStatus2.configure(fg_color=Student.rollColours[self.weekview[1]])
        self.btnStatus3.configure(fg_color=Student.rollColours[self.weekview[2]])
        self.btnStatus4.configure(fg_color=Student.rollColours[self.weekview[3]])
        self.btnStatus5.configure(fg_color=Student.rollColours[self.weekview[4]])
        self.lblDates.configure(text=f"{self.start.strftime('%d/%m/%Y')} - {self.end.strftime('%d/%m/%Y')}")

    def changeState(self, day):
        self.weekview[day] = self.weekview[day] + 1 if self.weekview[day] + 1 <= 3 else 0

        # Updating GUI
        self.btnStatus1.configure(fg_color=Student.rollColours[self.weekview[0]])
        self.btnStatus2.configure(fg_color=Student.rollColours[self.weekview[1]])
        self.btnStatus3.configure(fg_color=Student.rollColours[self.weekview[2]])
        self.btnStatus4.configure(fg_color=Student.rollColours[self.weekview[3]])
        self.btnStatus5.configure(fg_color=Student.rollColours[self.weekview[4]])

    def edit(self):
        self.btnStatus1.configure(state="normal")
        self.btnStatus2.configure(state="normal")
        self.btnStatus3.configure(state="normal")
        self.btnStatus4.configure(state="normal")
        self.btnStatus5.configure(state="normal")
        self.btnEditAndSave.configure(command=self.save, text="Save")
        self.btnTodayAndCancel.configure(
            text="Cancel",
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.revert
        )

        # Disabling scrolling
        self.btnLeft.configure(state="disabled")
        self.btnRight.configure(state="disabled")

    def revert(self):
        self.btnStatus1.configure(state="disabled")
        self.btnStatus2.configure(state="disabled")
        self.btnStatus3.configure(state="disabled")
        self.btnStatus4.configure(state="disabled")
        self.btnStatus5.configure(state="disabled")
        self.btnEditAndSave.configure(command=self.edit, text="Edit")
        self.btnTodayAndCancel.configure(
            text="Today",
            text_color=("gray10", "#DCE4EE"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            command=lambda: self.scroll(0, today=True)
        )

        # Updating GUI
        self.weekview = self.student.weekView(self.start)
        self.btnStatus1.configure(fg_color=Student.rollColours[self.weekview[0]])
        self.btnStatus2.configure(fg_color=Student.rollColours[self.weekview[1]])
        self.btnStatus3.configure(fg_color=Student.rollColours[self.weekview[2]])
        self.btnStatus4.configure(fg_color=Student.rollColours[self.weekview[3]])
        self.btnStatus5.configure(fg_color=Student.rollColours[self.weekview[4]])

        # Enabling scrolling
        self.btnLeft.configure(state="normal")
        self.btnRight.configure(state="normal")

    def save(self):
        # Reading old data
        oldData = []
        with open(ROLL_FILE) as rollFile:
            reader = csv.reader(rollFile)
            for row in reader:
                if not self.start <= dt.date.fromisoformat(row[2]) <= self.end:
                    oldData.append(row)

        # Writing new data
        with open(ROLL_FILE, "w") as rollFile:
            writer = csv.writer(rollFile, quoting=csv.QUOTE_ALL, lineterminator="\n")
            for row in oldData:
                writer.writerow(row)
            for weekday in self.weekview:
                date = self.start + dt.timedelta(weekday)
                status = self.weekview[weekday]
                writer.writerow([self.student.username, self.student.group, date.strftime("%Y-%m-%d"), status])

        # Updating GUI
        self.scroll(0)
        self.revert()

    def createNotes(self, *, update=False, delete=False):
        self.notes = self.student.notes
        self.keys = list(self.notes.keys())
        if not update and not delete:
            self.index = 0
        elif delete:
            if self.index != 0:
                self.index -= 1

        # Notes
        if self.notes:
            self.note.setTitle(self.keys[self.index])
            self.note.setContent(self.notes[self.keys[self.index]])
            self.btnDeleteNote.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        else:
            self.note.setTitle("No Notes")
            self.note.setContent("There are no notes to display.")
            self.btnDeleteNote.grid_forget()

        # Disabling
        if len(self.keys) < 2:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="disabled")
        elif self.index == 0:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="normal")
        elif self.index == len(self.keys) - 1:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="disabled")
        else:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="normal")

        # CTkLabel width fix
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def deleteNote(self):
        question = "Are you sure you would like to delete this note?"
        confirm = Messagebox.askyesno("Delete Note", question, master=self)
        if confirm:
            noteTitle = self.keys[self.index]

            # Reading old data
            oldData = []
            with open(NOTES_FILE) as noteFile:
                reader = csv.reader(noteFile)
                for row in reader:
                    if row[1] != noteTitle:
                        oldData.append(row)

            # Writing new data
            with open(NOTES_FILE, "w") as noteFile:
                writer = csv.writer(noteFile, quoting=csv.QUOTE_ALL, lineterminator="\n")
                for row in oldData:
                    writer.writerow(row)

            # Update GUI
            self.createNotes(delete=True)

    def scrollNote(self, offset):
        self.index += offset

        # Updating GUI
        self.note.setTitle(self.keys[self.index])
        self.note.setContent(self.notes[self.keys[self.index]])

        # Disabling
        if self.index == 0:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="normal")
        elif self.index == len(self.keys) - 1:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="disabled")
        else:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="normal")

        # CTkLabel width fix
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

# Main screens
class LoginScreen(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Images
        open = Image.open("images/login_background.png")
        resize = open.resize((int(300 * scale_factor), int(540 * scale_factor)))
        self.imgBackground = ImageTk.PhotoImage(resize)

        # Fonts (SORT THESE OUT ASAP)
        self.font1 = ("Inter", -24, "bold")
        self.font2 = ("Consolas", -19)
        self.font3 = ("Inter", -13)
        self.font4 = ("Inter", -13, "underline")
        self.font5 = ("Inter", -20)
        self.font6 = ("Inter", -18, "bold")

        # Frames
        self.frameGroup = CTkFrame(
            self,
            fg_color= ("#EBEBEC", "#212325"),
            corner_radius=0
        )

        # Labels
        self.lblBackground = CTkLabel(
            self,
            width=300,
            height=self.master.height,
            text=None,
            image=self.imgBackground,
            corner_radius=0
        )
        self.lblTitle = CTkLabel(
            self,
            text="Student Attendance System",
            text_font=self.font1
        )
        self.lblUsername = CTkLabel(
            self,
            width=250,
            text="Username",
            text_font=self.font6,
            justify=LEFT,
            anchor=W,
            corner_radius=0
        )
        self.lblUsername.text_label.grid_configure(sticky=W) # <- CTkLabel anchor fix
        self.lblPassword = CTkLabel(
            self,
            width=250,
            text="Password",
            text_font=self.font6,
            justify=LEFT,
            anchor=W,
            corner_radius=0
        )
        self.lblPassword.text_label.grid_configure(sticky=W) # <- CTkLabel anchor fix
        self.lblMsg = CTkLabel(
            self.frameGroup,
            width=92,
            height=10,
            text="Unable to login?",
            text_font=self.font3,
            corner_radius=0
        )

        # Entries
        self.entUsername = CTkEntry(
            self,
            placeholder_text="Username",
            text_font=self.font2,
            height=35,
            width=250
        )
        self.entPassword = CTkEntry(
            self,
            placeholder_text="Password",
            text_font=self.font2,
            height=35,
            width=250,
            show="•"
        )

        # Buttons
        self.switchShowPassword = CTkSwitch(
            self,
            text="Show Password",
            command=self.showPassword
        )
        self.btnLogin = CTkButton(
            self,
            width=150,
            height=45,
            text="Login",
            text_font=self.font5,
            command=self.login
        )
        self.btnHelp = CTkButton(
            self.frameGroup,
            text="Display Help",
            text_font=self.font4,
            width=75,
            height=10,
            corner_radius=0,
            fg_color=("#EBEBEC", "#212325"),
            text_color=("#0969DA", "#58A6FF"),
            hover=False,
            border_width=0,
            command=self.help
        )

        # Widget placement
        self.lblBackground.grid(row=0, rowspan=10, column=0, sticky="nsew")
        self.lblTitle.grid(row=0, column=1, pady=(45, 0))
        self.lblUsername.grid(row=2, column=1)
        self.entUsername.grid(row=3, column=1, pady=(0, 40))
        self.lblPassword.grid(row=4, column=1)
        self.entPassword.grid(row=5, column=1)
        self.switchShowPassword.grid(row=6, column=1, pady=10)
        self.btnLogin.grid(row=8, column=1)
        self.frameGroup.grid(row=9, column=1, pady=(2, 60))
        self.lblMsg.grid(row=0, column=0, pady=(1, 0))
        self.btnHelp.grid(row=0, column=1)

        # Grid configuration
        self.columnconfigure(0, weight=5, uniform="columns")
        self.columnconfigure(1, weight=7, uniform="columns")
        self.rowconfigure((1, 7), weight=1, uniform="spacing")

        # System binds
        self.entUsername.bind("<FocusIn>", lambda x: self.accent(self.entUsername, 1), add=True)
        self.entUsername.bind("<FocusOut>", lambda x: self.accent(self.entUsername, 0), add=True)
        self.entPassword.bind("<FocusIn>", lambda x: self.accent(self.entPassword, 1), add=True)
        self.entPassword.bind("<FocusOut>", lambda x: self.accent(self.entPassword, 0), add=True)

    def setBinds(self, master):
        master.bind("<Escape>", lambda x: master.destroy())
        master.bind("<Return>", lambda x: self.login())
        self.switchShowPassword.deselect()

    def login(self):
        global user
        username = self.entUsername.get()
        password = self.entPassword.get()

        if username and password:
            result = False
            with open(DATA_FILE) as dataFile:
                reader = csv.reader(dataFile)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        result = True

                        # Clearing entries
                        self.entUsername.focus_set()
                        self.entUsername.delete(0, END)
                        self.entPassword.delete(0, END)

                        if int(row[5]) == 0:
                            user = Student(*row)
                            self.master.display(self.master.frameStudent, title="Student Interface")
                            self.master.frameStudent.setup()
                        elif int(row[5]) == 1:
                            user = Parent(*row)
                            self.master.display(self.master.frameParent, title="Parent Interface")
                            self.master.frameParent.setup()
                        elif int(row[5]) == 2:
                            user = User(*row)
                            self.master.display(self.master.frameTeacher, title="Teacher Interface")
                            self.master.frameTeacher.setup()
                        elif int(row[5]) == 3:
                            user = User(*row)
                            self.master.display(self.master.frameAdmin, title="Administrator Interface")
                            self.master.frameAdmin.setup()
                        break
            if not result:
                Messagebox.showerror("Login Failed", "Username or Password Incorrect.")
        else:
            Messagebox.showwarning("Fields Blank", "Please enter a username and password.")

    def showPassword(self):
        state = self.switchShowPassword.get()
        if state == 1:
            self.entPassword.configure(show="")
        else:
            self.entPassword.configure(show="•")

    def help(self):
        message = "If you are unable to login please ask an administrator for help."
        Messagebox.showinfo("Login Help", message, master=self)

    @staticmethod
    def accent(widget, state):
        colours = {
            1: ("#0969DA", "#58A6FF"),
            0: ("#979DA2", "#565B5E")
        }
        widget.configure(border_color=colours[state])

class StudentScreen(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 10, "bold")
        self.font3 = ("Inter", 12, "bold")

        # Frames
        self.frameSidebar = CTkFrame(
            self,
            width=200,
            height=self.winfo_width() / scale_factor,
            corner_radius=0
        )
        self.frameMain = CTkFrame(
            self,
            width=480,
            height=self.winfo_width() / scale_factor,
            corner_radius=10
        )
        self.frameStatus = CTkFrame(
            self.frameMain,
            width=75,
            height=25,
            fg_color=Student.rollColours[0],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.spacer = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )


        # Sidebar widgets
        self.lblTitle = CTkLabel(
            self.frameSidebar,
            text="Student Attendance System",
            text_font=self.font3,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )
        self.switchDarkMode = CTkSwitch(
            self.frameSidebar,
            text="Dark Mode",
            text_font=self.font1,
            command=self.changeAppearance
        )

        # Main area widgets
        self.lblUserInfo = CTkLabel(
            self.frameMain,
            text="User (Username)",
            text_font=self.font2,
            text_color=("#0969DA", "#58A6FF"),
            justify="left",
            anchor="w"
        )
        self.lblUserInfo.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblDetails = CTkLabel(
            self.frameMain,
            text="Your Details",
            text_font=self.font3,
            justify="left",
            anchor="w"
        )
        self.lblDetails.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblUsername = CTkLabel(
            self.frameMain,
            width=215,
            text="Username: Username",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblUsername.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblFirstName = CTkLabel(
            self.frameMain,
            width=215,
            text="First Name: First Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblFirstName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblLastName = CTkLabel(
            self.frameMain,
            width=215,
            text="Last Name: Last Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblLastName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblClass = CTkLabel(
            self.frameMain,
            width=215,
            text="Class: Class",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblClass.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblAge = CTkLabel(
            self.frameMain,
            width=215,
            text="Age: Age",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblAge.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblEmail = CTkLabel(
            self.frameMain,
            width=215,
            text="Email: Email",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblEmail.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.btnChangePassword = CTkButton(
            self.frameMain,
            height=28,
            text="Change Password",
            text_font=self.font1,
            command=lambda: ChangePassword(self)
        )
        self.btnLogout = CTkButton(
            self.frameMain,
            width=60,
            text="Logout",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.logout
        )
        self.lblAttendance = CTkLabel(
            self.frameMain,
            width=200,
            text="Your Attendance",
            text_font=self.font3
        )
        self.lblStatus = CTkLabel(
            self.frameMain,
            text="Today's Status:",
            text_font=self.font1,
            corner_radius=0
        )
        self.frameStatus = CTkFrame(
            self.frameMain,
            width=75,
            height=25,
            fg_color=Student.rollColours[0],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.btnAttendance = CTkButton(
            self.frameMain,
            width=110,
            height=28,
            text="View Attendance",
            text_font=self.font1,
            command=lambda: ViewAttendance(user, master=self)
        )
        self.frameNote = CTkFrame(
            self.frameMain,
            width=200,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )
        self.lblNotes = CTkLabel(
            self.frameNote,
            width=180,
            text="Attendance Notes",
            text_font=self.font3
        )
        self.note = Note(
            self.frameNote,
            width=180,
            height=180,
            title="No Notes",
            content="There are no notes to display.",
            fg_color=("#C0C2C5", "#343638"),
            corner_radius=10
        )
        self.btnBack = CTkButton(
            self.frameNote,
            width=80,
            text="Previous",
            text_font=self.font1,
            command=lambda: self.scroll(-1)
        )
        self.btnNext = CTkButton(
            self.frameNote,
            width=80,
            text="Next",
            text_font=self.font1,
            command=lambda: self.scroll(1)
        )

        # Widget placement
        self.frameSidebar.grid(row=0, column=0, sticky="nsew")
        self.lblTitle.grid(row=0, column=0, pady=20)
        self.switchDarkMode.grid(row=2, column=0, pady=30)
        self.frameMain.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.lblUserInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.lblDetails.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        self.lblUsername.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
        self.lblFirstName.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")
        self.lblLastName.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")
        self.lblClass.grid(row=5, column=0, columnspan=2,padx=10, sticky="w")
        self.lblAge.grid(row=6, column=0, columnspan=2, padx=10, sticky="w")
        self.lblEmail.grid(row=7, column=0, columnspan=2, padx=10, sticky="w")
        self.btnChangePassword.grid(row=8, column=0, columnspan=2, padx=16, pady=10, sticky="w")
        self.spacer.grid(row=9, column=0, columnspan=2, sticky="ns")
        self.btnLogout.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.lblAttendance.grid(row=1, column=2, columnspan=2)
        self.lblStatus.grid(row=2, column=2, sticky="e")
        self.frameStatus.grid(row=2, column=3, stick="w")
        self.btnAttendance.grid(row=3, rowspan=2, column=2, columnspan=2, pady=10)
        self.frameNote.grid(row=5, rowspan=5, column=2, columnspan=2, sticky="n")
        self.lblNotes.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 10))
        self.note.grid(row=1, column=0, columnspan=2)
        self.btnBack.grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.btnNext.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        # Grid configuration
        self.columnconfigure(0, weight=5, uniform="columns")
        self.columnconfigure(1, weight=13, uniform="columns")
        self.rowconfigure(0, weight=1, uniform="rows")
        self.frameSidebar.columnconfigure(0, weight=1, uniform="columns1")
        self.frameSidebar.rowconfigure(1, weight=1, uniform="spacing")
        self.frameMain.columnconfigure((0, 1, 2, 3), weight=1, uniform="columns2")
        self.frameMain.rowconfigure(9, weight=1, uniform="spacing1")

    def setBinds(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.logout())
        master.bind("<Escape>", lambda x: self.logout())
        if get_appearance_mode() == "Dark":
            self.switchDarkMode.select()

    def setup(self):
        self.lblUserInfo.configure(text=f"{user.first} {user.last} ({user.username})")
        self.lblUsername.configure(text=f"Username: {user.username}")
        self.lblFirstName.configure(text=f"First Name: {user.first}")
        self.lblLastName.configure(text=f"Last Name: {user.last}")
        self.lblClass.configure(text=f"Class: {user.group}")
        self.lblAge.configure(text=f"Age: {user.age} years ({user.dob})")
        self.lblEmail.configure(text=f"Email: {user.email}")
        self.frameStatus.configure(fg_color=Student.rollColours[user.today])
        self.createNotes()

        # CTkLabel width fix
        self.lblUsername.canvas.configure(width=int(215 * scale_factor))
        self.lblFirstName.canvas.configure(width=int(215 * scale_factor))
        self.lblLastName.canvas.configure(width=int(215 * scale_factor))
        self.lblClass.canvas.configure(width=int(215 * scale_factor))
        self.lblAge.canvas.configure(width=int(215 * scale_factor))
        self.lblEmail.canvas.configure(width=int(215 * scale_factor))
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.lblUsername.text_label.configure(width=27)
        self.lblFirstName.text_label.configure(width=27)
        self.lblLastName.text_label.configure(width=27)
        self.lblClass.text_label.configure(width=27)
        self.lblAge.text_label.configure(width=27)
        self.lblEmail.text_label.configure(width=27)
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def createNotes(self):
        self.notes = user.notes
        self.keys = list(self.notes.keys())
        self.index = 0

        if self.notes:
            self.note.setTitle(self.keys[self.index])
            self.note.setContent(self.notes[self.keys[self.index]])

        # Disabling
        self.btnBack.configure(state="disabled")
        if len(self.keys) < 2:
            self.btnNext.configure(state="disabled")

    def scroll(self, offset):
        self.index += offset

        # Updating GUI
        self.note.setTitle(self.keys[self.index])
        self.note.setContent(self.notes[self.keys[self.index]])

        # Disabling
        if self.index == 0:
            self.btnBack.configure(state="disabled")
        elif self.index == len(self.keys) - 1:
            self.btnNext.configure(state="disabled")
        else:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="normal")

        # CTkLabel width fix
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def logout(self):
        question = "Are you sure you would like to logout?"
        confirm = Messagebox.askyesno("Exit", question, master=self.master)
        if confirm:
            self.master.display(self.master.frameLogin, title="Welcome")

    def changeAppearance(self):
        state = self.switchDarkMode.get()
        if state == 1:
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")

class ParentScreen(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 10, "bold")
        self.font3 = ("Inter", 12, "bold")

        # Frames
        self.frameSidebar = CTkFrame(
            self,
            width=200,
            height=self.winfo_width() / scale_factor,
            corner_radius=0
        )
        self.frameMain = CTkFrame(
            self,
            width=480,
            height=self.winfo_width() / scale_factor,
            corner_radius=10
        )
        self.frameStatus = CTkFrame(
            self.frameMain,
            width=75,
            height=25,
            fg_color=Student.rollColours[0],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.spacer = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )


        # Sidebar widgets
        self.lblTitle = CTkLabel(
            self.frameSidebar,
            text="Student Attendance System",
            text_font=self.font3,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )
        self.switchDarkMode = CTkSwitch(
            self.frameSidebar,
            text="Dark Mode",
            text_font=self.font1,
            command=self.changeAppearance
        )

        # Main area widgets
        self.lblUserInfo = CTkLabel(
            self.frameMain,
            text="User (Username)",
            text_font=self.font2,
            text_color=("#0969DA", "#58A6FF"),
            justify="left",
            anchor="w"
        )
        self.lblUserInfo.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblDetails = CTkLabel(
            self.frameMain,
            text="Your Details",
            text_font=self.font3,
            justify="left",
            anchor="w"
        )
        self.lblDetails.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblUsername = CTkLabel(
            self.frameMain,
            width=215,
            text="Username: Username",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblUsername.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblFirstName = CTkLabel(
            self.frameMain,
            width=215,
            text="First Name: First Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblFirstName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblLastName = CTkLabel(
            self.frameMain,
            width=215,
            text="Last Name: Last Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblLastName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblEmail = CTkLabel(
            self.frameMain,
            width=215,
            text="Email: Email",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblEmail.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.btnChangePassword = CTkButton(
            self.frameMain,
            height=28,
            text="Change Password",
            text_font=self.font1,
            command=lambda: ChangePassword(self)
        )
        self.btnCreateNote = CTkButton(
            self.frameMain,
            width=110,
            height=28,
            text="Create Note",
            text_font=self.font1,
            command=lambda: CreateNote(user.child, master=self)
        )
        self.btnLogout = CTkButton(
            self.frameMain,
            width=60,
            text="Logout",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.logout
        )
        self.lblAttendance = CTkLabel(
            self.frameMain,
            width=200,
            text="Child's Attendance",
            text_font=self.font3
        )
        self.lblStatus = CTkLabel(
            self.frameMain,
            text="Today's Status:",
            text_font=self.font1,
            corner_radius=0
        )
        self.frameStatus = CTkFrame(
            self.frameMain,
            width=75,
            height=25,
            fg_color=Student.rollColours[0],
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8
        )
        self.btnAttendance = CTkButton(
            self.frameMain,
            width=110,
            height=28,
            text="View Attendance",
            text_font=self.font1,
            command=lambda: ViewAttendance(user.child, master=self)
        )
        self.frameNote = CTkFrame(
            self.frameMain,
            width=200,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )
        self.lblNotes = CTkLabel(
            self.frameNote,
            width=180,
            text="Attendance Notes",
            text_font=self.font3
        )
        self.note = Note(
            self.frameNote,
            width=180,
            height=180,
            title="No Notes",
            content="There are no notes to display.",
            fg_color=("#C0C2C5", "#343638"),
            corner_radius=10
        )
        self.btnBack = CTkButton(
            self.frameNote,
            width=80,
            text="Previous",
            text_font=self.font1,
            command=lambda: self.scroll(-1)
        )
        self.btnNext = CTkButton(
            self.frameNote,
            width=80,
            text="Next",
            text_font=self.font1,
            command=lambda: self.scroll(1)
        )

        # Widget placement
        self.frameSidebar.grid(row=0, column=0, sticky="nsew")
        self.lblTitle.grid(row=0, column=0, pady=20)
        self.switchDarkMode.grid(row=2, column=0, pady=30)
        self.frameMain.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.lblUserInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.lblDetails.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        self.lblUsername.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
        self.lblFirstName.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")
        self.lblLastName.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")
        self.lblEmail.grid(row=5, column=0, columnspan=2,padx=10, sticky="w")
        self.btnChangePassword.grid(row=6, column=0, columnspan=2, padx=16, pady=10, sticky="w")
        self.btnCreateNote.grid(row=7, column=0, columnspan=2, padx=16, pady=10, sticky="w")
        self.spacer.grid(row=8, column=0, columnspan=2, sticky="ns")
        self.btnLogout.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.lblAttendance.grid(row=1, column=2, columnspan=2)
        self.lblStatus.grid(row=2, column=2, sticky="e")
        self.frameStatus.grid(row=2, column=3, stick="w")
        self.btnAttendance.grid(row=3, rowspan=2, column=2, columnspan=2, pady=10)
        self.frameNote.grid(row=5, rowspan=5, column=2, columnspan=2, sticky="n")
        self.lblNotes.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 10))
        self.note.grid(row=1, column=0, columnspan=2)
        self.btnBack.grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.btnNext.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        # Grid configuration
        self.columnconfigure(0, weight=5, uniform="columns")
        self.columnconfigure(1, weight=13, uniform="columns")
        self.rowconfigure(0, weight=1, uniform="rows")
        self.frameSidebar.columnconfigure(0, weight=1, uniform="columns1")
        self.frameSidebar.rowconfigure(1, weight=1, uniform="spacing")
        self.frameMain.columnconfigure((0, 1, 2, 3), weight=1, uniform="columns2")
        self.frameMain.rowconfigure(8, weight=1, uniform="spacing1")

    def setBinds(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.logout())
        master.bind("<Escape>", lambda x: self.logout())
        if get_appearance_mode() == "Dark":
            self.switchDarkMode.select()

    def setup(self):
        self.lblUserInfo.configure(text=f"{user.first} {user.last} ({user.username})")
        self.lblUsername.configure(text=f"Username: {user.username}")
        self.lblFirstName.configure(text=f"First Name: {user.first}")
        self.lblLastName.configure(text=f"Last Name: {user.last}")
        self.lblEmail.configure(text=f"Email: {user.email}")
        self.frameStatus.configure(fg_color=Student.rollColours[user.child.today])
        self.createNotes()

        # CTkLabel width fix
        self.lblUsername.canvas.configure(width=int(215 * scale_factor))
        self.lblFirstName.canvas.configure(width=int(215 * scale_factor))
        self.lblLastName.canvas.configure(width=int(215 * scale_factor))
        self.lblEmail.canvas.configure(width=int(215 * scale_factor))
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.lblUsername.text_label.configure(width=27)
        self.lblFirstName.text_label.configure(width=27)
        self.lblLastName.text_label.configure(width=27)
        self.lblEmail.text_label.configure(width=27)
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def createNotes(self, *, update=False):
        self.notes = user.child.notes
        self.keys = list(self.notes.keys())
        if not update:
            self.index = 0

        if self.notes:
            self.note.setTitle(self.keys[self.index])
            self.note.setContent(self.notes[self.keys[self.index]])

        # Disabling
        if len(self.keys) < 2:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="disabled")
        elif self.index == 0:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="normal")
        elif self.index == len(self.keys) - 1:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="disabled")
        else:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="normal")

        # CTkLabel width fix
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def scroll(self, offset):
        self.index += offset

        # Updating GUI
        self.note.setTitle(self.keys[self.index])
        self.note.setContent(self.notes[self.keys[self.index]])

        # Disabling
        if self.index == 0:
            self.btnBack.configure(state="disabled")
            self.btnNext.configure(state="normal")
        elif self.index == len(self.keys) - 1:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="disabled")
        else:
            self.btnBack.configure(state="normal")
            self.btnNext.configure(state="normal")

        # CTkLabel width fix
        self.note.lblTitle.canvas.configure(width=int(170 * scale_factor))
        self.note.lblContent.canvas.configure(width=int(170 * scale_factor))
        self.note.lblTitle.text_label.configure(width=23)
        self.note.lblContent.text_label.configure(width=23)

    def logout(self):
        question = "Are you sure you would like to logout?"
        confirm = Messagebox.askyesno("Exit", question, master=self.master)
        if confirm:
            self.master.display(self.master.frameLogin, title="Welcome")

    def changeAppearance(self):
        state = self.switchDarkMode.get()
        if state == 1:
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")

class TeacherScreen(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 10, "bold")
        self.font3 = ("Inter", 12, "bold")
        self.font4 = ("Consolas", 12)

        # Frames
        self.frameSidebar = CTkFrame(
            self,
            width=200,
            height=self.winfo_width() / scale_factor,
            corner_radius=0
        )
        self.frameMain = CTkFrame(
            self,
            width=480,
            height=self.winfo_width() / scale_factor,
            corner_radius=10
        )
        self.spacer = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )


        # Sidebar widgets
        self.lblTitle = CTkLabel(
            self.frameSidebar,
            text="Student Attendance System",
            text_font=self.font3,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )
        self.switchDarkMode = CTkSwitch(
            self.frameSidebar,
            text="Dark Mode",
            text_font=self.font1,
            command=self.changeAppearance
        )

        # Main area widgets
        self.lblUserInfo = CTkLabel(
            self.frameMain,
            text="User (Username)",
            text_font=self.font2,
            text_color=("#0969DA", "#58A6FF"),
            justify="left",
            anchor="w"
        )
        self.lblUserInfo.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblDetails = CTkLabel(
            self.frameMain,
            text="Your Details",
            text_font=self.font3,
            justify="left",
            anchor="w"
        )
        self.lblDetails.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblUsername = CTkLabel(
            self.frameMain,
            width=215,
            text="Username: Username",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblUsername.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblFirstName = CTkLabel(
            self.frameMain,
            width=215,
            text="First Name: First Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblFirstName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblLastName = CTkLabel(
            self.frameMain,
            width=215,
            text="Last Name: Last Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblLastName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblEmail = CTkLabel(
            self.frameMain,
            width=215,
            text="Email: Email",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblEmail.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.btnChangePassword = CTkButton(
            self.frameMain,
            height=28,
            text="Change Password",
            text_font=self.font1,
            command=lambda: ChangePassword(self)
        )
        self.btnLogout = CTkButton(
            self.frameMain,
            width=60,
            text="Logout",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.logout
        )
        self.frameGroup = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )
        self.lblStudentSearch = CTkLabel(
            self.frameGroup,
            width=200,
            text="Student Management",
            text_font=self.font3
        )
        self.entStudentSearch = CTkEntry(
            self.frameGroup,
            width=180,
            height=28,
            placeholder_text="Student Username",
            text_font=self.font4,
        )
        self.btnStudentSearch = CTkButton(
            self.frameGroup,
            width=80,
            height=28,
            text="Search",
            text_font=self.font1,
            command=self.studentSearch
        )

        # Widget placement
        self.frameSidebar.grid(row=0, column=0, sticky="nsew")
        self.lblTitle.grid(row=0, column=0, pady=20)
        self.switchDarkMode.grid(row=2, column=0, pady=30)
        self.frameMain.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.lblUserInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.lblDetails.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        self.lblUsername.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
        self.lblFirstName.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")
        self.lblLastName.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")
        self.lblEmail.grid(row=5, column=0, columnspan=2,padx=10, sticky="w")
        self.btnChangePassword.grid(row=6, column=0, columnspan=2, padx=16, pady=10, sticky="w")
        self.spacer.grid(row=7, column=0, columnspan=2, sticky="ns")
        self.btnLogout.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.frameGroup.grid(row=1, rowspan=7, column=2, columnspan=2, sticky="n")
        self.lblStudentSearch.grid(row=0, column=0)
        self.entStudentSearch.grid(row=1, column=0, pady=5)
        self.btnStudentSearch.grid(row=2, column=0, pady=10)

        # Grid configuration
        self.columnconfigure(0, weight=5, uniform="columns")
        self.columnconfigure(1, weight=13, uniform="columns")
        self.rowconfigure(0, weight=1, uniform="rows")
        self.frameSidebar.columnconfigure(0, weight=1, uniform="columns1")
        self.frameSidebar.rowconfigure(1, weight=1, uniform="spacing")
        self.frameMain.columnconfigure((0, 1, 2, 3), weight=1, uniform="columns2")
        self.frameMain.rowconfigure(7, weight=1, uniform="spacing1")
        self.frameGroup.columnconfigure(0, weight=1, uniform="columns3")

        # System binds
        self.entStudentSearch.bind("<FocusIn>", lambda x: self.accent(self.entStudentSearch, 1), add=True)
        self.entStudentSearch.bind("<FocusOut>", lambda x: self.accent(self.entStudentSearch, 0), add=True)

    def setBinds(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.logout())
        master.bind("<Escape>", lambda x: self.logout())
        if get_appearance_mode() == "Dark":
            self.switchDarkMode.select()

    def setup(self):
        self.lblUserInfo.configure(text=f"{user.first} {user.last} ({user.username})")
        self.lblUsername.configure(text=f"Username: {user.username}")
        self.lblFirstName.configure(text=f"First Name: {user.first}")
        self.lblLastName.configure(text=f"Last Name: {user.last}")
        self.lblEmail.configure(text=f"Email: {user.email}")

        # CTkLabel width fix
        self.lblUsername.canvas.configure(width=int(215 * scale_factor))
        self.lblFirstName.canvas.configure(width=int(215 * scale_factor))
        self.lblLastName.canvas.configure(width=int(215 * scale_factor))
        self.lblEmail.canvas.configure(width=int(215 * scale_factor))
        self.lblUsername.text_label.configure(width=27)
        self.lblFirstName.text_label.configure(width=27)
        self.lblLastName.text_label.configure(width=27)
        self.lblEmail.text_label.configure(width=27)

    def studentSearch(self):
        search = self.entStudentSearch.get().lower()

        if not search:
            Messagebox.showwarning("Search Blank", "Please enter a search parameter.")
            return None

        temp = {}
        with open(DATA_FILE) as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                if int(row[5]) == 0:
                    temp[row[0]] = row[1:]

        keys = list(temp.keys())
        keys = Sort.selectionSort(keys)
        students = {key: temp[key] for key in keys}
        result = Search.binarySearch([key.lower() for key in students], search)

        if result >= 0:
            searchUser = Student(keys[result], *students[keys[result]])
            EditAttendance(searchUser, master=self)
        else:
            Messagebox.showerror("Search Unsuccesful", "Student not found.")

    def logout(self):
        question = "Are you sure you would like to logout?"
        confirm = Messagebox.askyesno("Exit", question, master=self.master)
        if confirm:
            self.master.display(self.master.frameLogin, title="Welcome")

    def changeAppearance(self):
        state = self.switchDarkMode.get()
        if state == 1:
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")

    @staticmethod
    def accent(widget, state):
        colours = {
            1: ("#0969DA", "#58A6FF"),
            0: ("#979DA2", "#565B5E")
        }
        widget.configure(border_color=colours[state])


class AdminScreen(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fonts
        self.font1 = ("Inter", 10)
        self.font2 = ("Inter", 10, "bold")
        self.font3 = ("Inter", 12, "bold")
        self.font4 = ("Consolas", 12)

        # Frames
        self.frameSidebar = CTkFrame(
            self,
            width=200,
            height=self.winfo_width() / scale_factor,
            corner_radius=0
        )
        self.frameMain = CTkFrame(
            self,
            width=480,
            height=self.winfo_width() / scale_factor,
            corner_radius=10
        )
        self.spacer = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )


        # Sidebar widgets
        self.lblTitle = CTkLabel(
            self.frameSidebar,
            text="Student Attendance System",
            text_font=self.font3,
            wraplength=int(180 * scale_factor),
            corner_radius=0
        )
        self.switchDarkMode = CTkSwitch(
            self.frameSidebar,
            text="Dark Mode",
            text_font=self.font1,
            command=self.changeAppearance
        )

        # Main area widgets
        self.lblUserInfo = CTkLabel(
            self.frameMain,
            text="User (Username)",
            text_font=self.font2,
            text_color=("#0969DA", "#58A6FF"),
            justify="left",
            anchor="w"
        )
        self.lblUserInfo.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblDetails = CTkLabel(
            self.frameMain,
            text="Your Details",
            text_font=self.font3,
            justify="left",
            anchor="w"
        )
        self.lblDetails.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblUsername = CTkLabel(
            self.frameMain,
            width=215,
            text="Username: Username",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblUsername.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblFirstName = CTkLabel(
            self.frameMain,
            width=215,
            text="First Name: First Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblFirstName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblLastName = CTkLabel(
            self.frameMain,
            width=215,
            text="Last Name: Last Name",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblLastName.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.lblEmail = CTkLabel(
            self.frameMain,
            width=215,
            text="Email: Email",
            text_font=self.font1,
            wraplength=int(210 * scale_factor),
            justify="left",
            anchor="w"
        )
        self.lblEmail.text_label.grid_configure(sticky="w") # <- CTkLabel anchor fix
        self.btnChangePassword = CTkButton(
            self.frameMain,
            height=28,
            text="Change Password",
            text_font=self.font1,
            command=lambda: ChangePassword(self)
        )
        self.btnLogout = CTkButton(
            self.frameMain,
            width=60,
            text="Logout",
            text_font=self.font1,
            text_color="#DCE4EE",
            fg_color="#c92d39",
            command=self.logout
        )
        self.frameGroup = CTkFrame(
            self.frameMain,
            fg_color=("#D1D5D8", "#2A2D2E"),
            corner_radius=0
        )
        self.lblStudentSearch = CTkLabel(
            self.frameGroup,
            width=200,
            text="Student Management",
            text_font=self.font3
        )
        self.entStudentSearch = CTkEntry(
            self.frameGroup,
            width=180,
            height=28,
            placeholder_text="Student Username",
            text_font=self.font4,
        )
        self.btnStudentSearch = CTkButton(
            self.frameGroup,
            width=80,
            height=28,
            text="Search",
            text_font=self.font1,
            command=self.studentSearch
        )

        # Widget placement
        self.frameSidebar.grid(row=0, column=0, sticky="nsew")
        self.lblTitle.grid(row=0, column=0, pady=20)
        self.switchDarkMode.grid(row=2, column=0, pady=30)
        self.frameMain.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.lblUserInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.lblDetails.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        self.lblUsername.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
        self.lblFirstName.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")
        self.lblLastName.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")
        self.lblEmail.grid(row=5, column=0, columnspan=2,padx=10, sticky="w")
        self.btnChangePassword.grid(row=6, column=0, columnspan=2, padx=16, pady=10, sticky="w")
        self.spacer.grid(row=7, column=0, columnspan=2, sticky="ns")
        self.btnLogout.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.frameGroup.grid(row=1, rowspan=7, column=2, columnspan=2, sticky="n")
        self.lblStudentSearch.grid(row=0, column=0)
        self.entStudentSearch.grid(row=1, column=0, pady=5)
        self.btnStudentSearch.grid(row=2, column=0, pady=10)

        # Grid configuration
        self.columnconfigure(0, weight=5, uniform="columns")
        self.columnconfigure(1, weight=13, uniform="columns")
        self.rowconfigure(0, weight=1, uniform="rows")
        self.frameSidebar.columnconfigure(0, weight=1, uniform="columns1")
        self.frameSidebar.rowconfigure(1, weight=1, uniform="spacing")
        self.frameMain.columnconfigure((0, 1, 2, 3), weight=1, uniform="columns2")
        self.frameMain.rowconfigure(7, weight=1, uniform="spacing1")
        self.frameGroup.columnconfigure(0, weight=1, uniform="columns3")

        # System binds
        self.entStudentSearch.bind("<FocusIn>", lambda x: self.accent(self.entStudentSearch, 1), add=True)
        self.entStudentSearch.bind("<FocusOut>", lambda x: self.accent(self.entStudentSearch, 0), add=True)

    def setBinds(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.logout())
        master.bind("<Escape>", lambda x: self.logout())
        if get_appearance_mode() == "Dark":
            self.switchDarkMode.select()

    def setup(self):
        self.lblUserInfo.configure(text=f"{user.first} {user.last} ({user.username})")
        self.lblUsername.configure(text=f"Username: {user.username}")
        self.lblFirstName.configure(text=f"First Name: {user.first}")
        self.lblLastName.configure(text=f"Last Name: {user.last}")
        self.lblEmail.configure(text=f"Email: {user.email}")

        # CTkLabel width fix
        self.lblUsername.canvas.configure(width=int(215 * scale_factor))
        self.lblFirstName.canvas.configure(width=int(215 * scale_factor))
        self.lblLastName.canvas.configure(width=int(215 * scale_factor))
        self.lblEmail.canvas.configure(width=int(215 * scale_factor))
        self.lblUsername.text_label.configure(width=27)
        self.lblFirstName.text_label.configure(width=27)
        self.lblLastName.text_label.configure(width=27)
        self.lblEmail.text_label.configure(width=27)

    def studentSearch(self):
        search = self.entStudentSearch.get().lower()

        if not search:
            Messagebox.showwarning("Search Blank", "Please enter a search parameter.")
            return None

        temp = {}
        with open(DATA_FILE) as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                if int(row[5]) == 0:
                    temp[row[0]] = row[1:]

        keys = list(temp.keys())
        keys = Sort.quickSort(keys, 0, len(keys) - 1)
        students = {key: temp[key] for key in keys}
        result = Search.binarySearch([key.lower() for key in students], search)

        if result >= 0:
            searchUser = Student(keys[result], *students[keys[result]])
            EditAttendance(searchUser, master=self)
        else:
            Messagebox.showerror("Search Unsuccesful", "Student not found.")

    def logout(self):
        question = "Are you sure you would like to logout?"
        confirm = Messagebox.askyesno("Exit", question, master=self.master)
        if confirm:
            self.master.display(self.master.frameLogin, title="Welcome")

    def changeAppearance(self):
        state = self.switchDarkMode.get()
        if state == 1:
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")

    @staticmethod
    def accent(widget, state):
        colours = {
            1: ("#0969DA", "#58A6FF"),
            0: ("#979DA2", "#565B5E")
        }
        widget.configure(border_color=colours[state])


# Main window
class Main(CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.width = 720
        self.height = 540
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)

        # Panels (Frame windows)
        self.frameLogin = LoginScreen(
            self,
            width=self.width,
            height=self.height,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )
        self.frameStudent = StudentScreen(
            self,
            width=self.width,
            height=480,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )
        self.frameParent = ParentScreen(
            self,
            width=self.width,
            height=480,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )
        self.frameTeacher = TeacherScreen(
            self,
            width=self.width,
            height=480,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )
        self.frameAdmin = AdminScreen(
            self,
            width=self.width,
            height=480,
            fg_color=("#EBEBEC", "#212325"),
            corner_radius=0
        )

        # Widget placement
        self.frameLogin.grid(column=0, row=0, sticky="nsew")
        self.frameStudent.grid(column=0, row=0, sticky="nsew")
        self.frameParent.grid(column=0, row=0, sticky="nsew")
        self.frameTeacher.grid(column=0, row=0, sticky="nsew")
        self.frameAdmin.grid(column=0, row=0, sticky="nsew")

        # Grid configuration
        self.columnconfigure(0, weight=1, uniform="columns")
        self.rowconfigure(0, weight=1, uniform="rows")

        # System binds
        self.display(self.frameLogin, title="Welcome")

    def display(self, frame, *, title=None):
        # Disabling all widgets
        widgets = []
        self.listChildren(self, widgets)
        for widget in widgets:
            try:
                widget.configure(state="disabled")
            except TclError:
                pass

        # Enabling all widgets in frame
        frameWidgets = []
        self.listChildren(frame, frameWidgets)
        for widget in frameWidgets:
            try:
                widget.configure(state="normal")
            except TclError:
                pass

        # Raising frame and configuring
        self.width = int(frame.cget("width") / scale_factor)
        self.height = int(frame.cget("height") / scale_factor)
        self.x = int(((self.winfo_screenwidth() / scale_factor) - self.width) / 2)
        self.y = int(((self.winfo_screenheight() / scale_factor) - self.height) / 2 - 30)
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.title(title)
        self.removeBinds()
        frame.setBinds(self)
        frame.tkraise()

    def listChildren(self, widget, array):
        array.append(widget)

        # Recursively finding every child widget
        for child in widget.winfo_children():
            self.listChildren(child, array)

        return array

    def removeBinds(self):
        for event in self.bind():
            self.unbind(event)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

if __name__ == "__main__":
    app = Main()
    app.mainloop()
