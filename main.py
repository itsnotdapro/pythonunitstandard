from windows import ApplicationWindow, ClientList, DeleteClient, Invoice
import json
from datetime import datetime
from tkinter import Tk

cost = { "drive": 0.25,
         "hair": 1.50,
         "mani": 0.75}

def time_to_minutes(hour, minute, second):
    if hour == "": hour = 0
    if minute == "": minute = 0
    if second == "": second = 0
    return round(int(hour)*60 + int(minute) + int(second)/60)

class HairdressingApp(ApplicationWindow):
    def __init__(self, master):
        super().__init__(master)
        self.add_client.config(command=self.add_client_func)

    def get_totals(self):
        rv = {"drive": 0, "hair": 0, "mani": 0}
        with open("data.json") as file:
            data = json.load(file)
            now = datetime.now()
            current_date = "{}/{}/{}".format(now.day, now.month, now.year)
            for client in data[current_date]:
                rv["drive"] += data[current_date][client]["drive"]
                rv["hair"] += data[current_date][client]["hair"]
                rv["mani"] += data[current_date][client]["mani"]
        return rv

    def set_totals(self, data, date):
        try: type(data[date])
        except KeyError: return
        self.total_drive_time.config(text=str(self.get_totals()["drive"]) + " Minutes")
        self.total_hair_time.config(text=str(self.get_to tals()["hair"]) + " Minutes")
        self.total_mani_time.config(text=str(self.get_totals()["mani"]) + " Minutes")

        self.total_drive_price.config(text="$" + str(float(self.get_totals()["drive"])*cost["drive"]))
        self.total_hair_price.config(text="$" + str(float(self.get_totals()["hair"])*cost["hair"]))
        self.total_mani_price.config(text="$" + str(float(self.get_totals()["mani"])*cost["mani"]))

        self.total_price.config(text="$" + str(float(self.get_totals()["drive"])*cost["drive"] + \
                                               float(self.get_totals()["hair"])*cost["hair"] + \
                                               float(self.get_totals()["mani"])*cost["mani"]))
        
    def add_client_func(self):
        with open('data.json') as file:
            now = datetime.now()
            new_data = {}
            data = json.load(file)

            current_date = "{}/{}/{}".format(now.day, now.month, now.year)
            try: type(data[current_date])
            except KeyError: data[current_date] = {}
            data[current_date][self.name_input.get()] = {}
            data[current_date][self.name_input.get()]["address"] = self.address_input.get()
            data[current_date][self.name_input.get()]["drive"] = time_to_minutes(self.drive_hours.get(), self.drive_mins.get(), 0)
            data[current_date][self.name_input.get()]["hair"] = time_to_minutes(self.hair_hours.get(), self.hair_mins.get(), 0)
            data[current_date][self.name_input.get()]["mani"] = time_to_minutes(self.mani_hours.get(), self.mani_mins.get(), 0)

        with open('data.json', 'w') as file: json.dump(data, file)

        with open("data.json") as file:
            data = json.load(file)
            self.set_totals(data, current_date)

        invoice = Invoice(self, "name", "address", "drive", "hair", "mani", "price")
        invoice.geometry("300x140")
        invoice.mainloop()

        





root = Tk()
root.geometry("400x600")

app = HairdressingApp(root)
root.mainloop()
