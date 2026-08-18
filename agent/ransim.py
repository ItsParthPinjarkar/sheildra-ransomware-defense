import os
import time
import random
import threading
import datetime

def setup_test_vault(folder):
    os.makedirs(folder, exist_ok=True)
    files = [
        "README.txt", "document.docx", "report.pdf",
        "config.json", "keys.txt", "database.sql",
        "backup.zip", "invoice.xlsx", "photo.jpg", "source.py"
    ]
    for filename in files:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w') as f:
            f.write(f"Sample content for {filename}\nGenerated at {datetime.datetime.now().isoformat()}")

def _ransim_thread(folder, speed):
    try:
        for entry in os.scandir(folder):
            if entry.is_file() and not entry.name.endswith('.locked'):
                try:
                    with open(entry.path, 'rb') as f:
                        data = f.read()
                    
                    encrypted = bytearray([b ^ 0x42 for b in data])
                    
                    locked_path = entry.path + '.locked'
                    with open(locked_path, 'wb') as f:
                        f.write(encrypted)
                        
                    os.remove(entry.path)
                    print(f"[Simulator] Encrypted {entry.name}")
                    
                    time.sleep(speed)
                except Exception as e:
                    print(f"[Simulator] Failed to encrypt {entry.name}: {e}")
    except Exception as e:
        print(f"[Simulator] Error: {e}")

def simulate_ransomware(folder, speed=0.15):
    t = threading.Thread(target=_ransim_thread, args=(folder, speed), daemon=True)
    t.start()
    return t

def _normal_activity_thread(folder):
    while True:
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and not f.endswith('.locked')]
            if files:
                target = random.choice(files)
                with open(os.path.join(folder, target), 'a') as f:
                    f.write(f"\nAppended at {datetime.datetime.now().isoformat()}")
        except Exception:
            pass
        time.sleep(random.uniform(1.0, 3.0))

def simulate_normal_activity(folder):
    t = threading.Thread(target=_normal_activity_thread, args=(folder,), daemon=True)
    t.start()
    return t
