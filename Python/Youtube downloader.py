from pytube import YouTube 
from sys import argv
import PySimpleGUI as sg

def list_unpacker(folder_list):
    if folder_list == []:
        return folder_list
    else:
        #print("list length -1 = " ,len(folder_list)-1, folder_list[len(folder_list)-1], "Folder list: ", folder_list )
        return folder_list[len(folder_list)-1]

layout = [     
        [sg.Text("")],
        [sg.Text("Youtube link", size=(9,1)), sg.Input(key="link", size=(14,1), expand_x=True)],    
        [sg.Text("Output folder", size=(9,1)), sg.Combo(sorted(sg.user_settings_get_entry("-output_path-", [])), 
            default_value= list_unpacker(sg.user_settings_get_entry("-output_path-", [])), size=(10, 1), key="output_path", expand_x=True), sg.FolderBrowse(), sg.Button("Clear History", key = "Clear History")],
        [sg.Radio("High quality", "RadioDemo", default=True, size=(10,1), key="high quality"), 
         sg.Radio("Low quality", "RadioDemo", default=False, size=(10,1), key="low quality"),
         sg.Radio("MP3", "RadioDemo", default=False, size=(10,1), key="mp3")
         ],
        #[sg.ProgressBar(max_value=100, expand_y=True, size=(10,1))],
        [sg.Button("Download", bind_return_key=True), sg.Button("Clear"), sg.Exit(), sg.Sizegrip(key='Grip')],
]

window = sg.Window("Youtube downloader", layout, grab_anywhere=True, keep_on_top=True,  resizable=True ,finalize=True, use_custom_titlebar=True)#, icon=.ICO file used as icon)
window.TKroot.minsize(380,180)
#window.TKroot.maxsize(999999999, 200)

while True:
    event, values = window.read()
    print(event)
    print(values)
    if event == sg.WIN_CLOSED or event == "Exit":
            break

    if event == "Clear":
       window["link"]("")
       window["output_path"]("")

    if event == "Clear History":
        sg.user_settings_set_entry("-output_path-", [])
        window["output_path"].update(values=[], value="")

    if event == "Download":
        sg.user_settings_set_entry("-output_path-", list(sg.user_settings_get_entry("-output_path-", []) + [values["output_path"] ]))
        link = values["link"]
        progress = ""
        yt = YouTube(link, on_progress_callback=progress)
        
        if values["high quality"] == True:
            downloadtype = " High quality.mp4" 
            yd = yt.streams.get_highest_resolution()

        elif values["low quality"] == True:
            downloadtype = " low quality.mp4" 
            yd = yt.streams.get_lowest_resolution()

        elif values["mp3"] == True:
            downloadtype = " audio.mp3"    
            yd = yt.streams.get_audio_only()

        (sg.popup("Download has started!", keep_on_top=True), yd.download(values["output_path"], yt.title + downloadtype))
        sg.popup("Download complete!", keep_on_top=True)

window.close()

