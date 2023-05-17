import socket
import keyboard

def simulate_button_press(button_id, is_pressed):
    if button_id == 4:  # Assuming button 4 represents the Share button
        if is_pressed:
            keyboard.press('f23')
            keyboard.press('f24')
        else:
            keyboard.release('f23')
            keyboard.release('f24')

def receive_input(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", port))
    sock.listen(1)
    print("Connected")
    print("Closing the window will end the connection!")
    print("You may have to press anykey if it doesn't recieve anything.")
    while True:
        conn, _ = sock.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            button_data = data.decode().split()
            button_id = int(button_data[1])
            is_pressed = bool(int(button_data[2]))
            simulate_button_press(button_id, is_pressed)

def main():
    # Reciever PC network configuration
    receiver_port = 4743
    receive_input(receiver_port)

if __name__ == "__main__":
    main()
