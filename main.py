import subprocess
import time
import psutil, os

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def start_process(script_name):
    """Start the given script using a new Command Prompt window."""
    try:
        # Using start to open a new Command Prompt window and run the script
        subprocess.Popen(['start', 'cmd', '/k', f'python {script_name}'], shell=True)
    except Exception as e:
        print(f"Error starting {script_name}: {e}")

def main():
    os.system('cls')
    if not is_process_running('server.py'):
        print("Starting server.py...")
        start_process('server.py')
        time.sleep(2)  # Give server.py some time to start
    else:
        print("server.py is already running.")

    print("Starting client.py...")
    start_process('client.py')

if __name__ == "__main__":
    main()
