import os
import datetime
from random import random
import PySimpleGUI as sg
import pandas as pd
from time import time
from os import makedirs
from os.path import isfile
from pathlib import Path
from barcode import EAN13
from barcode.writer import ImageWriter
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

#sg.theme_previewer()
#Set default pathway for user settings inside of the folder the script is executed from
def user_settings(filename = "user_settings.json", path = os.path.dirname(os.path.realpath(__file__)), clear = False):    
    #if os.path.exists(os.path.join(path,filename))== False: #THIS LINE WILL WILL CREATE A DEFAULT SETTINGS FILE IF USED WHEN USER_SETTINGS.json ALREADY EXIST IN THE FOLDER. SO DON'T USE UNLESS YOU FIX IT
    sg.user_settings_filename(filename, path=path)
    if clear == True:
        clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-", "Clear History mother": "-path_mother-"}
        for key in clear_dict:
            sg.user_settings_set_entry(clear_dict[key], [])
    return

def True_or_False_random():
    nr = random()
    if nr <= 0.5:
        return True
    if nr > 0.5:
        return False 

def isNaN(num):
    return num != num

def create_barcode(number_string):   
    base_dir = Path(__file__).parent / "barcodes"
    makedirs(base_dir, exist_ok=True)
    barcode = EAN13(number_string, writer=ImageWriter())
    return barcode.save(base_dir/number_string)

def create_packinglistsheet(customer_info_dict , doc, order_table_dict, output_dir):
    #Create dates and insert into the input dict
    today_text = f"{datetime.datetime.now():%d-%m-%Y}"
    customer_info_dict["DATE"] = today_text
    today = today_text[8:10] + today_text[3:5] + today_text[:2]
    shipping_method = " " + customer_info_dict.pop("shipping method")

    #Merge info with table 
    context = customer_info_dict | order_table_dict
    #Create packinglist from motherpacking list and input info
    #filter out dead values and insert nothing into them
    for key in context:
        if isNaN(context[key]):
            context.update({key : ""})
    
    doc.render(context)
    doc.save(output_dir + "\\" +  today + " Packing list for " + customer_info_dict["DISPLAY_NAME"] + " order " + customer_info_dict["PO"] + shipping_method + ".docx")
    return

def create_table(doc, Pathway, customername):   
    row = {}
    tbl_contents = []
    
    try:
        order_df = pd.read_excel(Pathway, sheet_name="order")
        order_list = order_df.to_dict(orient="records")
    except Exception as exception: 
        sg.popup_auto_close("Couldn't open the order file\n\n" + str(exception), keep_on_top=True)
        context = {}
        return context
    else:
        for record in order_list:
            for key in record:
                if isNaN(record[key]):
                    record[key] = ""
            #Create default table layout        
            if (type(record["Barcode"]) == str or type(record["Barcode"]) == float) and record["Barcode"] != "":
                record["Barcode"] = str(int(float(record["Barcode"])))
            row["cols"] = [ record["Barcode"],
                            record["REF"], 
                            record["Name"], 
                            record["Description"], 
                            record["Category"], 
                            record["LOT"], 
                            record["Expiration_date"], 
                            int(str(record["Qty"]).split("[")[0]), 
                            int(str(record["Qty"]).split("[")[0]), 
                            "0"
                            ]
            #Change configuration for Turku
            if customername.lower() == "turku":
                row["cols"].insert(2, record["Item_code"])
            #if customername.lower() == "exception customer":
            #    special_case = "Whatever you need that is special"
            try:
                if record["Barcode"] != "":
                    row["cols"][0] = InlineImage(doc, create_barcode(str(record["Barcode"])), width=Mm(30), height=Mm(13.2))
                tbl_contents.append(row.copy())
            except:
                tbl_contents.append(row.copy())
        #Create table headers and finalise function to return the context
        if customername.lower() == "turku":
            col_labels = ["Barcode", "REF", "Item code", "Name", "Description", "Unit", "Lot No.", "Expiry date", "Quantity Ordered", "Quantity Shipped", "Back-order"]
        #elif other customer exceptions:
        else:
            col_labels = ["Barcode", "REF", "Name", "Description", "Unit", "Lot No.", "Expiry date", "Quantity Ordered", "Quantity Shipped", "Back-order"]
    context = {"col_labels" : col_labels, "tbl_contents": tbl_contents}
    return context

def JETA_Packing_list_maker():
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
            GUI setup and functionalities
    
    """
    
    #Create theme
    sg.theme("DarkTeal9")
    
    #Create settings location or clear settings
    user_settings(filename= "user_settings.json", path = os.path.dirname(os.path.realpath(__file__)), clear=False)

    #Create dictionaries to loop through pathways while clearing and saving
    clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-", "Clear History mother": "-path_mother-"}
    folder_dict = {"-path_log-": "log file location", "-path_order-": "ordered items location", "-path_customer-": "customer info location", "-path_output-": "output folder location", "-path_mother-": "mother packing list location"}
    customer_input_dict = {"INVOICE_NR": "invoice", "PO": "PO", "DESCRIPTION": "description"}
    
    # in case you load in impossible setting, use below to clear all the saved pathways
    #
    #clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-", "Clear History mother": "-path_mother-"}
    #for event in clear_dict:
    #    sg.user_settings_set_entry(clear_dict[event], [])
    
    #Create default pathways for initial use
    base_dir = Path(__file__).parent / "required files"
    os.makedirs(base_dir, exist_ok=True)
    
    #Create dictionary list for customer names
    customer_path = list_unpacker(sg.user_settings_get_entry("-path_customer-", [])) 
    
    try:
        if type(customer_path) == str:
            customerdf = pd.read_excel(customer_path)
            customer_info_dict_records = customerdf.to_dict(orient="records")
            customer_dic_names = customerdf.to_dict(orient="list")
        elif type(customer_path) == list:
            sg.popup("Customer pathway settings are empty.\nPlease select correct customer pathway and restart.", keep_on_top=True)
            customer_dic_names = {"DISPLAY_NAME": ""}
    except Exception as exception:
        sg.popup("Couldn't load customer information!\n\n" + str(exception), keep_on_top=True)
        customer_dic_names = {"DISPLAY_NAME": ""}
    
    #Create the default invoicing number
    current_time = str(datetime.datetime.today())
    default_invoice_number = current_time[2:4] + current_time[5:7] + current_time[8:10]
    
    #Setup the layout of the UI tabs
    Input_Elements = [
        [sg.Text("")],
        [sg.Text("Customer", size=(12,1)), sg.Combo(customer_dic_names["DISPLAY_NAME"], key="customer name", size=(20, 1))],
        [sg.Text("PO Nr.", size=(12,1)), sg.InputText(key= "PO", size=(40, 1))],
        [sg.Text("Invoice Nr.", size = (12,1)), sg.InputText(key="invoice", size=(40, 1), default_text= default_invoice_number)],
        [sg.Text("Description", size = (12,1)), sg.Combo(["Medical kit", "QTRACE Kit", "QTRACE Assays","Assays", "Plates", "EFS Order", "Hospital Order"] ,key="description", size=(38, 1))],
        [sg.Text("Shipping method", size = (20,1)), sg.Radio("Ambient", "RadioDemo", default=True, size=(10,1), key="ambient"), sg.Radio("Dry Ice", "RadioDemo", default=False, size=(10,1), key="dry ice")],
        [sg.Text("")],
        [sg.Submit(), sg.Button("Clear"), sg.Exit()],
    ]

    File_Pathways = [    
        [sg.Text("")],        
        [sg.Text("Log file", size=(14,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_log-", [])), 
            default_value=  list_unpacker(sg.user_settings_get_entry("-path_log-", [])), size=(30, 1), key="log file location", expand_x=True), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History log")],
        [sg.Text("Ordered items", size=(14,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_order-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_order-", [])), size=(30, 1), key="ordered items location", expand_x=True), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History order")],
        [sg.Text("Customer sheet", size=(14,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_customer-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_customer-", [])), size=(30, 1), key="customer info location", expand_x=True), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History customer")],
        [sg.Text("Mother packing list", size=(14,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_mother-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_mother-", [])), size=(30, 1), key="mother packing list location", expand_x=True), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History mother")],
        [sg.Text("")],
        [sg.Button("Save", bind_return_key=True), sg.Button("Clear"), sg.Exit()]
    ]

    Output_pathway = [
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("Output folder", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_output-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_output-", [])), size=(30, 1), key="output folder location", expand_x=True), sg.FolderBrowse(), sg.Button("Clear History", key = "Clear History output")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Text("")],
        [sg.Button("Save", bind_return_key=True), sg.Button("Clear"), sg.Exit()]
    ]

    #Combine the tabs into a generals layout of the UI
    layout = [
        [sg.TabGroup([[sg.Tab("Input Elements", Input_Elements),
                    sg.Tab("File pathways", File_Pathways), 
                    sg.Tab("Output pathway", Output_pathway)]], key="-TAB GROUP-", expand_x=True, expand_y=True)], 
                            [sg.Sizegrip(key='Grip')] 
    ]

    #Start the program window
    global JETA_window
    JETA_window = sg.Window("JETA Packing list creator", layout, grab_anywhere=True, keep_on_top=True,  resizable=True ,finalize=True, use_custom_titlebar=True)#, icon=.ICO file used as icon)
    JETA_window.TKroot.minsize(550,300)
    
    #Start an infinite loop to check for user input
    while True:
        event, values = JETA_window.read()
        #print(event, type(event))
        if event == sg.WIN_CLOSED or event == "Exit" or event == "Exit4" or event == "Exit8":
            break   
            
        if event == "Save" or event == "Save6":
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
            JETA_window[folder_dict[clear_dict[event]]].update(values=[], value="")
            continue
        
        if event == "Clear" or event == "Clear3" or event == "Clear7":
            for key in values:
                if "Browse" in key or key == "-TAB GROUP-" or key == "Grip":
                    continue
                JETA_window[key]("")
            continue
        
        if event == "Submit" or event == "Enter":
            if values["customer name"] not in customer_dic_names["DISPLAY_NAME"] or values["customer name"] == "":
                sg.popup_auto_close("The customer name you've given is not in the database.", keep_on_top=True)
                continue
            
            #Create customer_info_dict of the selected customer
            for record in customer_info_dict_records:
                if record["DISPLAY_NAME"] == values["customer name"]:
                    customer_info_dict = record
                    break
            
            for key in customer_input_dict:
                customer_info_dict[key] = values[customer_input_dict[key]]
            
            #Read in the log file
            #for key in folder_dict:
            #    if values[folder_dict[key]] == "":
            #        values[folder_dict[key]] = base_dir / file_name_dict[]

            #create local copy of values to manipulate into excel data
            log_data = values.copy()
            
            #Check which method is selected and add it to the output file
            if values["dry ice"] == True:
                customer_info_dict["SHIPPING_WARNING"] = "!!! ALL ITEMS NEED TO BE STORED AT -20°C UPON ARRIVAL !!!"
                log_data["shipping method"] = "dry ice"
                customer_info_dict["shipping method"] = "dry ice"
            elif values["ambient"] == True:
                customer_info_dict["SHIPPING_WARNING"] = "STORE AT AMBIENT TEMPERATURE: +15⁰C to +30⁰C"
                log_data["shipping method"] = "ambient"
                customer_info_dict["shipping method"] = "ambient"
            
            #Remove unwanted data from values dictionary
            keys_to_remove = ["output folder location", "log file location", "ordered items location", "-TAB GROUP-", "Browse", "Browse0", "Browse1",  "Browse2", "dry ice", "ambient", "customer info location", "Browse5", "mother packing list location", "Grip"]
            for key in keys_to_remove:
                del log_data[key]

            #Create and save a log file
            if values["log file location"] == "" and isfile(base_dir / "1. Packing list log.xlsx"):
                values["log file location"] = base_dir / "1. Packing list log.xlsx"    
            try:
                excel_path = values["log file location"]
                df = pd.read_excel(excel_path)
                log_data["date"] = current_time
                log_data["Save location"] = values["output folder location"] #Double save location index addition
                df = pd.concat([df, pd.DataFrame(log_data, index=[0])], ignore_index=True)
                df.to_excel(excel_path, index=False)
            except Exception as exception:
                sg.popup_auto_close("Couldn't open log file!\n\n" + str(exception), keep_on_top=True)
            #log FILE SAVED or ERROR CAUGHT##########################

            if values["mother packing list location"] == "" and isfile(base_dir / "4. Mother-packing-list.docx"):
                values["mother packing list location"] = base_dir / "4. Mother-packing-list.docx"
            
            doc = DocxTemplate(values["mother packing list location"])
            #create_packinglistsheet(customer_info_dict, word_template_path, ordered_items_path, output_dir)
            
            #try:
            start = time()
            create_packinglistsheet(customer_info_dict, doc, create_table(doc, values["ordered items location"], values["customer name"]), values["output folder location"])
            end = time()
            #except:
            #    traceback.print_exc()
            #    sg.popup_auto_close("Couldn't create packing list!", keep_on_top=True)
            #    continue
                
            sg.popup("Packing list has been created!","(It took {} seconds!)".format(round(end-start, 2)) , keep_on_top=True)
            continue
            
    JETA_window.close()
    return

#start the application
while True:
    try:
        JETA_Packing_list_maker()
    except PermissionError:
        sg.popup("Permission error!","Please close all relevant documents.", keep_on_top=True)
        JETA_window.close()
        continue
    break