import time
import tkinter as tk

from dvm import DVM

dvm = DVM()
root = tk.Tk()

root.minsize(width=160, height=520)

root.iconbitmap('favicon.ico')

lockable_buttons = []

def connect():
    if dvm.connect():
        show_status("blue", "Connected")
        unlock_buttons()

    else:
        show_status("yellow", "PSU Not Found")




def disconnect():
    dvm.disconnect()
    lock_buttons()
    show_status("grey", "Not Connected")

def turn_on():
    psu.turn_on()
    show_voltage("green", "{:.2f}V".format(psu.voltage))


def turn_off():
    psu.turn_off()
    show_voltage("red", "{:.2f}V".format(psu.voltage))
    root.update()

def set_ohms():
    dvm.set_ohms()

def set_vdc():
    dvm.set_vdc()

def read_value():
    print(dvm.read_voltage())

def get_id():
    print(psu.get_id())


def set_voltage(v):
    psu.set_voltage(v)
    show_voltage("green", "{:.2f}V".format(v))


def reset_to_voltage(v):
    turn_off()
    time.sleep(0.2)
    set_voltage(v)
    time.sleep(0.2)
    turn_on()


def delayed_reset():
    set_voltage(13)
    turn_off()
    show_status("red", "READY")
    root.update()
    time.sleep(1)
    show_status("orange", "STEADY")
    root.update()
    time.sleep(1)
    show_status("green", "GO")
    root.update()
    time.sleep(1)
    turn_on()

    time.sleep(1)
    show_connected_status()


def show_connected_status():
    if dvm.connected:
        show_status("light blue", "Connected")
    else:
        show_status("grey", "Not Connected")


def startup_voltage_test():
    reset_to_voltage(6.8)
    root.update()
    time.sleep(2)
    reset_to_voltage(18.2)
    root.update()
    time.sleep(2)
    reset_to_voltage(13)


def show_voltage(col, t):
    voltage_indicator.config(bg=col, text=t)


def show_status(col, t):
    status_indicator.config(bg=col, text=t)


def lock_buttons():
    connect_button['state'] = 'normal'
    for obj in lockable_buttons:
        obj['state'] = 'disabled'

def unlock_buttons():
    connect_button['state'] = 'disabled'
    for obj in lockable_buttons:
        obj['state'] = 'normal'

def close():
    dvm.disconnect()
    exit()


tk.Label(root, text="CSB PSU Remote").pack(pady=5, padx=5)

voltage_indicator = tk.Label(root, text="0V", bg="red", fg="black", font=("Helvetica", 16))
voltage_indicator.pack(fill=tk.X, pady=5)

status_indicator = tk.Label(root, text="Not Connected", bg="grey", fg="black", font=("Helvetica", 16))
status_indicator.pack(fill=tk.X, pady=5)
tk.Label(root).pack()

connect_button = tk.Button(root, text="Connect", command=lambda: connect())
connect_button.pack(fill=tk.X, padx=5)
disconnect_button = tk.Button(root, text="Disconnect", command=lambda: disconnect())
disconnect_button.pack(fill=tk.X, padx=5)
disconnect_button.configure(state=tk.DISABLED)
tk.Label(root).pack()

on_button = tk.Button(root, text="VDC", command=lambda: set_vdc())
on_button.pack(fill=tk.X, padx=5)
off_button = tk.Button(root, text="OHMS", command=lambda: set_ohms())
off_button.pack(fill=tk.X, padx=5)
tk.Label(root).pack()

delayed_reset_button = tk.Button(root, text="Read Value", command=lambda: read_value())
delayed_reset_button.pack(fill=tk.X, padx=5)
tk.Label(root).pack()

startup_voltage_test_button = tk.Button(root, text="Startup Voltage Test", command=lambda: startup_voltage_test())
startup_voltage_test_button.pack(fill=tk.X, padx=5)
tk.Label(root).pack()

six_eight_button = tk.Button(root, text="6.8 V", command=lambda: reset_to_voltage(6.8))
six_eight_button.pack(fill=tk.X, padx=5)
thirteen_button = tk.Button(root, text="13.0 V", command=lambda: reset_to_voltage(13))
thirteen_button.pack(fill=tk.X, padx=5)
eighteen_two_button = tk.Button(root, text="18.2 V", command=lambda: reset_to_voltage(18.2))
eighteen_two_button.pack(fill=tk.X, padx=5)

tk.Button(root, text="Exit", command=lambda: close()).pack(fill=tk.X, padx=5, pady = 20)

lockable_buttons = [disconnect_button, on_button, off_button, delayed_reset_button, startup_voltage_test_button, six_eight_button, thirteen_button, eighteen_two_button]
lock_buttons()

root.mainloop()
