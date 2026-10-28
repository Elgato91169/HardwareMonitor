import psutil
import cpuinfo
import platform
import wmi
import pythoncom
import time
from datetime import datetime

try:
    import pynvml
    pynvml.nvmlInit()
    nvml_available = True
except Exception:
    nvml_available = False

class CoreMonitor:
    def __init__(self):
        if platform.system() == 'Windows':
            pythoncom.CoInitialize()
            
        self.w = wmi.WMI()
        self.os_info = platform.uname()
        self.is_windows = platform.system() == 'Windows'
        
        # Inisialisasi variabel untuk kalkulasi kecepatan I/O Real-time
        self.last_net = psutil.net_io_counters()
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()

    def get_static_info(self):
        info = cpuinfo.get_cpu_info()
        
        # Ekstraksi Cache (Menghindari WMI yang menyesatkan, fokus ke cpuinfo)
        l2_size = info.get('l2_cache_size', 'N/A')
        l3_size = info.get('l3_cache_size', 'N/A')
        l2_assoc = info.get('l2_cache_associativity', 'N/A')

        board_maker, board_model = "N/A", "N/A"
        try:
            board = self.w.Win32_BaseBoard()[0]
            board_maker = board.Manufacturer
            board_model = board.Product
        except Exception:
            pass

        # Bab 6: RAM Transfer Rate (MT/s) vs DRAM Clock (MHz)
        ram_mts, ram_clock, ram_type, ram_cap = "N/A", "N/A", "Unknown", 0
        try:
            mem_modules = self.w.Win32_PhysicalMemory()
            if mem_modules:
                ram_mts = mem_modules[0].Speed
                ram_clock = int(ram_mts) // 2 if ram_mts else "N/A"
                ram_type = "DDR5" if ram_mts and int(ram_mts) >= 4800 else "DDR4/Older"
                ram_cap = sum(int(m.Capacity) for m in mem_modules) // (1024**3)
        except Exception:
            pass

        # Fallback GPU yang jujur
        gpu_name = "Integrated / Basic Display"
        if nvml_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                name_raw = pynvml.nvmlDeviceGetName(handle)
                gpu_name = name_raw.decode('utf-8') if isinstance(name_raw, bytes) else name_raw
            except Exception:
                pass
        else:
            try:
                gpus = self.w.Win32_VideoController()
                if gpus: gpu_name = gpus[0].Name
            except Exception:
                pass

        return {
            "cpu_brand": info.get('brand_raw', 'Unknown'),
            "cpu_arch": f"{info.get('arch_string_raw', '')} ({info.get('bits', '')} bit)",
            "cores_phys": psutil.cpu_count(logical=False),
            "cores_log": psutil.cpu_count(logical=True),
            "l2_cache": f"{l2_size} (Ways: {l2_assoc})",
            "l3_cache": l3_size,
            "board_maker": board_maker,
            "board_model": board_model,
            "ram_clock": f"{ram_clock} MHz",
            "ram_mts": f"{ram_mts} MT/s",
            "ram_type": ram_type,
            "ram_cap": f"{ram_cap} GB",
            "gpu_name": gpu_name,
            "os_name": f"{self.os_info.system} {self.os_info.release}",
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_dynamic_metrics(self):
        # Karena kita membuang WMI suhu yang lambat, psutil murni berjalan <0.05 detik
        # Tidak akan membekukan (freeze) thread utama UI.
        current_time = time.time()
        time_delta = current_time - self.last_time

        freq = psutil.cpu_freq()
        mem = psutil.virtual_memory()
        
        # Kalkulasi Kecepatan Jaringan Aktual (I/O Bab 8)
        current_net = psutil.net_io_counters()
        net_sent_speed = (current_net.bytes_sent - self.last_net.bytes_sent) / time_delta / 1024
        net_recv_speed = (current_net.bytes_recv - self.last_net.bytes_recv) / time_delta / 1024
        
        self.last_net = current_net
        self.last_time = current_time

        gpu_load, gpu_temp, gpu_mem = "N/A", "N/A", "N/A"
        if nvml_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                try:
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_load = f"{util.gpu}%"
                except Exception:
                    gpu_load = "0% (Sleep/Idle)"
                try:
                    temp = pynvml.nvmlDeviceGetTemperature(handle, 0)
                    gpu_temp = f"{temp}°C"
                except Exception: pass
                try:
                    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    gpu_mem = f"{mem_info.used // (1024**2)} MB / {mem_info.total // (1024**2)} MB"
                except Exception: pass
            except Exception:
                pass

        # Ekstraksi Proses Teratas (Bab 9 - OS & Process Management)
        top_procs = []
        try:
            for p in sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:3]:
                top_procs.append(f"{p.info['name']} ({p.info['cpu_percent']}%)")
        except Exception:
            pass

        disk_usage = psutil.disk_usage('C:\\' if self.is_windows else '/')

        return {
            "cpu_load": psutil.cpu_percent(interval=None),
            "freq_current": f"{freq.current:.1f} MHz" if freq else "N/A",
            "gpu_load": gpu_load,
            "gpu_temp": gpu_temp,
            "gpu_mem": gpu_mem,
            "ram_used": f"{mem.used / (1024**3):.2f} GB ({mem.percent}%)",
            "disk_used": f"{disk_usage.used / (1024**3):.2f} GB ({disk_usage.percent}%)",
            "net_sent": f"{net_sent_speed:.1f} KB/s",
            "net_recv": f"{net_recv_speed:.1f} KB/s",
            "top_procs": " | ".join(top_procs) if top_procs else "N/A"
        }
        