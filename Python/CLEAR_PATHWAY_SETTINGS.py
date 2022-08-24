# In case you load in impossible setting (clears all the saved pathways)
import os
import PySimpleGUI as sg

sg.user_settings_filename("user_settings.json", path = os.curdir)

clear_dict = {"Clear History log": "-path_log-", "Clear History order": "-path_order-", "Clear History customer": "-path_customer-", "Clear History output": "-path_output-", "Clear History mother": "-path_mother-"}
for event in clear_dict:
    sg.user_settings_set_entry(clear_dict[event], [])