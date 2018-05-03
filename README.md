# Unit Standard US18741 Plan

## Brief

The program will be used by a mobile hairdresser, to:
    a) Calculate Pricing of jobs based on minutes worked, and generate invoices of jobs.
    b) Store the information of clients and respective job information.
    
The program will be made with Python 3.5, using tkinter as the base of a GUI interface, to
make the program simple for anybody to use, with clear buttons, entries and instructions.

## Data Sheet

### Global

	def time_to_minutes - take time in hours and minutes and convert it to minutes only
	dict cost - predefine costs to easily change later

### Classes

	class WindowApplication - child class of tk Frame, defines all window widgets and some functionality
		def __init__ - define all widgets
		def open_client_list - create instance of ClientList
		def open_delete_list - create instance of DeleteClient
		def help - open help box
	
	tk.Entry(s) - entries for time in hours and minutes of driving, haircutting and manicuring
	
	class HairdressingApplication - child class of WindowApplication, defines functionality of window
		def add_client - add a client/generate invoice
		def get_totals - get all the totals of the entries
	

	class DeleteClient - tk Toplevel for deleting clients
		def __init__ - initialize window
	class ClientList - tk Toplevel for list of clients
		def __init__ - initialize window
	class Invoice - tk Toplevel for invoice windo
		def __init__ - initialize window
	
## Testing



