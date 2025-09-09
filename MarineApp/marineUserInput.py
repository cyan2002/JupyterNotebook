#Import packages
import tkinter as ttk
from tkcalendar import DateEntry
from tkinter import messagebox
#import openpyxl
import pandas as pd
from datetime import datetime

#creates an instance of the Tk class, which initializes Tk and creates its associated Tcl interpreter. 
#It also creates a toplevel window, known as the root window, which serves as the main window of the application.
root = ttk.Tk()
root.title("Marine User Input App")
root.geometry("1000x800")

#List of Species
entries = []
entries_value = []
v = ttk.IntVar()
hold = int()
labels = ["Cunner", "Black Sea Bass", "Striper", 
          "Atlantic Rock Crab", "Jonah Crab", "Green Crab", "Asian Shore Crab"]

# function to validate mark entry for ONLY integers
def only_numbers(char):
    return char.isdigit()
validation_number = root.register(only_numbers)

def only_time(char):
    return (char.isdigit()) or (char == ":")
validation_time = root.register(only_time)

def valid_date():
    #checking if valid time is entered - checks for correct form HH:MM or H:MM
    if((len(time_entry.get()) != 4 and (len(time_entry.get())) != 5)):
        #return error message!
        #messagebox.showerror("Error", "Invalid Time Format!")
        return True
    #checking if there is a semi-colon
    elif(time_entry.get()[1] != ":" and time_entry.get()[2] != ":"):
        #return error message!
        #messagebox.showerror("Error", "Forgot the semi-colon!")
        return True
    #checking that hour is valid (12 or less, we are american!)
    elif(int(time_entry.get()[0:int(time_entry.get()[time_entry.get().index(":")-1])]) > 12):
        #messagebox.showerror("Error", "We are American!")
        return True
    #checking that minutes are less than 60
    elif(int(time_entry.get()[(time_entry.get().index(":")+1):(len(time_entry.get()))]) > 60):
        #messagebox.showerror("Error", "Check your minutes!")
        return True
    else:
        return False

#getting input and writing to csv to save file.
def get_input():
    if(valid_date()):
        messagebox.showerror("Error", "Check your time format!")
    else:
        #all good!
        entries_value.clear()
        for i in range(len(entries)):
            current_value = entries[i].get()
            if not current_value:
                entries_value.insert(i, 0)
            else:
                entries_value.append(int(entries[i].get()))
        write_to_csv()

def write_to_csv():
    #date_format = "%m/%d/%y"
    #date_string = datetime.strptime(date_entry.get(), date_format).date()
    filename = date_entry.get().replace("/", "-")
    filename = filename + "_species_count.xlsx"

    MornOrNight = str()
    if(date_entry.get() == 2):
        MornOrNight = "AM"
    else:
        MornOrNight = "PM"

    data_meta = [["Date:", "AM or PM", "Time"],[date_entry.get(), MornOrNight, time_entry.get()]]
    df_meta = pd.DataFrame(data_meta)

    # Create a simple DataFrame (replace with your data)
    data_data = {'Species': labels,
        'Count': entries_value}
    df_data = pd.DataFrame(data_data)

    with pd.ExcelWriter(filename) as writer:  
        df_meta.to_excel(writer, sheet_name='Meta', index=False) 
        df_data.to_excel(writer, sheet_name='Counts', index=False)

    messagebox.showinfo("Submission Status", "Form submitted successfully!")

#Date entry - problem: modern macs have a glitch when running this
date_label = ttk.Label(root, text="Date")
date_label.grid(column=0, row=0)
date_entry = DateEntry(root)
date_entry.grid(column = 1, row = 0)
date_warning = ttk.Label(root, text="Note: Keep date in same format")
date_warning.grid(column = 2, row = 0)

#Time Entry - time
time_label = ttk.Label(root, text="Time")
time_label.grid(column=0, row=1)
time_entry = ttk.Entry(root, validate="key", validatecommand=(validation_time, '%S'))
time_entry.grid(column=1, row=1)

#Time Entry - AM or PM choice
ttk.Label(root, text="Choose AM or PM").grid(column=0, row=2, columnspan=2)
AMorPM = ttk.Radiobutton(root, 
               text="AM",
               value=1,
               var=v).grid(column=0, row=3, padx=0)
AMorPM = ttk.Radiobutton(root, 
               text="PM",
               value=2,
               var=v).grid(column=1, row=3, padx=0)

#Site Entry 
site_label = ttk.Label(root, text="Site")
site_label.grid(column=0, row=5)
site_entry = ttk.Entry(root)
site_entry.grid(column=1, row=5)

for i in range(7): # creating label widgets FOR species label
    entry_label = ttk.Label(root, text=labels[i])
    entry_label.grid(column=0, row=i+6)

for i in range(7): # creating entry widgets FOR species count
    entry = ttk.Entry(root, validate="key", validatecommand=(validation_number, '%S'))
    entry.grid(column=1, row=i+6)
    entries.append(entry)

# Button that will call the submit function 
ttk.Button(root,text = 'Submit', command = get_input).grid(column = 0, row = 13)

#A button widget is then created, and placed to the right of the label. When pressed, it will call the destroy() method of the root window.
ttk.Button(root, text="Quit", command=root.destroy).grid(column=0, row=14)

#Finally, the mainloop() method puts everything on the display, and responds to user input until the program terminates.
root.mainloop()

#things to do
#main screen
#add images