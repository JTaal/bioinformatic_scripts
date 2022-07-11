import os
import datetime
import PySimpleGUI as sg
import pandas as pd
from os import makedirs
from pathlib import Path
from barcode import EAN13
from barcode.writer import ImageWriter
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

#sg.theme_previewer()

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
    doc.save(output_dir + "\\" +  today + " Packing list for " + customer_info_dict["NAME"] + " order " + customer_info_dict["PO"] + shipping_method + ".docx")
    return

def create_table(doc, Pathway, customername):   
    row = {}
    tbl_contents = []
    
    try:
        order_df = pd.read_excel(Pathway, sheet_name="order")
        order_list = order_df.to_dict(orient="records")
    except: 
        sg.popup_auto_close("Couldn't open the order file", keep_on_top=True)
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
                            record["Expiration date"], 
                            int(str(record["Qty"]).split("[")[0]), 
                            int(str(record["Qty"]).split("[")[0]), 
                            "0"
                            ]
            #Change configuration for Turku
            if customername.lower() == "turku":
                row_list = row["cols"]
                if record["Item code"] == "":
                    row_list.insert(1, record["Item code"])
                else:        
                    row_list.insert(1, int(record["Item code"]))
                    
            try:
                if record["Barcode"] != "": 
                    create_barcode(str(record["Barcode"]))
                    row["cols"][0] = InlineImage(doc, create_barcode(record["Barcode"]), width=Mm(30), height=Mm(13.2))
                tbl_contents.append(row.copy())
            except:
                tbl_contents.append(row.copy())
        #Create table headers and finalise function to return the context
        if customername.lower() == "turku":
            col_labels = ["Barcode", "Item code","REF", "Name", "Description", "Unit", "Lot No.", "Expiry date", "Quantity Ordered", "Quantity Shipped", "Back-order"]
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
    
    #Create dictionaries to loop through pathways while clearing and saving
    clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-"}
    folder_dict = {"-path_log-": "log file location", "-path_order-": "ordered items location", "-path_customer-": "customer info location", "-path_output-": "output folder location"}
    customer_input_dict = {"INVOICE_NR": "invoice", "PO": "PO", "DESCRIPTION": "description"}
    
    # in case you load in impossible setting, use below to clear all the saved pathways
    #
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
            customer_dic_names = {"NAME": ""}
    except:
        sg.popup("Couldn't load customer information!", keep_on_top=True)
        customer_dic_names = {"NAME": ""}
    
    #Create the default invoicing number
    current_time = str(datetime.datetime.today())
    default_invoice_number = current_time[2:4] + current_time[5:7] + current_time[8:10]
    
    #Setup the layout of the UI tabs
    Input_Elements = [
        [sg.Text("")],
        [sg.Text("customer", size=(12,1)), sg.Combo(customer_dic_names["NAME"], key="customer name", size=(20, 1))],
        [sg.Text("PO Nr.", size=(12,1)), sg.InputText(key= "PO", size=(40, 1))],
        [sg.Text("Invoice Nr.", size = (12,1)), sg.InputText(key="invoice", size=(40, 1), default_text= default_invoice_number)],
        [sg.Text("Description", size = (12,1)), sg.Combo(["Medical kit", "QTRACE Kit", "QTRACE Assays","Assays", "Plates", "EFS Order", "Hospital Order"] ,key="description", size=(38, 1))],
        [sg.Text("Shipping method", size = (20,1)), sg.Radio("Ambient", "RadioDemo", default=True, size=(10,1), key="ambient"), sg.Radio("Dry Ice", "RadioDemo", default=False, size=(10,1), key="dry ice")],
        [sg.Text("")],
        [sg.Submit(), sg.Button("Clear"), sg.Exit()]
    ]

    Settings = [    
        [sg.Text("")],        
        [sg.Text("log file", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_log-", [])), 
            default_value=  list_unpacker(sg.user_settings_get_entry("-path_log-", [])), size=(30, 1), key="log file location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History log")],
        [sg.Text("ordered items", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_order-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_order-", [])), size=(30, 1), key="ordered items location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History order")],
        [sg.Text("customer sheet", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_customer-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_customer-", [])), size=(30, 1), key="customer info location"), sg.FileBrowse(), sg.Button("Clear History", key = "Clear History customer")],
        [sg.Text("output folder", size=(12,1)), sg.Combo(sorted(sg.user_settings_get_entry("-path_output-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-path_output-", [])), size=(30, 1), key="output folder location"), sg.FolderBrowse(), sg.Button("Clear History", key = "Clear History output")],
        [sg.Text("")],
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
            if values["customer name"] not in customer_dic_names["NAME"] or values["customer name"] == "":
                sg.popup_auto_close("\nThe customer name you've given is not in the database.", keep_on_top=True)
                continue
            
            #Create customer_info_dict of the selected customer
            for record in customer_info_dict_records:
                if record["NAME"] == values["customer name"]:
                    customer_info_dict = record
                    break
            
            for key in customer_input_dict:
                customer_info_dict[key] = values[customer_input_dict[key]]            
            
            #Read in the log file
            #for key in folder_dict:
            #    if values[folder_dict[key]] == "":
            #        values[folder_dict[key]] = base_dir / file_name_dict[]
            
            #Temporary error workaround if location is not given
            if values["log file location"] == "":
                values["log file location"] = base_dir / "Packing list log.xlsx"
            
            
            try:
                excel_path = values["log file location"] 
                df = pd.read_excel(excel_path)
            except:
                sg.popup_auto_close("Couldn't open log file!", keep_on_top=True)
                continue
            #create localS copy of values to manipulate into excel data
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
            keys_to_remove = ["output folder location", "log file location", "ordered items location", "-TAB GROUP-", "Browse", "Browse0", "Browse1",  "Browse2", "dry ice", "ambient", "customer info location"]
            for key in keys_to_remove:
                del log_data[key]
            
            #add data to excel file
            log_data["date"] = current_time
            log_data["Save location"] = values["output folder location"] #Double save location index addition
            df = pd.concat([df, pd.DataFrame(log_data, index=[0])], ignore_index=True)
            df.to_excel(excel_path, index=False)
            #log FILE SAVED##########################
            
            
            doc = DocxTemplate(base_dir / "Mother-packing-list.docx")
            #create_packinglistsheet(customer_info_dict, word_template_path, ordered_items_path, output_dir)
            
            #try:
            create_packinglistsheet(customer_info_dict, doc, create_table(doc, values["ordered items location"], values["customer name"]), values["output folder location"])
            #except:
            #    traceback.print_exc()
            #    sg.popup_auto_close("Couldn't create packing list!", keep_on_top=True)
            #    continue
                
            sg.popup_auto_close("Packing list has been created!", keep_on_top=True)
            continue
            
    window.close()
    return

#start the application
while True:
    try:
        JETA_Packing_list_maker()
    except PermissionError:
        sg.popup_auto_close("Permission error!\nPlease close all relevant documents.", keep_on_top=True)
        continue
    break