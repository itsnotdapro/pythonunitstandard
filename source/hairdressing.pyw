# Hairdressing Application logic and window function
# main.py
# 4/05/18

from windows import ApplicationWindow, ClientList, DeleteClient, Invoice
import json
from datetime import datetime
from tkinter import Tk, messagebox

# set costs of services, can be changed by editing these values
cost = { "drive": 0.25,
         "hair": 1.50,
         "mani": 0.75}

# get time in minutes ONLY
def time_to_minutes(hour, minute, second):
    if hour == "": hour = 0
    if minute == "": minute = 0
    if second == "": second = 0
    return round(int(hour)*60 + int(minute) + int(second)/60)

## Child class of ApplicationWindow, with all functionality added ## 
class HairdressingApp(ApplicationWindow):
    def __init__(self, master):
        super().__init__(master)
        now = datetime.now()
        self.add_client.config(command=self.add_client_func) # set function of the set client button
        with open('data.json') as file:
            data = json.load(file) # get data from json file
            self.set_totals(data, "{}/{}/{}".format(now.day, now.month, now.year)) # set the totals text on lauch
        
    # get all totals from inputs
    def get_totals(self):
        rv = {"drive": 0, "hair": 0, "mani": 0} #rv = return value
        with open("data.json") as file:
            data = json.load(file) #get data from json file
            now = datetime.now()
            current_date = "{}/{}/{}".format(now.day, now.month, now.year)
            for client in data[current_date]: # for each value under the current date, add to corresponding index in rv
                rv["drive"] += data[current_date][client]["drive"]
                rv["hair"] += data[current_date][client]["hair"]
                rv["mani"] += data[current_date][client]["mani"]
        return rv

    # set the totals text
    def set_totals(self, data, date):
        try: type(data[date]) # see if any data is under the current date
        except KeyError: return

        # set ALL THE TEXT
        self.total_drive_time.config(text=str(self.get_totals()["drive"]) + " Minutes")
        self.total_hair_time.config(text=str(self.get_totals()["hair"]) + " Minutes")
        self.total_mani_time.config(text=str(self.get_totals()["mani"]) + " Minutes")

        self.total_drive_price.config(text="$" + str(float(self.get_totals()["drive"])*cost["drive"]))
        self.total_hair_price.config(text="$" + str(float(self.get_totals()["hair"])*cost["hair"]))
        self.total_mani_price.config(text="$" + str(float(self.get_totals()["mani"])*cost["mani"]))

        self.total_price.config(text="$" + str(float(self.get_totals()["drive"])*cost["drive"] + \
                                               float(self.get_totals()["hair"])*cost["hair"] + \
                                               float(self.get_totals()["mani"])*cost["mani"]))

    # add client to database, and generate invoice
    def add_client_func(self):
        if self.name_input.get() in ["", "Namе"] or self.address_input.get() in ["", "Addrеss"]:
            messagebox.showerror("Error", "No Name and/or Address given")
            return
        
        with open('data.json') as file:
            now = datetime.now()
            new_data = {}
            data = json.load(file) # get data from json file

            current_date = "{}/{}/{}".format(now.day, now.month, now.year)
            try: type(data[current_date]) # check if any data exists under current date
            except KeyError: data[current_date] = {} # if not, create a dict under current date
            data[current_date][self.name_input.get()] = {}
            data[current_date][self.name_input.get()]["address"] = self.address_input.get()
            data[current_date][self.name_input.get()]["drive"] = time_to_minutes(self.drive_hours.get(), self.drive_mins.get(), 0)
            data[current_date][self.name_input.get()]["hair"] = time_to_minutes(self.hair_hours.get(), self.hair_mins.get(), 0)
            data[current_date][self.name_input.get()]["mani"] = time_to_minutes(self.mani_hours.get(), self.mani_mins.get(), 0)

        with open('data.json', 'w') as file: json.dump(data, file) # write to file

        with open("data.json") as file: # set the totals, has to be done here as the data needs to be in the json file to be read
            data = json.load(file)
            self.set_totals(data, current_date)

        # generate invoice
        invoice = Invoice(self, self.name_input.get(),
                                self.address_input.get(),
                                time_to_minutes(self.drive_hours.get(), self.drive_mins.get(), 0),
                                time_to_minutes(self.hair_hours.get(), self.hair_mins.get(), 0),
                                time_to_minutes(self.mani_hours.get(), self.mani_mins.get(), 0), cost)
        invoice.title(self.name_input.get() + " Invoice")
        invoice.geometry("325x150")

        # delete text in inputs
        self.name_input.delete(0, "end")
        self.address_input.delete(0, "end")
        self.address_placeholder(None)
        self.name_placeholder(None)
        self.drive_hours.delete(0, "end")
        self.drive_mins.delete(0, "end")
        self.hair_hours.delete(0, "end")
        self.hair_mins.delete(0, "end")
        self.mani_hours.delete(0, "end")
        self.mani_mins.delete(0, "end")
        
        invoice.mainloop()

if __name__ == "__main__":        
    root = Tk()
    root.geometry("400x400")
    root.title("Hairdressing Application")

    app = HairdressingApp(root)
    root.mainloop()
