import tkinter as tk
import win32api
import win32con
import pywintypes

def display_text(text, display_time):
    def close_window():
        label.master.destroy()

    label = tk.Label(text=text, font=('Segoe Script', '80'), fg='black', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+250+250")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()

    # Close the window after the specified display time (in milliseconds)
    label.after(display_time, close_window)

    label.mainloop()

def main():
    display_text("Hello, World!", 5000)

if __name__ == '__main__':
    main()