import tkinter as tk
import json
from functools import partial
from datetime import datetime

class ApplicationWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Start creating all the fucking widgets. This is why tkinter is the fucking worst #
        menubar = tk.Menu()
        filebar = tk.Menu(menubar, tearoff=0)
        filebar.add_command(label="Show Today's Clients", command=self.open_client_list)
        filebar.add_command(label="Delete a Client", command=self.open_delete_clients)

        helpbar = tk.Menu(menubar, tearoff=0)
        helpbar.add_command(label="How to Use")

        menubar.add_cascade(label="File", menu=filebar)
        menubar.add_cascade(label="Help", menu=helpbar)
        master.config(menu=menubar)

        tk.Label(text="Title", font=("Verdana", 20, "bold")).pack()

        self.name_input = tk.Entry()
        self.name_input.pack()

        self.address_input = tk.Entry()
        self.address_input.pack()

        self.input_grid = tk.Frame()
        self.input_grid.pack()

        tk.Label(self.input_grid, text="Driving").grid(row=0, column=0, columnspan=2)
        tk.Label(self.input_grid, text="Haircutting").grid(row=0, column=2, columnspan=2)
        tk.Label(self.input_grid, text="Mani").grid(row=0, column=4, columnspan=2)

        self.drive_hours = self.create_time_inputs("Hours: ", 0, 1)
        self.drive_mins = self.create_time_inputs("Minutes: ", 0, 2)

        self.hair_hours = self.create_time_inputs("Hours: ", 2, 1)
        self.hair_mins = self.create_time_inputs("Minutes: ", 2, 2)

        self.mani_hours = self.create_time_inputs("Hours: ", 4, 1)
        self.mani_mins = self.create_time_inputs("Minutes: ", 4, 2)

        self.add_client = tk.Button(text="Add Client and Generate Invoice", font=("Verdana", 12))
        self.add_client.pack(pady=20)

        tk.Label(text="Today's Totals", font=("Verdana", 16, "bold")).pack()
        total_grid = tk.Frame()
        total_grid.pack()

        tk.Label(total_grid, text="Driving", font=("Verdana", 11, "bold")).grid(row=0, column=0)
        tk.Label(total_grid, text="Haircutting", font=("Verdana", 11, "bold")).grid(row=0, column=1)
        tk.Label(total_grid, text="Mani", font=("Verdana", 11, "bold")).grid(row=0, column=2)

        self.total_drive_time = tk.Label(total_grid, text="0 Minutes")
        self.total_drive_time.grid(row=1, column=0, padx = 20)
        self.total_hair_time = tk.Label(total_grid, text="0 Minutes")
        self.total_hair_time.grid(row=1, column=1, padx = 20)
        self.total_mani_time = tk.Label(total_grid, text="0 Minutes")
        self.total_mani_time.grid(row=1, column=2, padx = 20)

        self.total_drive_price = tk.Label(total_grid, text="$0")
        self.total_drive_price.grid(row=2, column=0)
        self.total_hair_price = tk.Label(total_grid, text="$0")
        self.total_hair_price.grid(row=2, column=1)
        self.total_mani_price = tk.Label(total_grid, text="$0")
        self.total_mani_price.grid(row=2, column=2)

        tk.Label(text = "Total Earnings", font=("Verdana", 16, "bold")).pack()
        self.total_price = tk.Label(text="$0")
        self.total_price.pack()

        # Stop creating all the goddamn widgets #
        
    def create_time_inputs(self, text, column, row):
        tk.Label(self.input_grid, text=text).grid(row=row, column=column)
        rv = tk.Entry(self.input_grid, width=7)
        rv.grid(column=column+1, row=row)
        return rv

    def open_client_list(self):
        now = datetime.now()
        clients = ClientList(self, now.day, now.month, now.year)
        clients.geometry("260x400")
        clients.title("{}/{}/{}".format(now.day, now.month, now.year) + " Clients")

        clients.mainloop()

    def open_delete_clients(self):
        now = datetime.now()
        delete = DeleteClient(self, now.day, now.month, now.year)
        delete.title("{}/{}/{} Clients".format(now.day, now.month, now.year))
        delete.geometry("260x400")
        delete.mainloop()

class DeleteClient(tk.Toplevel):
    def __init__(self, master, day, month, year):
        super().__init__(master)

        self.frame = tk.Frame(self, width=260, height=400)
        self.frame.pack()
        canvas = tk.Canvas(self.frame, width=150, height=400)
        canframe = tk.Frame(canvas)
        canvas.create_window(0,0,window=canframe)
        scrollbar = tk.Scrollbar(self.frame)
        canvas.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command=canvas.yview)
        self.buttons = {}

        try:
            with open("data.json") as file:
                data = json.load(file)
                current_date = "{}/{}/{}".format(day, month, year)
                if data[current_date] == {}: raise KeyError
                for client in data[current_date]:
                    self.buttons[client + "name"] = tk.Label(canframe, text=client, wraplengt=150)
                    self.buttons[client + "name"].pack()
                    self.buttons[client + "address"] = tk.Label(canframe,
                                                                text="Address: " + data[current_date][client]["address"],
                                                                wraplengt=150)
                    self.buttons[client + "address"].pack()
                    self.buttons[client] = tk.Button(canframe, text="Delete",
                                                     command=partial(self.delete_client, master,
                                                                                       client,
                                                                                       data,
                                                                                       current_date))
                    self.buttons[client].pack()
                scrollbar.pack(side="right", fill="y")
                canvas.pack(side="left", expand=True, fill="both")
                self.update()
                canvas.config(scrollregion=canvas.bbox("all"))
        except KeyError: tk.Label(self.frame, text="There are no clients on this day").pack()
        
    def delete_client(self, master, client, data, date):
        del data[date][client]
        self.buttons[client].destroy()
        self.buttons[client + "name"].destroy()
        self.buttons[client + "address"].destroy()
        with open('data.json', 'w') as file: json.dump(data, file)

        
class ClientList(tk.Toplevel):
    def __init__(self, master, day, month, year):
        super().__init__(master)

        frame = tk.Frame(self)
        frame.pack()
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame)
        self.data_list = tk.Listbox(canvas, yscrollcommand=scrollbar.set, width=250, height=600)
        try:
            with open("data.json") as file:
                data = json.load(file)
                current_date = "{}/{}/{}".format(day, month, year)
                if data[current_date] == {}: raise KeyError
                for client in data[current_date]:
                    self.data_list.insert("end", client)
                    self.data_list.insert("end", "Address: " + data[current_date][client]["address"])
                    self.data_list.insert("end", "Driving: " + str(data[current_date][client]["drive"]))
                    self.data_list.insert("end", "Haircutting: " + str(data[current_date][client]["hair"]))
                    self.data_list.insert("end", "Mani: " + str(data[current_date][client]["mani"]))
                    self.data_list.insert("end", "")
            self.data_list.pack(side="left", fill="both")
            scrollbar.config(command=self.data_list.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", expand=True, fill="both")
        except KeyError:
            tk.Label(frame, text="No Clients On This Day").pack()


class Invoice(tk.Toplevel):
    def __init__(self, master, client, address, drive, hair, mani, costs):
        super().__init__(master)

        tk.Label(self, text="Name: " + client, wraplengt=325).pack(anchor="nw")
        tk.Label(self, text="Address: " + address, wraplengt=325).pack(anchor="nw")
        tk.Label(self, text="Driving Time: " + str(drive), wraplengt=325).pack(anchor="nw")
        tk.Label(self, text="Haircutting Time: " + str(hair), wraplengt=325).pack(anchor="nw")
        tk.Label(self, text="Manicuring Time: " + str(mani), wraplengt=325).pack(anchor="nw")
        price = drive*costs['drive'] + hair*costs['hair'] + mani*costs['mani']
        tk.Label(self, text="Cost: " + str(price), wraplengt=325).pack(anchor="nw")
        
