import tkinter as tk
from time import strftime, localtime
from datetime import datetime
from PIL import Image, ImageTk
import time
import threading
import os
from playsound import playsound

# Global variables for stopwatch and timer
time_elapsed = 0
timer_time = [0]
running_stopwatch = False
running_timer = False
alarm_time = None

# Update Clock
def update_clock():
    current_time = strftime('%I:%M:%S %p', localtime())
    date = strftime('%A, %B %d, %Y', localtime())
    clock_label.config(text=current_time, fg='black')
    date_label.config(text=date, font=('Arial', 18, 'bold'), fg='#FF4500')
    clock_label.after(1000, update_clock)

# Alarm Function
def check_alarm():
    global alarm_time
    while True:
        if alarm_time and datetime.now().strftime("%H:%M") == alarm_time:
            playsound("bell.wav")  # Play alarm sound
            alarm_time = None
        time.sleep(10)

def set_alarm(hour_var, minute_var):
    global alarm_time
    alarm_time = f"{hour_var.get()}:{minute_var.get()}"
    alarm_label.config(text=f"Alarm set for {alarm_time}")

def open_alarm_window():
    alarm_window = tk.Toplevel(root)
    alarm_window.title("Set Alarm")
    alarm_window.geometry("300x200")
    
    tk.Label(alarm_window, text="Set Alarm Time:", font=('Arial', 14, 'bold')).pack(pady=5)
    
    hour_var = tk.StringVar(value="00")
    minute_var = tk.StringVar(value="00")
    
    hour_spinbox = tk.Spinbox(alarm_window, from_=0, to=23, wrap=True, textvariable=hour_var, width=5, format="%02.0f", font=('Arial', 12))
    minute_spinbox = tk.Spinbox(alarm_window, from_=0, to=59, wrap=True, textvariable=minute_var, width=5, format="%02.0f", font=('Arial', 12))
    
    hour_spinbox.pack(side="left", padx=5)
    tk.Label(alarm_window, text=":", font=('Arial', 14, 'bold')).pack(side="left")
    minute_spinbox.pack(side="left", padx=5)
    
    tk.Button(alarm_window, text="Set Alarm", font=('Arial', 12), command=lambda: set_alarm(hour_var, minute_var)).pack(pady=10)
    
    global alarm_label
    alarm_label = tk.Label(alarm_window, text="No alarm set", font=('Arial', 12))
    alarm_label.pack(pady=5)

    

# Stopwatch Functions
def open_stopwatch_window():
    global running_stopwatch, time_elapsed
    
    def start_stopwatch():
        global running_stopwatch
        running_stopwatch = True
        update_stopwatch()
    
    def stop_stopwatch():
        global running_stopwatch
        running_stopwatch = False
    
    def reset_stopwatch():
        global time_elapsed, running_stopwatch
        running_stopwatch = False
        time_elapsed = 0
        stopwatch_label.config(text="00:00:00")
    
    def update_stopwatch():
        global time_elapsed
        if running_stopwatch:
            time_elapsed += 1
            stopwatch_label.config(text=f"{time_elapsed // 3600:02}:{(time_elapsed % 3600) // 60:02}:{time_elapsed % 60:02}")
            stopwatch_label.after(1000, update_stopwatch)
    
    stopwatch_window = tk.Toplevel(root)
    stopwatch_window.title("Stopwatch")
    stopwatch_window.geometry("300x200")
    
    stopwatch_label = tk.Label(stopwatch_window, text="00:00:00", font=('Arial', 30, 'bold'))
    stopwatch_label.pack(pady=10)
    
    tk.Button(stopwatch_window, text="Start", font=('Arial', 12), command=start_stopwatch).pack(side="left", padx=5)
    tk.Button(stopwatch_window, text="Stop", font=('Arial', 12), command=stop_stopwatch).pack(side="left", padx=5)
    tk.Button(stopwatch_window, text="Reset", font=('Arial', 12), command=reset_stopwatch).pack(side="left", padx=5)

# Timer Functions
def open_timer_window():
    global running_timer, timer_time
    
    def update_timer():
        global running_timer, timer_time
        if running_timer and timer_time[0] > 0:
            timer_time[0] -= 1
            timer_label.config(text=f"{timer_time[0] // 60:02}:{timer_time[0] % 60:02}")
            timer_label.after(1000, update_timer)
        elif running_timer:
            playsound("bell.wav")  # Play sound when timer ends
            timer_label.config(text="Time's up!")
    
    def start_timer():
        global running_timer, timer_time
        running_timer = True
        timer_time[0] = timer_var.get() * 60
        update_timer()
    
    def stop_timer():
        global running_timer
        running_timer = False
    
    def reset_timer():
        global running_timer, timer_time
        running_timer = False
        timer_time[0] = 0
        timer_label.config(text="00:00")
    
    timer_window = tk.Toplevel(root)
    timer_window.title("Timer")
    timer_window.geometry("300x200")
    
    tk.Label(timer_window, text="Set Timer (Minutes):", font=('Arial', 12)).pack(pady=5)
    
    timer_var = tk.IntVar(value=0)
    timer_spinbox = tk.Spinbox(timer_window, from_=0, to=999, wrap=True, textvariable=timer_var, width=5, font=('Arial', 12))
    timer_spinbox.pack(pady=5)
    
    timer_label = tk.Label(timer_window, text="00:00", font=('Arial', 30, 'bold'))
    timer_label.pack(pady=10)
    
    tk.Button(timer_window, text="Start", font=('Arial', 12), command=start_timer).pack(side="left", padx=5)
    tk.Button(timer_window, text="Stop", font=('Arial', 12), command=stop_timer).pack(side="left", padx=5)
    tk.Button(timer_window, text="Reset", font=('Arial', 12), command=reset_timer).pack(side="left", padx=5)

# Initialize Main Window
root = tk.Tk()
root.title("Digital Clock")
root.geometry("500x500")

# Set Background Image
if os.path.exists("clock.png"):
    bg_image = Image.open("clock.png").resize((500, 500), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

clock_label = tk.Label(root, font=('Georgia', 48, 'bold'), fg='black')
clock_label.pack(pady=10)
date_label = tk.Label(root, font=('Arial', 18, 'bold'), fg='#FF4500')
date_label.pack(pady=10)
update_clock()

tk.Button(root, text="Set Alarm", font=('Arial', 12, 'bold'), command=open_alarm_window).pack(pady=5)
tk.Button(root, text="Open Timer", font=('Arial', 12, 'bold'), command=open_timer_window).pack(pady=5)
tk.Button(root, text="Open Stopwatch", font=('Arial', 12, 'bold'), command=open_stopwatch_window).pack(pady=5)

threading.Thread(target=check_alarm, daemon=True).start()
root.mainloop()
