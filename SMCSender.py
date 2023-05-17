import socket
import configparser
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

def update_config(host, port):
    config = configparser.ConfigParser()
    config['Network'] = {
        'ReceiverIP': host,
        'ReceiverPort': port
        }
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def get_config():
    if 'Network' not in config:
        update_config('', 4743)
    config.read(config_file_path)
    host = config['Network']['ReceiverIP']
    port = config['Network']['ReceiverPort']
    return host, port

def save_config():
    host = ip_entry.get()
    port = 4743 # port_entry.get()
    update_config(host, port)
    root.destroy()

def main():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    receiver_ip, receiver_port = get_config()
    print("Connected")
    print("Closing the window will end the connection!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                if event.button == 4:
                    button_state = joystick.get_button(event.button)
                    input_data = f"Button {event.button} {button_state}"
                    send_input(input_data, receiver_ip, receiver_port)

if __name__ == "__main__":
    root = Tk()
    root.title("Sync Mute Control")
    
    window_width = 300
    window_height = 150

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

    """
    port_label = ttk.Label(root, text="Receiver Port:")
    port_label.pack()
    port_entry = ttk.Entry(root)
    port_entry.insert(0, str(get_config()[1]))
    port_entry.pack(pady=5)
    """

    save_button = ttk.Button(root, text="Save", command=save_config)
    save_button.pack(pady=5)
    
    root.mainloop()

    main()

    
