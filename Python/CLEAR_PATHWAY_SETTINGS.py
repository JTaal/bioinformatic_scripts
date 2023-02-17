# In case you load in impossible setting (clears all the saved pathways)
import os
import PySimpleGUI as sg

def user_settings(filename = "user_settings.json", path = os.path.dirname(os.path.realpath(__file__)), clear = False):    
    sg.user_settings_filename(filename, path=path)
    if clear == True:
        clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-", "Clear History mother": "-path_mother-"}
        for key in clear_dict:
            sg.user_settings_set_entry(clear_dict[key], [])
        print("Clearing setting files executed!")
    return

user_settings(clear=True)