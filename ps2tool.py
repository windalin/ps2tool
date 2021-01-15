import time
import threading
import os
import urllib.request
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.colorchooser
from tkinter import ttk
from configparser import ConfigParser
from shutil import copyfile
from datetime import datetime

#external libraries
import pygetwindow
import pyautogui


start = time.time()

#======================CLASSES
class MyEntry(tkinter.Entry):
    def set_text(self, text_in):
        self.delete(0, tkinter.END)
        self.insert(0, text_in)

class MyCheckbutton(tkinter.Checkbutton):
    def __init__(self, on_off):
        self.my_variable = tkinter.StringVar()
        self.my_variable.set(on_off)
        super().__init__(offvalue="0", onvalue="1", variable=self.my_variable, command=self.placeholder)

    def refresh(self, on_off):
        self.my_variable.set(on_off)

    def placeholder(self):
        pass

class MyCombobox(ttk.Combobox):
    def __init__(self, options_list, action_on_select=None):
        super().__init__(values=options_list, width=60)
        self.bind("<<ComboboxSelected>>", self.selected)
        self.action_on_select = action_on_select

    def set_options(self, options_list):
        self["values"] = options_list

    def add_option(self, new_option):
        temp = list(self["values"])
        if new_option not in temp:
            temp.append(new_option)
        self["values"] = temp
        self.set(new_option)
        self.selected(None)

    def selected(self, event):
        if self.action_on_select == "colour":
            colours = get_config_colours(self.get())
            if colours != None:
                set_colours(colours)
        elif self.action_on_select == "server":
            server = self.get()
            settings["most_recent_world"] = server
            update_pop_labels(server)

#======================FUNCTIONS
def get_config_colours(ini_file):
    config.read(ini_file)
    if config.getint("UI", "TintModeReticuleStyle") == 0:
        tkinter.messagebox.showwarning(title="TintModeReticuleStyle", message="TintModeReticuleStyle must be set to 1 in the .ini file in order to use custom reticule colours, restart this tool.")

    try:
        return[config.getint("UI", "TintModeReticuleColor"), config.getint("UI", "NoDeployZoneColor"), config.getint("UI", "OrbitalStrikeColor")]
    except:
        print("\nThe selected .ini file is missing 1 or more colour option lines under the UI section")
        return [0, 0, 0]

def get_default_colours():
    global default_colours
    default_colours = [config.getint("UI", "TintModeReticuleColor"), config.getint("UI", "NoDeployZoneColor"), config.getint("UI", "OrbitalStrikeColor")]
        
def parse_settings(filename):  
    global data
    data = []
    
    file = open(filename)
    line = file.readline()
    while line:
        if line != "\n":
            line = line.rstrip()
        data.append(line)
        line = file.readline()
        
    print("\ndata (settings lines) on parse")
    for i in range(len(data)):
        print([data[i]])
        if data[i] in settings.keys():
            if type(settings[data[i]]) == str:
                if data[i+1] != "\n":
                    settings[data[i]] = data[i+1]
                else:
                    settings[data[i]] = ""
            elif type(settings[data[i]]) == list:
                settings[data[i]] = data[i+1].split(",")

    print("\nsettings dict on parse")
    for item in settings.items():
        print(item)

    file.close()

def browse_path(entry=None, combobox=None):
    filename = tkinter.filedialog.askopenfilename()

    if filename != "":
        if entry != None:
            entry.set_text(filename)

        if combobox != None:
            combobox.add_option(filename) 

def write_to_settings(filename, reset=False):
    file = open(filename, mode="w")

    if reset:
        data_to_write = default_data
    else:
        data_to_write = data

    print("\ndata (settings lines) on write")
    for item in data_to_write:
        if "\n" not in item and item != "end":
            item = item + "\n"
        print([item])
        file.write(item)
    
    file.close()

def apply_changes():
    #get ps2 window
    try:
        launchpad_window = pygetwindow.getWindowsWithTitle("Planetside 2")[0]
        
    except:
        launchpad_window = None
        print("Launchpad window not found")
    
    s = time.time()
    settings["recursion_path"] = recursion_entry.get()
    settings["start_with_recursion"] = recursion_checkbutton.my_variable.get()
    settings["other_fonts"] = list(font_combobox["values"])
    settings["most_recent_font"] = font_combobox.get()
    settings["other_useroptions"] = list(useroptions_combobox["values"])
    settings["most_recent_useroptions"] = useroptions_combobox.get()

    print("\nsettings dict on apply")
    for item in settings.items():
        print(item)

    for key in settings.keys():
        try:
            index = data.index(key)
            if type(settings[key]) == str:
                data[index+1] = settings[key]
            elif type(settings[key]) == list:
                data[index+1] = (",").join(settings[key])
        except:
            pass
            
##    print("\ndata on apply")
##    for item in data:
##        print([item])

    write_to_settings(settings_file)

    if settings["most_recent_font"] == "default" or settings["most_recent_font"] == "":
        try:
            copyfile("Geo-Md.ttf", "UI/Resource/Fonts/Geo-Md.ttf")
        except:
            print("\nGeo-Md.ttf file missing or invalid, font was not changed to default")
    else:
        copyfile(settings["most_recent_font"], "UI/Resource/Fonts/Geo-Md.ttf")

    if settings["most_recent_useroptions"] != "UserOptions.ini" and settings["most_recent_useroptions"] != "":
        copyfile(settings["most_recent_useroptions"], "Useroptions.ini")

    #if settings["start_with_recursion"] == "1" and settings["recursion_path"] != "\n":
        #os.startfile(settings["recursion_path"])

    selected_ini_file = useroptions_combobox.get()
    config.read(selected_ini_file)
    config.set("UI", "TintModeReticuleColor", str(settings["reticule_colour"]))
    config.set("UI", "NoDeployZoneColor", str(settings["no_deploy_colour"]))
    config.set("UI", "OrbitalStrikeColor", str(settings["orbital_strike_colour"]))
    with open(selected_ini_file, "w") as configfile:
        config.write(configfile)

    print()
    print(time.time() - s, "seconds to apply changes")

    if launchpad_window:
        print("Launchpad window found")
        launchpad_window.activate()
        #752, 522
        play_button_x = launchpad_window.left + 752
        play_button_y = launchpad_window.top + 522
        pyautogui.click(play_button_x, play_button_y)
    else:
        print("Launchpad window not found")

    window.destroy()

def set_colours(colours): #index 012 for reticule nodeploy orbital
    reticule_colour_label2.configure(bg=decimal_to_tkinter(colours[0]), text=str(colours[0]), fg=white_or_black(colours[0]))
    no_deploy_zone_label2.configure(bg=decimal_to_tkinter(colours[1]), text=str(colours[1]), fg=white_or_black(colours[1]))
    orbital_strike_colour_label2.configure(bg=decimal_to_tkinter(colours[2]), text=str(colours[2]), fg=white_or_black(colours[2]))

def reset_settings():
    if tkinter.messagebox.askquestion("Reset settings", "Reset settings?") == "yes":
        set_colours(default_colours) #colours from most_recent_useroptions are used as default colours
       
        write_to_settings(settings_file, reset=True)
        parse_settings(settings_file)

        recursion_entry.set_text(settings["recursion_path"])
        recursion_checkbutton.refresh(settings["start_with_recursion"])
        font_combobox.set(settings["most_recent_font"])
        useroptions_combobox.set(settings["most_recent_useroptions"])

        copyfile("Geo-Md.ttf", "UI/Resource/Fonts/Geo-Md.ttf")

def decimal_to_rgb(decimal):    
    binary_colour = bin(decimal)[2:]
    binary_colour = (24 - len(binary_colour)) * "0" + binary_colour

    return (int(binary_colour[:8], 2), int(binary_colour[8:16], 2), int(binary_colour[16:24], 2))

def rgb_to_tkinter(rgb):
    return "#%02x%02x%02x" % rgb

def hex_to_decimal(hex_in):
    if hex_in[0] == "#":
        hex_in = hex_in[1:]

    return int(hex_in, 16)

def decimal_to_tkinter(decimal):  
    return rgb_to_tkinter(decimal_to_rgb(decimal))

def white_or_black(decimal): #from https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
    rgb = decimal_to_rgb(decimal)
    
    if (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) > 150:
        return "black"
    else:
        return "white"

def browse_colour(dict_key, label_to_change, decimal):
    print("\ncurrent", dict_key, "is:", settings[dict_key])
    
    colour = tkinter.colorchooser.askcolor(color=decimal_to_tkinter(decimal))

    if colour[1] != None:
        new_decimal = hex_to_decimal(colour[1])
        print("    new", dict_key, "is:", new_decimal)        
        settings[dict_key] = new_decimal
        label_to_change.configure(bg=decimal_to_tkinter(new_decimal), text=str(new_decimal), fg=white_or_black(new_decimal))

def kill_msi_afterburner():
    print()
    kill_msi = os.system("taskkill /f /t /im MSIAfterburner.exe")
    if kill_msi == 0:
        print("MSI afterburner killed, taskkill code: 0")
    else:
        print("MSI afterburner not killed, taskkill code:", kill_msi)

def close_everything(close_self=False):
    print()
    
    kill_recursion = os.system("taskkill /f /t /im RTST.exe")
    if kill_recursion == 0:
        print("recursion killed, taskkill code: 0")
    else:
        print("recursion not killed, taskkill code:", kill_recursion)

    kill_launchpad = os.system("taskkill /f /t /im LaunchPad.exe")
    if kill_launchpad == 0:
        print("launchpad killed, taskkill code: 0")
    else:
        print("launchpad not killed, taskkill code:", kill_launchpad)

    if close_self:
        window.destroy()

#second thread
def get_population():
    print("\nget pop started")
    pop_label = tkinter.Label(text="Getting server population from fisu API...")
    pop_label.grid(row=1, column=4, columnspan=2, padx=(60, 0), sticky="W")

    server_combobox = MyCombobox(worlds_names, action_on_select="server")
    server_combobox.configure(width=40)
    server_combobox.grid(row=2, column=4, columnspan=2, padx=(62, 0), sticky="W")
    server_combobox.set(settings["most_recent_world"])
    
    start1 = time.time()
   
    pop_data = urllib.request.urlopen("https://ps2.fisu.pw/api/population/?world=1,10,13,17,40")
    pop_data = pop_data.read().decode("utf-8")
    pop_data = json.loads(pop_data)
    print()
    print(time.time() - start1, "seconds to get data from fisu API")

    global results
    results = pop_data["result"]
    
    vs_label = tkinter.Label(text="VS: ")
    tr_label = tkinter.Label(text="TR: ")
    nc_label = tkinter.Label(text="NC: ")
    vs_label.grid(row=3, column=4, padx=(60, 0), sticky="W")
    tr_label.grid(row=4, column=4, padx=(60, 0), sticky="W")
    nc_label.grid(row=5, column=4, padx=(60, 0), sticky="W")

    global vs_bar, tr_bar, nc_bar, vs_percent_label, tr_percent_label, nc_percent_label
    vs_bar = tkinter.Label(bg="#521c99")
    tr_bar = tkinter.Label(bg="#b32020")
    nc_bar = tkinter.Label(bg="#3089db")
    vs_percent_label = tkinter.Label()
    tr_percent_label = tkinter.Label()
    nc_percent_label = tkinter.Label()

    update_pop_labels(settings["most_recent_world"])

    vs_bar.grid(row=3, column=5, sticky="W")
    tr_bar.grid(row=4, column=5, sticky="W")
    nc_bar.grid(row=5, column=5, sticky="W")
    vs_percent_label.grid(row=3, column=6, padx=5, sticky="W")
    tr_percent_label.grid(row=4, column=6, padx=5, sticky="W")
    nc_percent_label.grid(row=5, column=6, padx=5, sticky="W")

    now = datetime.now()
    string = "Server population fetched at " + now.strftime("%H:%M %p")
    pop_label.configure(text=string)

def update_pop_labels(server):
    world_id = server_to_id(server)
    
    info = results[world_id][0]
    total_pop = info["vs"] + info["tr"] + info["nc"]

    vs_percent = round((info["vs"] / total_pop) * 100)
    tr_percent = round((info["tr"] / total_pop) * 100)
    nc_percent = round((info["nc"] / total_pop) * 100)
    max_percent = max(vs_percent, tr_percent, nc_percent)
    vs_width = round((vs_percent / max_percent) * 30)
    tr_width = round((tr_percent / max_percent) * 30)
    nc_width = round((nc_percent / max_percent) * 30)
    
    print("\nUpdate population for:", server)
    print("Total pop:", total_pop)
    print("VS: ", info["vs"], " | ", vs_percent, "%", sep="")
    print("TR: ", info["tr"], " | ", tr_percent, "%", sep="")
    print("NC: ", info["nc"], " | ", nc_percent, "%", sep="")

    vs_bar.configure(width=vs_width)
    tr_bar.configure(width=tr_width)
    nc_bar.configure(width=nc_width)
    vs_percent_label.configure(text=str(vs_percent) + "% | " + str(info["vs"]))
    tr_percent_label.configure(text=str(tr_percent) + "% | " + str(info["tr"]))
    nc_percent_label.configure(text=str(nc_percent) + "% | " + str(info["nc"]))
    
def server_to_id(server):
    return worlds_ids[worlds_names.index(server)]

#third thread
def not_top():
    time.sleep(5)
    window.after_idle(window.attributes, '-topmost', False)
    
#======================INITIALISE
window = tkinter.Tk()

#run second thread for pop data
thread2 = threading.Thread(target=get_population, args=())
thread2.start()

print("\nmain123")
window.title("PS2 tool")
window.geometry("1100x250")

worlds_ids = ["1", "10", "13", "17", "40"]
worlds_names = ["Connery", "Miller", "Cobalt", "Emerald", "Soltech"]

data = []    
default_data = ["recursion_path", "\n", "start_with_recursion", "0", "other_fonts", "default", "most_recent_font", "default", "other_useroptions", "UserOptions.ini", "most_recent_useroptions", "UserOptions.ini", "most_recent_world", "Connery", "is_default_settings", "1", "end"]
default_colours = [0, 0, 0]

config = ConfigParser()
config.read("UserOptions.ini")

settings_file = "settings.txt"
settings = {"recursion_path":"",
            "start_with_recursion":"",
            "other_fonts":[],
            "most_recent_font":"",
            "other_useroptions":[],
            "most_recent_useroptions":"",
            "reticule_colour":0,
            "no_deploy_colour":0,
            "orbital_strike_colour":0,
            "most_recent_world":"",

            "is_default_settings":""}

parse_settings(settings_file)
default_colours = get_config_colours("UserOptions.ini")
settings["reticule_colour"] = default_colours[0]
settings["no_deploy_colour"] = default_colours[1]
settings["orbital_strike_colour"] = default_colours[2]

copyfile("Geo-Md.ttf", "UI/Resource/Fonts/Geo-Md.ttf")
#print(data)
if settings["start_with_recursion"] == "1":
    os.startfile(settings["recursion_path"])
os.startfile("LaunchPad.exe")
#kill_msi_afterburner()

#======================WIDGETS
#use custom reticule colour
##custom_reticule_label = tkinter.Label(text="Use custom reticule colour")
##custom_reticule_label.grid(row=21, column=1, sticky="EW")
    
#orbital strike colour row 7
orbital_strike_colour_label = tkinter.Label(text="Orbital strike colour")
orbital_strike_colour_label.grid(row=7, column=1, sticky="W")

orbital_strike_colour_label2 = tkinter.Label(text=settings["orbital_strike_colour"], width=15, bg=rgb_to_tkinter(decimal_to_rgb(settings["orbital_strike_colour"])), borderwidth=2, relief="groove")
orbital_strike_colour_label2.grid(row=7, column=2, sticky="W")
orbital_strike_colour_label2.configure(fg=white_or_black(settings["orbital_strike_colour"]))

orbital_strike_colour_add = tkinter.Button(text="Choose orbital strike colour", command=lambda: browse_colour("orbital_strike_colour", orbital_strike_colour_label2, settings["orbital_strike_colour"]))
orbital_strike_colour_add.grid(row=7, column=3, sticky="EW")

#no deploy zone colour row 6
no_deploy_zone_label = tkinter.Label(text="No deploy zone colour")
no_deploy_zone_label.grid(row=6, column=1, sticky="W")

no_deploy_zone_label2 = tkinter.Label(text=settings["no_deploy_colour"], width=15, bg=rgb_to_tkinter(decimal_to_rgb(settings["no_deploy_colour"])), borderwidth=2, relief="groove")
no_deploy_zone_label2.grid(row=6, column=2, sticky="W")
no_deploy_zone_label2.configure(fg=white_or_black(settings["no_deploy_colour"]))

no_deploy_zone_colour_add = tkinter.Button(text="Choose no deploy zone colour", command=lambda: browse_colour("no_deploy_colour", no_deploy_zone_label2, settings["no_deploy_colour"]))
no_deploy_zone_colour_add.grid(row=6, column=3, sticky="EW")

#reticule colour row 5
reticule_colour_label = tkinter.Label(text="Reticule colour")
reticule_colour_label.grid(row=5, column=1, sticky="W")

reticule_colour_label2 = tkinter.Label(text=settings["reticule_colour"], width=15, bg=rgb_to_tkinter(decimal_to_rgb(settings["reticule_colour"])), borderwidth=2, relief="groove")
reticule_colour_label2.grid(row=5, column=2, sticky="W")
reticule_colour_label2.configure(fg=white_or_black(settings["reticule_colour"]))

reticule_colour_add = tkinter.Button(text="Choose reticule colour", command=lambda: browse_colour("reticule_colour", reticule_colour_label2, settings["reticule_colour"]))
reticule_colour_add.grid(row=5, column=3, sticky="EW")

#useroptions row 4
useroptions_label = tkinter.Label(text="Choose .ini file")
useroptions_label.grid(row=4, column=1, sticky="W")

useroptions_combobox = MyCombobox(settings["other_useroptions"], action_on_select="colour")
useroptions_combobox.set(settings["most_recent_useroptions"])
useroptions_combobox.grid(row=4, column=2, sticky="W")

useroptions_add = tkinter.Button(text="Add .ini file", command=lambda: browse_path(entry=None, combobox=useroptions_combobox))
useroptions_add.grid(row=4, column=3, sticky="EW")

#fonts row 3
font_label = tkinter.Label(text="Choose .ttf font file")
font_label.grid(row=3, column=1, sticky="W")

font_combobox = MyCombobox(settings["other_fonts"])
font_combobox.set(settings["most_recent_font"])
font_combobox.grid(row=3, column=2, sticky="W")

font_add = tkinter.Button(text="Add .ttf font", command=lambda: browse_path(entry=None, combobox=font_combobox))
font_add.grid(row=3, column=3, sticky="EW")

#recursion row 1, 2
recursion_label = tkinter.Label(text="Recursion path")
recursion_label.grid(row=1, column=1, sticky="W")

recursion_entry = MyEntry(width=20)
recursion_entry.set_text(settings["recursion_path"])
recursion_entry.grid(row=1, column=2, sticky="EW")

recursion_browse = tkinter.Button(text="Browse for RTST.exe", command=lambda: browse_path(entry=recursion_entry, combobox=None))
recursion_browse.grid(row=1, column=3, sticky="EW")

start_recursion_label = tkinter.Label(text="Start Recursion with this")
start_recursion_label.grid(row=2, column=1, sticky="W")

recursion_checkbutton = MyCheckbutton(settings["start_with_recursion"])
recursion_checkbutton.grid(row=2, column=2, sticky="W")

#reset settings button last row
reset_settings_button = tkinter.Button(text="Reset settings", width=18, command=lambda: reset_settings())
reset_settings_button.grid(row=6, column=4, columnspan=2, padx=(60, 0), sticky="W")

#apply changes button last row
apply_changes_button = tkinter.Button(text="Apply changes", width=14, command=lambda: apply_changes())
apply_changes_button.grid(row=20, column=1, sticky="W")
    
#don't want to play
close_everything_button = tkinter.Button(text="I don't want to play", width=18, command=lambda: close_everything(True))
close_everything_button.grid(row=7, column=4, columnspan=2, padx=(60, 0), sticky="W")

#test button
##test_button = tkinter.Button(text="test", command=test123)
##test_button.grid(row=55, column=1)

#start launchpad
##start_launchpad = tkinter.Button(text="Start Launchpad", width=14, command=lambda: os.startfile("LaunchPad.exe"))
##start_launchpad.grid(row=21, column=1, sticky="W")

print()
print(time.time() - start, "seconds for main thread")

window.lift()
window.attributes('-topmost', True)

thread3 = threading.Thread(target=not_top, args=())
thread3.start()

window.mainloop()

