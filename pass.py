# import tkinter module
import tkinter as tk
from threading import Thread
import os

import time
import hashlib
from pynput import keyboard, mouse
from tkinter import Tk, Label, Entry, Button
from capture import capture_photo
from lock import lock_computer
import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
PASSWORD = os.environ.get("PASSWORD")
# Configuration

FAILED_ATTEMPTS_LIMIT = 3
INITIAL_MOUSE_CLICKS_ALLOWED = 2  # Number of mouse clicks allowed at the start

# Global variables
failed_attempts = 0
monitoring = True
keyboard_listener_active = True  # To pause keyboard tracking
window_open = False  # Track if a Tkinter window is already open
initial_mouse_clicks = 0  # Counter for initial mouse clicks


def show_password_prompt():
    global failed_attempts, monitoring, keyboard_listener_active, window_open

    if window_open:  # If a window is already open, do nothing
        return

    keyboard_listener_active = False
    window_open = True  # Mark the window as open

    # Function to verify the password
    def verify_password():
        entered_password = entry.get()
        print("Entered password:", entered_password)
        if entered_password == PASSWORD:
            print("✅ Password correct. Monitoring stopped.")
            monitoring = False
            root.after(0, root.destroy) 
            os._exit(0) 
        else:
            global failed_attempts
            failed_attempts += 1
            print(f"❌ Incorrect password. Attempt {failed_attempts}/{FAILED_ATTEMPTS_LIMIT}")
            if failed_attempts >= FAILED_ATTEMPTS_LIMIT:
                print("❌ Maximum attempts reached. Locking the computer.")
                capture_photo()
                lock_computer()
                root.after(0, root.destroy)  # Schedule root.destroy() on the main thread
                os._exit(0)  # Terminate the program immediately
            else:
                error_label.config(text=f"Incorrect password. {FAILED_ATTEMPTS_LIMIT - failed_attempts} attempts left.", fg="red")

    # Function to handle window close
    def on_close():
        global window_open
        window_open = False  # Mark the window as closed
        root.destroy()

    # Main application window
    root = tk.Tk()
    root.title("Password Required")
    # root.overrideredirect(True)  
    root.attributes("-fullscreen", True)  # Make the window fullscreen
    root.attributes("-topmost", True)  # Ensure the window stays on top
    
    root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event
    root.configure(bg="#2c3e50")  # Set background color

    # Create a frame for the content
    frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
    frame.pack(expand=True)

    # Title label
    title_label = tk.Label(frame, text="Enter Password", font=("Helvetica", 24, "bold"), bg="#34495e", fg="white")
    title_label.pack(pady=20)

    # Create entry widget
    entry = tk.Entry(frame, width=30, font=("Helvetica", 16), show="*")
    entry.pack(pady=10)

    # Error label
    error_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="#34495e", fg="red")
    error_label.pack(pady=5)

    # Create button to submit the password
    button = tk.Button(frame, text="Submit", command=verify_password, font=("Helvetica", 14), bg="#1abc9c", fg="white", padx=10, pady=5)
    button.pack(pady=20)

    # Display GIF inside Tkinter
    gif_label = tk.Label(frame, bg="#34495e")
    gif_label.pack(pady=20)

    gif_data = imageio.mimread("danger.gif")
    gif_frames = [tk.PhotoImage(file="danger.gif", format=f"gif -index {i}") for i in range(len(gif_data))]

    def update_gif(index):
        frame = gif_frames[index]
        gif_label.configure(image=frame)
        index = (index + 1) % len(gif_frames)
        root.after(100, update_gif, index)

    update_gif(0)

    # Run the application
    root.mainloop()
    keyboard_listener_active = True


# Function to monitor keyboard and mouse activity
def monitor_activity():
    global initial_mouse_clicks
    print("🔒 Monitoring started. Press any key or click to trigger the password prompt.")

    def on_activity():
        global monitoring, initial_mouse_clicks
        if initial_mouse_clicks < INITIAL_MOUSE_CLICKS_ALLOWED:
            initial_mouse_clicks += 1
            print(f"🖱️ Initial mouse click {initial_mouse_clicks}/{INITIAL_MOUSE_CLICKS_ALLOWED} allowed.")
        elif monitoring:
            print("🔒 Activity detected. Prompting for password.")
            show_password_prompt()

    # Keyboard listener
    def on_key_press(_):
        if keyboard_listener_active:  # Only track keyboard if allowed
            on_activity()

    # Mouse listener
    def on_mouse_click(_, __, ___, pressed):
        if pressed:
            on_activity()

    # Start listeners
    with keyboard.Listener(on_press=on_key_press) as keyboard_listener, \
            mouse.Listener(on_click=on_mouse_click) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()


# Main code
def main():
    monitor_thread = Thread(target=monitor_activity)
    monitor_thread.daemon = True
    monitor_thread.start()
    # Keep the program running
    while monitoring:
        time.sleep(1)
    print("🔓 Monitoring stopped.")


main()