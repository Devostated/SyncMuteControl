import socket
import configparser
import tkinter
from tkinter import Tk, ttk, Label, Entry, Button
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

appdata_dir = os.getenv('APPDATA')

destination_dir = os.path.join(appdata_dir, 'SyncMuteControl')
os.makedirs(destination_dir, exist_ok=True)

config_file_path = os.path.join(destination_dir, 'config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)

def send_input(input_data, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    sock.sendall(input_data.encode())
    sock.close()

def update_config(host, port, buttonIndex):
    config = configparser.ConfigParser()
    config['Settings'] = {
        'ReceiverIP': host,
        'ReceiverPort': port,
        'ButtonIndex': buttonIndex
        }
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def get_config():
    if 'Settings' not in config:
        update_config('', 4743, 4)
    config.read(config_file_path)
    host = config['Settings']['ReceiverIP']
    port = config['Settings']['ReceiverPort']
    buttonIndex = config['Settings']['Buttonindex']
    return host, port, buttonIndex

def save_config():
    host = ip_entry.get()
    port = 4743 # port_entry.get()
    buttonIndex = button_entry.get()
    update_config(host, port, buttonIndex)
    root.destroy()

def show_hide_buttons():
    if checkbox_var.get() == 1:
        # port_label.pack()
        # port_entry.pack()
        button_label.pack()
        button_entry.pack()
        root.geometry("300x195")
    else:
        # port_label.pack_forget()
        # port_entry.pack_forget()
        button_label.pack_forget()
        button_entry.pack_forget()
        root.geometry("300x110")

def main():
    pygame.init()
    pygame.joystick.init()
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        receiver_ip, receiver_port, button_index = get_config()
        print("Connected")
        print("Closing the window will end the connection!")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                    if event.button == int(button_index):
                        button_state = joystick.get_button(event.button)
                        input_data = f"Button {event.button} {button_state}"
                        try:
                            send_input(input_data, receiver_ip, receiver_port)
                        except:
                            print("Connection interrupted! Press the button again!")
    except:
        print("No controller found!")

if __name__ == "__main__":
    root = Tk()
    root.title("Sync Mute Control")
    
    window_width = 300
    window_height = 110

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    
    ip_label = ttk.Label(root, text="Receiver IP:")
    ip_label.pack()
    ip_entry = ttk.Entry(root, show="*")
    ip_entry.insert(0, get_config()[0]) 
    ip_entry.pack(pady=5)

    # Create a variable to track the checkbox state
    checkbox_var = tkinter.IntVar()
    # Create the checkbox
    checkbox = ttk.Checkbutton(root, text="Advanced Settings", variable=checkbox_var, command=show_hide_buttons)
    checkbox.pack()

    """
    port_label = ttk.Label(root, text="Receiver Port:")
    port_label.pack()
    port_label.pack_forget()
    port_entry = ttk.Entry(root)
    port_entry.insert(0, str(get_config()[1]))
    port_entry.pack(pady=5)
    port_entry.pack_forget()
    """

    # Create the extra buttons
    button_label = ttk.Label(root, text="Button Index:")
    button_label.pack()
    button_label.pack_forget()
    button_entry = ttk.Entry(root)
    button_entry.insert(0, str(get_config()[2]))
    button_entry.pack(pady=5)
    button_entry.pack_forget()

    save_button = ttk.Button(root, text="Save", command=save_config)
    save_button.pack(pady=5)

    root.mainloop()

    main()

    
