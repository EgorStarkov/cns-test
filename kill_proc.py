import psutil

def kill_all_processes():
    current_proc = psutil.Process()
    for proc in psutil.process_iter():
        if(("chrome" in proc.name() or "python" in proc.name()) and current_proc.pid != proc.pid):
            proc.kill()

kill_all_processes()