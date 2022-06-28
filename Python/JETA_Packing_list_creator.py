#GUI creator
import datetime
import os
import PySimpleGUI as sg
import pandas as pd
from pathlib import Path
from os.path import isfile

#sg.theme_previewer()

def JETA_Packing_list_maker():  
    #Unpack dictionaries


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            Input 
    
    """
    
    
    file_name_dict = {"log_file_name" : "Packing list log.xlsx", 
    "customer_file_name" : "JETA Packing list customer info.xlsx",
    "items_file_name" : "Order file.xlsx",
    "Mother_packinglist_file_name" : "Mother-packing-list.docx"}
    
    """
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            functions 
    
    """    
    def list_unpacker(folder_list):
        if folder_list == []:
            return folder_list
        else:
            #print("list length -1 = " ,len(folder_list)-1, folder_list[len(folder_list)-1], "Folder list: ", folder_list )
            return folder_list[len(folder_list)-1]        

    
    """
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            GUI setup
    
    """
    

    
    #Create theme
    sg.theme("DarkTeal9")
    
    #Create dictionaries to loop through pathways while clearing and saving
    clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-"}
    folder_dict = {"-path_log-": "Log file location", "-path_order-": "Ordered items location", "-path_customer-": "Customer info location", "-path_output-": "Output folder location"}
    
    
    # in case you load in impossible setting use below to clear all the saved pathways
    #
    #for event in clear_dict:
    #    sg.user_settings_set_entry(clear_dict[event], [])
    
    #Create default pathways for initial use
    base_dir = Path(__file__).parent / "required files"
    os.makedirs(base_dir, exist_ok=True)
    
    #Create dictionary list for customer names
    customer_path = base_dir / "JETA Packing list customer info.xlsx"
    
    
    if isfile(customer_path):
        customerdf = pd.read_excel(customer_path, sheet_name="Customer info")
        customer_dic_names = customerdf.to_dict(orient="list")
    else:
        print("Couldn't load customer information!")
        customer_dic_names = {"name": ""}
    
    #Create the default invoicing number
    current_time = str(datetime.datetime.today())
    default_invoice_number = current_time[2:4] + current_time[5:7] + current_time[8:10]
    
    #Setup the layout of the UI tabs
    Input_Elements = [
        [sg.Text("")],
        [sg.Text("Customer", size=(12,1)), sg.Combo(customer_dic_names["name"], key="customer name", size=(20, 1))],
        [sg.Text("PO Nr.", size=(12,1)), sg.InputText(key= "PO", size=(40, 1))],
        [sg.Text("Invoice Nr.", size = (12,1)), sg.InputText(key="invoice", size=(40, 1), default_text= default_invoice_number)],
        [sg.Text("Description", size = (12,1)), sg.Combo(["Medical kit", "Assays", "Plates"] ,key="description", size=(38, 1))],
        [sg.Text("Shipping method", size = (20,1)), sg.Radio("Ambient", "RadioDemo", default=True, size=(10,1), key="ambient"), sg.Radio("Dry Ice", "RadioDemo", default=False, size=(10,1), key="dry ice")],
        [sg.Text("")],
        [sg.Submit(), sg.Button("Clear"), sg.Exit()]

    ]

    Settings = [    
        [sg.Text("")],        
        [sg.Text("Log file", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_log-", [])), 
            default_value=  list_unpacker(sg.user_settings_get_entry("-path_log-", [])), size=(30, 1), key="Log file location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History log")],
        [sg.Text("Ordered items", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_order-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_order-", [])), size=(30, 1), key="Ordered items location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History order")],
        [sg.Text("Customer sheet", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_customer-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_customer-", [])), size=(30, 1), key="Customer info location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History customer")],
        [sg.Text("Output folder", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_output-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_output-", [])), size=(30, 1), key="Output folder location"), sg.FolderBrowse(), sg.Button("Clear History", key = "Clear History output")],
        [sg.Text("")],
    #    [sg.Text("Output folder", size=(12,1)), sg.Input(key= "Output folder location"), sg.FolderBrowse()],    
    #    [sg.Text("Log file", size=(12,1)), sg.InputText(key= "Log file location"), sg.FolderBrowse()],
    #    [sg.Text("Ordered items", size=(12,1)), sg.InputText(key= "Ordered items location"), sg.FileBrowse()],
        [sg.Button("Save", bind_return_key=True), sg.Button("Clear"), sg.Exit()]

    ]


    #Combine the tabs into a generals layout of the UI
    layout = [
        
        [sg.TabGroup([[sg.Tab("Input Elements", Input_Elements),
                    sg.Tab("File pathways", Settings)]], key="-TAB GROUP-", expand_x=True, expand_y=True)],
            
    ]

    #Start the program window
    window = sg.Window("JETA Packing list creator", layout, grab_anywhere=True, keep_on_top=True, use_custom_titlebar=True, finalize=True,)
    
    
    #Start an infinite loop to check for user input
    while True:
        event, values = window.read()
        #print(event, type(event)) 
        if event == sg.WIN_CLOSED or event == "Exit" or event == "Exit4":
            break   
            
        if event == "Save":
            for key in folder_dict:
                #Check if path boxes are empty          
                if values[folder_dict.get(key)] == "" or values[folder_dict.get(key)] in sg.user_settings_get_entry(key, []):
                    continue
                #Save the new path into the settings with the old list
                #print("\n\n",key, list(set(sg.user_settings_get_entry(key, []).append( [values[folder_dict.get(key)] ]))))
                
                #print("\n\n", sg.user_settings_get_entry(key, []))
                
                
                sg.user_settings_set_entry(key, list(sg.user_settings_get_entry(key, []) + [values[folder_dict.get(key)] ]))
            sg.popup_auto_close("Pathways have been saved!", keep_on_top=True)
            continue
        
        if "Clear History" in event:
            sg.user_settings_set_entry(clear_dict[event], [])
            window[folder_dict[clear_dict[event]]].update(values=[], value="")
            continue
         
        if event == "Clear" or event == "Clear3":
            for key in values:
                if "Browse" in key or key == '-TAB GROUP-':
                    continue
                window[key]("")
            continue
        
        if event == "Submit" or event == "Enter":
            #Read in the log file
                 
            #for key in folder_dict:
            #    if values[folder_dict[key]] == "":
            #        values[folder_dict[key]] = base_dir / file_name
            
            #Temporary error workaround if location is not given
            if values["Log file location"] == "":
                values["Log file location"] = base_dir / "Packing list log.xlsx"
            
            excel_path = values["Log file location"] 
            
            df = pd.read_excel(excel_path)            
            
            #create localS copy of values to manipulate into excel data
            Excel_Data = values.copy()
            
            #Check which method is selected and add it to the output file
            if Excel_Data["dry ice"] == True:
                Excel_Data["Shipping method"] = "dry ice"
            elif Excel_Data["ambient"] == True:
                Excel_Data["Shipping method"] = "ambient"
            
            #Remove unwanted data from values dictionary
            keys_to_remove = ["Output folder location", "Log file location", "Ordered items location", "-TAB GROUP-", "Browse", "Browse0", "Browse1",  "Browse2", "dry ice", "ambient", "Customer info location"]
            for key in keys_to_remove:
                del Excel_Data[key]
            
            #add data to excel file
            Excel_Data["date"] = current_time
            Excel_Data["Save location"] = excel_path #Double save location index addition
            df = pd.concat([df, pd.DataFrame(Excel_Data,index=[0])], ignore_index=True)
            df.to_excel(excel_path, index=False)
            break
            
    window.close()
    exit()

#start the application or not    
JETA_Packing_list_maker()