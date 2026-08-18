import os
import subprocess
import psutil

def suspend_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.suspend()
        return True
    except psutil.NoSuchProcess:
        return False
    except (psutil.AccessDenied, AttributeError):
        try:
            # Fallback to taskkill on Windows
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False
    except Exception:
        return False

def block_all_network(exception_ip=None):
    try:
        if os.name == 'nt':
            # Block outbound
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="AutoVault_Emergency"', 'dir=out', 'action=block', 'protocol=any'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Block inbound
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="AutoVault_Emergency"', 'dir=in', 'action=block', 'protocol=any'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        return False
    except Exception:
        return False

def restore_network():
    try:
        if os.name == 'nt':
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name="AutoVault_Emergency"'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        return False
    except Exception:
        return False

def execute_lockdown(pid, cid):
    suspended = suspend_process(pid)
    network_blocked = block_all_network()
    
    return {
        'suspended': suspended,
        'network_blocked': network_blocked,
        'pid': pid
    }
