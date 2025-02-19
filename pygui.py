import tkinter as tk
from tkinter import *
from tkinter import ttk
import datetime
from tkcalendar import DateEntry
from SaveDocx import pDocx
from AIResponses import AIResponse
import threading
import json

# Global variables
patients_data = []
providers_data = []
filtered_patients = []
filtered_providers = []

def popup_err(e):
    win = tk.Toplevel()
    win.wm_title("Error")

    l = tk.Label(win, text=e, wraplength=400, justify="center", padx=20, pady=20, bg='#ffdddd', font=('Arial', 12))
    l.pack(padx=20, pady=20)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def popup_gen(t):
    win = tk.Toplevel()
    win.wm_title(t)

    l = tk.Label(win, text=t, wraplength=400, justify="center", padx=20, pady=20, bg='#ddffdd', font=('Arial', 12))
    l.pack(padx=20, pady=20)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def load_company_name():
    try:
        with open('template.txt', 'r') as file:
            company_name = file.readline().strip()
            companyName.set(company_name)
    except Exception as e:
        popup_err(f"Failed to load company name: {e}")

def load_patient_data():
    global patients_data, filtered_patients
    try:
        with open('patients.json', 'r') as file:
            patients_data = json.load(file)
            filtered_patients = patients_data.copy()
            clientName_combo['values'] = [patient['name'] for patient in patients_data]
            update_client_list()
    except Exception as e:
        popup_err(f"Failed to load patient data: {e}")

def load_providers():
    global providers_data, filtered_providers
    try:
        with open('providers.json', 'r') as file:
            providers_data = json.load(file)
            filtered_providers = providers_data.copy()
            serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
            serviceProvidedBy_combo_edit['values'] = [provider['name'] for provider in providers_data]
            update_provider_list()
    except Exception as e:
        popup_err(f"Failed to load providers data: {e}")

def on_client_name_selected(event):
    selected_name = clientName.get()
    for patient in patients_data:
        if patient['name'] == selected_name:
            clientID.set(patient['id'])
            clientDOB.set(patient['dob'])
            serviceProvided.set(patient['service'])
            SupportPlan.set(patient['support_plan'])
            serviceProvidedBy.set(patient.get('provider', ''))
            break

def save_client_data():
    new_patient = {
        "name": clientName.get(),
        "id": clientID.get(),
        "dob": clientDOB.get(),
        "service": serviceProvided.get(),
        "support_plan": SupportPlan.get(),
        "provider": serviceProvidedBy.get()
    }

    # Check if the patient already exists and update their information
    for patient in patients_data:
        if patient['name'] == new_patient['name']:
            patient.update(new_patient)
            break
    else:
        # If the patient does not exist, append the new patient data
        patients_data.append(new_patient)

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client saved successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
    except Exception as e:
        popup_err(f"Failed to save client data: {e}")

def delete_client_data():
    selected_name = clientName.get()
    global patients_data
    patients_data = [patient for patient in patients_data if patient['name'] != selected_name]

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client deleted successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
        clear_client_fields()
    except Exception as e:
        popup_err(f"Failed to delete client data: {e}")

def clear_client_fields():
    clientName.set('')
    clientID.set('')
    clientDOB.set('')
    serviceProvided.set('')
    SupportPlan.set('')
    serviceProvidedBy.set('')

def save_provider_data():
    new_provider = {
        "name": serviceProvidedBy.get()
    }

    # Check if the provider already exists and update their information
    for provider in providers_data:
        if provider['name'] == new_provider['name']:
            provider.update(new_provider)
            break
    else:
        # If the provider does not exist, append the new provider data
        providers_data.append(new_provider)

    try:
        with open('providers.json', 'w') as file:
            json.dump(providers_data, file, indent=4)
        popup_gen("Provider saved successfully.")
        serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
        serviceProvidedBy_combo_edit['values'] = [provider['name'] for provider in providers_data]
        update_provider_list()
    except Exception as e:
        popup_err(f"Failed to save provider data: {e}")

def delete_provider_data():
    selected_name = serviceProvidedBy.get()
    global providers_data
    providers_data = [provider for provider in providers_data if provider['name'] != selected_name]

    try:
        with open('providers.json', 'w') as file:
            json.dump(providers_data, file, indent=4)
        popup_gen("Provider deleted successfully.")
        serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
        serviceProvidedBy_combo_edit['values'] = [provider['name'] for provider in providers_data]
        update_provider_list()
        clear_provider_fields()
    except Exception as e:
        popup_err(f"Failed to delete provider data: {e}")

def clear_provider_fields():
    serviceProvidedBy.set('')

def filter_client_list():
    search_term = search_var.get().lower()
    global filtered_patients
    filtered_patients = [patient for patient in patients_data if search_term in patient['name'].lower()]
    update_client_list()

def filter_provider_list():
    search_term = search_provider_var.get().lower()
    global filtered_providers
    filtered_providers = [provider for provider in providers_data if search_term in provider['name'].lower()]
    update_provider_list()

root = Tk()
root.title("KAP Software | AI Powered Patient Report Generator ")
# root.geometry("1280x800")

bgcolor = '#f6eee0'
appWideFont = ('Times New Roman',16)

root.configure(bg=bgcolor)

style = ttk.Style()
style.configure('TFrame', background=bgcolor)
style.configure('TLabel', background=bgcolor, font=appWideFont)
style.configure('TEntry', font=appWideFont)
style.configure('TButton', font=appWideFont, padding=10)
style.configure('TCombobox', font=appWideFont)

notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, sticky=(N, W, E, S))

descriptionCol = 2
textBoxCol = 3
textboxWidth = 40

def add_labels_entries(panel, labels, variables, row_start):
    for i, (label_text, variable) in enumerate(zip(labels, variables)):
        ttk.Label(panel, text=label_text).grid(column=descriptionCol, row=row_start + i, sticky=W)
        if isinstance(variable, StringVar):
            ttk.Entry(panel, width=textboxWidth, textvariable=variable).grid(column=textBoxCol, row=row_start + i, sticky=(W, E))
        elif isinstance(variable, ttk.Combobox):
            variable.grid(column=textBoxCol, row=row_start + i, sticky=(W, E))
        elif isinstance(variable, DateEntry):
            variable.grid(column=textBoxCol, row=row_start + i, sticky=(W, E))

def add_buttons(panel, buttons, row_start):
    for i, (button_text, command) in enumerate(buttons):
        ttk.Button(panel, text=button_text, command=command).grid(column=descriptionCol, row=row_start + i, columnspan=2, pady=10)

# First Panel
panel1 = ttk.Frame(notebook, padding="20 20 20 20")
panel1.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel1, text='Report Generator')

companyName = StringVar()
clientName = StringVar()
clientID = StringVar()
clientDOB = StringVar()
serviceProvided = StringVar()
serviceProvidedBy = StringVar()
SupportPlan = StringVar()
startDate = StringVar()
endDate = StringVar()

clientName_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=clientName)
clientName_combo.bind("<<ComboboxSelected>>", on_client_name_selected)
serviceProvidedBy_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=serviceProvidedBy)
startDate_entry = DateEntry(panel1, width=textboxWidth - 2, textvariable=startDate, date_pattern='mm/dd/yyyy')
endDate_entry = DateEntry(panel1, width=textboxWidth - 2, textvariable=endDate, date_pattern='mm/dd/yyyy')

labels = ["Company Name", "Client Name", "Client ID", "Client DOB", "Service Provided", "Service Provided By", "Support Plan", "Start Date (month/day/year)", "End Date (month/day/year)"]
variables = [companyName, clientName_combo, clientID, clientDOB, serviceProvided, serviceProvidedBy_combo, SupportPlan, startDate_entry, endDate_entry]

add_labels_entries(panel1, labels, variables, row_start=1)

# Generate time intervals
time_options = [datetime.time(hour=h, minute=m).strftime("%I:%M %p") for h in range(24) for m in (0, 15, 30, 45)]

startTime = StringVar()
endTime = StringVar()

startTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=startTime, values=time_options)
endTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=endTime, values=time_options)

time_labels = ["Start Time", "End Time"]
time_variables = [startTime_combo, endTime_combo]

add_labels_entries(panel1, time_labels, time_variables, row_start=10)

button_state = NORMAL

def genAndSave(progress_callback):
    hourFormat = "%I:%M %p"
    dateFormat = "%m/%d/%Y"
    StartDate = datetime.datetime.strptime(startDate.get(), dateFormat)
    EndDate = datetime.datetime.strptime(endDate.get(), dateFormat)
    StartTime = datetime.datetime.strptime(startTime.get(), hourFormat)
    EndTime = datetime.datetime.strptime(endTime.get(), hourFormat)
    difference = EndDate - StartDate

    currentDate = StartDate

    i = 0
    while i <= difference.days:
        response = AIResponse(clientName.get(), SupportPlan.get())
        pDocx(clientName.get(),
              clientID.get(),
              currentDate,
              response,
              serviceProvided.get(),
              serviceProvidedBy.get(),
              StartTime.strftime(hourFormat),
              EndTime.strftime(hourFormat),
              (EndTime - StartTime),
              (((EndTime - StartTime).seconds / 60) / 60) * 4)
        progress_callback(i)
        currentDate = currentDate + datetime.timedelta(days=1)
        i += 1
    popup_gen('Complete!')

def update_progress(value):
    progress_bar['value'] = value
    panel1.update_idletasks()
    if value == progress_bar['maximum']:
        generate_button['state'] = NORMAL

def runGeneration():
    generate_button['state'] = DISABLED
    def wrapper():
        genAndSave(update_progress)

    thread = threading.Thread(target=wrapper)
    thread.start()

def command():
    try:
        hourFormat = "%I:%M %p"
        dateFormat = "%m/%d/%Y"
        StartDate = datetime.datetime.strptime(startDate.get(), dateFormat)
        EndDate = datetime.datetime.strptime(endDate.get(), dateFormat)
        StartTime = datetime.datetime.strptime(startTime.get(), hourFormat)
        EndTime = datetime.datetime.strptime(endTime.get(), hourFormat)
        difference = EndDate - StartDate
        global progress_bar
        progress_bar = ttk.Progressbar(panel1, maximum=difference.days)
        progress_bar.grid(column=descriptionCol, row=14, columnspan=2, pady=10)
        runGeneration()
    except Exception as e:
        popup_err(e)

progress_var = tk.IntVar()
generate_button = ttk.Button(panel1, text="Generate AI Reports", command=command, state=button_state)
generate_button.grid(column=descriptionCol, row=13, columnspan=2, pady=10)

# Buttons for panel1
panel1_buttons = [("Load Company Name", load_company_name), ("Save Client", save_client_data), ("Save Provider", save_provider_data)]
add_buttons(panel1, panel1_buttons, row_start=15)

# Second Panel for managing clients
panel2 = ttk.Frame(notebook, padding="20 20 20 20")
panel2.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel2, text='Manage Clients')

def update_client_list():
    client_listbox.delete(0, END)
    for patient in filtered_patients:
        client_listbox.insert(END, patient['name'])

def on_client_select(event):
    selected_index = client_listbox.curselection()
    if selected_index:
        selected_patient = filtered_patients[selected_index[0]]
        clientName.set(selected_patient['name'])
        clientID.set(selected_patient['id'])
        clientDOB.set(selected_patient['dob'])
        serviceProvided.set(selected_patient['service'])
        SupportPlan.set(selected_patient['support_plan'])
        serviceProvidedBy.set(selected_patient.get('provider', ''))

search_var = StringVar()
search_entry = ttk.Entry(panel2, width=textboxWidth, textvariable=search_var)
search_entry.grid(column=0, row=0, columnspan=2, sticky=(W),pady=10)
search_entry.bind("<KeyRelease>", lambda event: filter_client_list())

client_listbox = Listbox(panel2, height=20, font=appWideFont)
client_listbox.grid(column=0, row=1, rowspan=8, sticky=(N, S, E, W))
client_listbox.bind("<<ListboxSelect>>", on_client_select)

# Add a frame for editing client details
edit_frame = ttk.Frame(panel2, padding="10 10 10 10")
edit_frame.grid(column=1, row=1, rowspan=8, sticky=(N, S, E, W))

serviceProvidedBy_combo_edit = ttk.Combobox(edit_frame, width=textboxWidth, textvariable=serviceProvidedBy)

edit_labels = ["Client Name", "Client ID", "Client DOB", "Service Provided", "Service Provided By", "Support Plan"]
edit_variables = [clientName, clientID, clientDOB, serviceProvided, serviceProvidedBy_combo_edit, SupportPlan]

add_labels_entries(edit_frame, edit_labels, edit_variables, row_start=0)

# Buttons for panel2
panel2_buttons = [("Save Edited Client", save_client_data), ("Delete Client", delete_client_data), ("New Client", clear_client_fields), ("Load Patient Data", load_patient_data)]
add_buttons(edit_frame, panel2_buttons, row_start=6)

# Third Panel for managing providers
panel3 = ttk.Frame(notebook, padding="20 20 20 20")
panel3.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel3, text='Manage Providers')

def update_provider_list():
    provider_listbox.delete(0, END)
    for provider in filtered_providers:
        provider_listbox.insert(END, provider['name'])

def on_provider_select(event):
    selected_index = provider_listbox.curselection()
    if selected_index:
        selected_provider = filtered_providers[selected_index[0]]
        serviceProvidedBy.set(selected_provider['name'])

search_provider_var = StringVar()
search_provider_entry = ttk.Entry(panel3, width=textboxWidth, textvariable=search_provider_var)
search_provider_entry.grid(column=0, row=0, columnspan=2, sticky=(W),pady=10)
search_provider_entry.bind("<KeyRelease>", lambda event: filter_provider_list())

provider_listbox = Listbox(panel3, height=20, font=appWideFont)
provider_listbox.grid(column=0, row=1, rowspan=8, sticky=(N, S, E, W))
provider_listbox.bind("<<ListboxSelect>>", on_provider_select)

# Add a frame for editing provider details
provider_edit_frame = ttk.Frame(panel3, padding="10 10 10 10")
provider_edit_frame.grid(column=1, row=1, rowspan=8, sticky=(N, S, E, W))

provider_labels = ["Provider Name"]
provider_variables = [serviceProvidedBy]

add_labels_entries(provider_edit_frame, provider_labels, provider_variables, row_start=0)

# Buttons for panel3
panel3_buttons = [("Save Edited Provider", save_provider_data), ("Delete Provider", delete_provider_data), ("Load Provider Data", load_providers)]
add_buttons(provider_edit_frame, panel3_buttons, row_start=1)

# Load patient data on startup
load_patient_data()

# Load providers data on startup
load_providers()

for child in panel1.winfo_children():
    child.grid_configure(padx=10, pady=5)

for child in edit_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()