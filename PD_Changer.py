from tkinter import *
from datetime import datetime
import requests
from tkcalendar import Calendar, DateEntry
from babel import localedata


master = Tk()
master.title("Change Pitch Demand")
frame = Frame(master)
API_key = ""
server_name = "graham"
site_number = "1"
End_Point = "https://" + server_name + ".leading2lean.com/api/1.0/pitches/set_demand/?auth=" + API_key + "&site=" + site_number

line_options = [
	"0123-BLWM-0001",
	"0123-BLWM-0002",
	"0123-BLWM-0003",
	"0123-BLWM-0005",
	"0123-BLWM-0006",
	"0123-BLWM-0007",
	"0123-BLWM-0008"
]
time_options = [
	"6:30",
	"18:30"
]

def send_demand():
	start_text = start_date.get()
	start_list = start_text.split("/")
	start_time_text = start_time_clicked.get()
	start_time_list = start_time_text.split(":")
	a = datetime((int("20"+start_list[2])),int(start_list[0]),int(start_list[1]),int(start_time_list[0]),int(start_time_list[1]))
	
	end_text = end_date.get()
	end_list = end_text.split("/")
	end_time_text = end_time_clicked.get()
	end_time_list = end_time_text.split(":")
	b = datetime((int("20"+end_list[2])),int(end_list[0]),int(end_list[1]),int(end_time_list[0]),int(end_time_list[1]))
	c = b-a
	hours = c.total_seconds()/3600

	line_text = clicked.get()
	
	demand = demand_var.get()
	demand = int(demand) * hours
	demand_total = format(demand,".0f")
	
	start_formatted = "20"+start_list[2]+"-"+start_list[0]+"-"+start_list[1] + " " + start_time_text
	end_formatted = "20"+end_list[2]+"-"+end_list[0]+"-"+end_list[1] + " " + end_time_text
	parameters = {
		'site':1,
		'linecode':line_text,
		'start': start_formatted,
		'end': end_formatted,
		'demand': demand_total	
	}
	setdemand = requests.post(End_Point, data=parameters, verify=False, proxies=proxies)
	response = setdemand.json().get("success")

	if response:
		label2.config(text="True")
	else:
		label2.config(text=setdemand.text)

start_date_label = Label(master, text="choose start date").grid(row=0,column=0)
start_date = DateEntry(master)
start_date.grid(row=0,column=1)

start_time_label = Label(master, text="choose start time").grid(row=0, column=2)
start_time_clicked = StringVar()
start_time_clicked.set(time_options[0])
start_time = OptionMenu(master, start_time_clicked, *time_options)
start_time.grid(row=0,column=3)


end_date_label = Label(master, text="choose end date").grid(row=1,column=0)
end_date = DateEntry(master)
end_date.grid(row=1,column=1)

end_time_label = Label(master, text="choose end time").grid(row=1, column=2)
end_time_clicked = StringVar()
end_time_clicked.set(time_options[0])
end_time = OptionMenu(master, end_time_clicked, *time_options)
end_time.grid(row=1,column=3)

demand_var = StringVar()
demand_label = Label(master,text="Desired demand per hour").grid(row=3,column=0,columnspan=2)
demand_entry = Entry(master,textvariable=demand_var).grid(row=3,column=2,columnspan=2)

clicked = StringVar()
clicked.set(line_options[0])

drop = OptionMenu(master, clicked, *line_options)
drop.grid(row=2,column=0,columnspan=4)

call_button = Button(master, text="Set Demand", command=send_demand).grid(row=4,column=0,columnspan=4)

label1 = Label(master,text="Set Demand Success")
label1.grid(row=5,column=0,columnspan=2)

label2 = Label(master, text="")
label2.grid(row=5,column=2,columnspan=2)





mainloop()