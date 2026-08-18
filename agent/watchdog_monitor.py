import os
import time
import math
import threading

def calculate_entropy(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            if not data:
                return 0.0
            byte_freq = {}
            for byte in data:
                byte_freq[byte] = byte_freq.get(byte, 0) + 1
            length = len(data)
            entropy = -sum((count / length) * math.log2(count / length) for count in byte_freq.values())
            return entropy
    except Exception:
        return 0.0

class FileWatcher:
    def __init__(self, watch_folder):
        self.watch_folder = watch_folder
        self.running = False
        self.thread = None
        self.file_states = {}
        self.io_events = []
        self.current_entropy = 0.0
        self.current_io_velocity = 0
        self.current_extension_churn = 0
        self.files_scanned = 0
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            
    def _monitor_loop(self):
        if not os.path.exists(self.watch_folder):
            os.makedirs(self.watch_folder, exist_ok=True)
            
        while self.running:
            now = time.time()
            # Clean up old io events (older than 1 second)
            self.io_events = [ts for ts in self.io_events if now - ts <= 1.0]
            
            try:
                current_files = {}
                scanned = 0
                max_entropy = 0.0
                ext_churn = 0
                
                for entry in os.scandir(self.watch_folder):
                    if entry.is_file():
                        scanned += 1
                        stat = entry.stat()
                        mtime = stat.st_mtime
                        size = stat.st_size
                        
                        current_files[entry.name] = {'mtime': mtime, 'size': size}
                        
                        # Check if file is new or modified
                        if entry.name not in self.file_states or \
                           self.file_states[entry.name]['mtime'] != mtime or \
                           self.file_states[entry.name]['size'] != size:
                            
                            self.io_events.append(now)
                            ent = calculate_entropy(entry.path)
                            if ent > max_entropy:
                                max_entropy = ent
                                
                        # Check extension churn
                        if entry.name.endswith('.locked') or entry.name.endswith('.encrypted') or entry.name.endswith('.enc'):
                            if entry.name not in self.file_states:
                                ext_churn += 1
                                
                self.file_states = current_files
                self.files_scanned = scanned
                if max_entropy > 0:
                    self.current_entropy = max_entropy
                self.current_io_velocity = len(self.io_events)
                self.current_extension_churn += ext_churn
                
            except Exception as e:
                pass
                
            time.sleep(0.2)
            
    def get_telemetry(self):
        return {
            'entropy': float(self.current_entropy),
            'io_velocity': int(self.current_io_velocity),
            'extension_churn': int(self.current_extension_churn),
            'files_scanned': int(self.files_scanned),
            'active_process': 'monitor.py',
            'pid': os.getpid()
        }
