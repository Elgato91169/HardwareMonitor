import tkinter as tk
from tkinter import ttk
import threading

class HardwareMonitorApp:
    def __init__(self, root, core):
        self.root = root
        self.core = core
        
        self.root.title("ElgatoMonitor | Computer System")
        self.root.geometry("540x550")
        self.root.configure(bg="#150B1E")
        self.root.resizable(False, False)
        
        self.setup_styles()
        self.create_widgets()
        
        # Muat data statis di latar belakang agar tidak lag saat booting
        threading.Thread(target=self.load_static_data, daemon=True).start()
        self.update_dynamic_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        bg_color, frame_color, text_color, accent_color = "#150B1E", "#241536", "#EAD8FD", "#8A4FFF"
        
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=frame_color, foreground=text_color, font=("Consolas", 9, "bold"), padding=[12, 6])
        style.map("TNotebook.Tab", background=[("selected", accent_color)])
        style.configure("Card.TFrame", background=frame_color, relief="flat")
        style.configure("Card.TLabel", background=frame_color, foreground=text_color, font=("Consolas", 10))
        style.configure("Header.TLabel", background=frame_color, foreground="#C099FF", font=("Consolas", 10, "bold"))
        style.configure("Footer.TLabel", background=bg_color, foreground="#6D558F", font=("Consolas", 9, "italic"))

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=(10, 0))
        
        self.tab_cpu = ttk.Frame(self.notebook, style="Card.TFrame"); self.notebook.add(self.tab_cpu, text=" CPU & Cache ")
        self.tab_board = ttk.Frame(self.notebook, style="Card.TFrame"); self.notebook.add(self.tab_board, text=" Board & GPU ")
        self.tab_mem = ttk.Frame(self.notebook, style="Card.TFrame"); self.notebook.add(self.tab_mem, text=" Memory ")
        self.tab_io = ttk.Frame(self.notebook, style="Card.TFrame"); self.notebook.add(self.tab_io, text=" OS & I/O ")
        
        # --- TAB 1: CPU & CACHE ---
        ttk.Label(self.tab_cpu, text="[ Processor Unit ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15,5))
        self.l_brand = ttk.Label(self.tab_cpu, style="Card.TLabel", text="Loading..."); self.l_brand.pack(anchor="w", padx=15, pady=2)
        self.l_arch = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_arch.pack(anchor="w", padx=15, pady=2)
        self.l_cores = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_cores.pack(anchor="w", padx=15, pady=2)
        self.l_freq = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_freq.pack(anchor="w", padx=15, pady=2)
        self.l_load = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_load.pack(anchor="w", padx=15, pady=2)
        
        ttk.Label(self.tab_cpu, text="[ Cache Hierarchy ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15,5))
        self.l_l2 = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_l2.pack(anchor="w", padx=15, pady=2)
        self.l_l3 = ttk.Label(self.tab_cpu, style="Card.TLabel"); self.l_l3.pack(anchor="w", padx=15, pady=2)

        # --- TAB 2: BOARD & GPU ---
        ttk.Label(self.tab_board, text="[ System Interconnect ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15,5))
        self.l_board_maker = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_board_maker.pack(anchor="w", padx=15, pady=2)
        self.l_board_model = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_board_model.pack(anchor="w", padx=15, pady=2)
        
        ttk.Label(self.tab_board, text="[ Graphics Processing Unit ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(20,5))
        self.l_gpu_name = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_gpu_name.pack(anchor="w", padx=15, pady=2)
        self.l_gpu_load = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_gpu_load.pack(anchor="w", padx=15, pady=2)
        self.l_gpu_temp = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_gpu_temp.pack(anchor="w", padx=15, pady=2)
        self.l_gpu_mem = ttk.Label(self.tab_board, style="Card.TLabel"); self.l_gpu_mem.pack(anchor="w", padx=15, pady=2)

        # --- TAB 3: MEMORY ---
        ttk.Label(self.tab_mem, text="[ DRAM Specifications ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15,5))
        self.l_ram_type = ttk.Label(self.tab_mem, style="Card.TLabel"); self.l_ram_type.pack(anchor="w", padx=15, pady=2)
        self.l_ram_mts = ttk.Label(self.tab_mem, style="Card.TLabel"); self.l_ram_mts.pack(anchor="w", padx=15, pady=2)
        self.l_ram_clock = ttk.Label(self.tab_mem, style="Card.TLabel"); self.l_ram_clock.pack(anchor="w", padx=15, pady=2)
        self.l_ram_cap = ttk.Label(self.tab_mem, style="Card.TLabel"); self.l_ram_cap.pack(anchor="w", padx=15, pady=2)
        
        ttk.Label(self.tab_mem, text="[ Real-time Utilization ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(20,5))
        self.l_ram_use = ttk.Label(self.tab_mem, style="Card.TLabel"); self.l_ram_use.pack(anchor="w", padx=15, pady=2)

        # --- TAB 4: OS & I/O ---
        ttk.Label(self.tab_io, text="[ Storage & Network (I/O) ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15,5))
        self.l_disk_use = ttk.Label(self.tab_io, style="Card.TLabel"); self.l_disk_use.pack(anchor="w", padx=15, pady=2)
        self.l_net_sent = ttk.Label(self.tab_io, style="Card.TLabel"); self.l_net_sent.pack(anchor="w", padx=15, pady=2)
        self.l_net_recv = ttk.Label(self.tab_io, style="Card.TLabel"); self.l_net_recv.pack(anchor="w", padx=15, pady=2)
        
        ttk.Label(self.tab_io, text="[ OS & Top Processes ]", style="Header.TLabel").pack(anchor="w", padx=15, pady=(20,5))
        self.l_os_name = ttk.Label(self.tab_io, style="Card.TLabel"); self.l_os_name.pack(anchor="w", padx=15, pady=2)
        self.l_top_procs = ttk.Label(self.tab_io, style="Card.TLabel"); self.l_top_procs.pack(anchor="w", padx=15, pady=2)

        ttk.Label(self.root, text="Developed by: Syaroful Haidar S (225443051) | Computer System", style="Footer.TLabel").pack(pady=10)

    def load_static_data(self):
        s = self.core.get_static_info()
        self.root.after(0, self.populate_static_data, s)

    def populate_static_data(self, s):
        self.l_brand.config(text=f"Name       : {s['cpu_brand']}")
        self.l_arch.config(text=f"Arch       : {s['cpu_arch']}")
        self.l_cores.config(text=f"Cores      : {s['cores_phys']} Physical, {s['cores_log']} Threads")
        self.l_l2.config(text=f"L2 Cache   : {s['l2_cache']}")
        self.l_l3.config(text=f"L3 Cache   : {s['l3_cache']}")
        
        self.l_board_maker.config(text=f"Vendor     : {s['board_maker']}")
        self.l_board_model.config(text=f"Model      : {s['board_model']}")
        self.l_gpu_name.config(text=f"Name       : {s['gpu_name']}")
        
        self.l_ram_type.config(text=f"Generation : {s['ram_type']}")
        self.l_ram_cap.config(text=f"Total Cap  : {s['ram_cap']}")
        self.l_ram_mts.config(text=f"Transfer   : {s['ram_mts']}")
        self.l_ram_clock.config(text=f"DRAM Clock : {s['ram_clock']}")
        self.l_os_name.config(text=f"OS Version : {s['os_name']}")

    def update_dynamic_data(self):
        d = self.core.get_dynamic_metrics()
        
        self.l_freq.config(text=f"Core Speed : {d['freq_current']}")
        self.l_load.config(text=f"CPU Load   : {d['cpu_load']}%")
        
        self.l_gpu_load.config(text=f"GPU Load   : {d['gpu_load']}")
        self.l_gpu_temp.config(text=f"Temperature: {d['gpu_temp']}")
        self.l_gpu_mem.config(text=f"VRAM Usage : {d['gpu_mem']}")
        
        self.l_ram_use.config(text=f"RAM Usage  : {d['ram_used']}")
        self.l_disk_use.config(text=f"Drive C:   : {d['disk_used']}")
        self.l_net_sent.config(text=f"Upload Spd : {d['net_sent']}")
        self.l_net_recv.config(text=f"Download   : {d['net_recv']}")
        self.l_top_procs.config(text=f"Top Tasks  : {d['top_procs']}")
        
        self.root.after(1000, self.update_dynamic_data)
