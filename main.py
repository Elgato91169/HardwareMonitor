import tkinter as tk
import multiprocessing
from core import CoreMonitor
from ui import HardwareMonitorApp

def main():
    multiprocessing.freeze_support()
    root = tk.Tk()
    core = CoreMonitor()
    app = HardwareMonitorApp(root, core)
    root.mainloop()

if __name__ == "__main__":
    main()
    