import json
import time
import subprocess
import logging
import re
import os

def run_daemon():
    # Загрузка конфига
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Настройка логирования
    logging.basicConfig(
        filename=config.get('log_file', 'checker.log'),
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    hosts = config.get('hosts', [])

    while True:
        for host in hosts:
            try:
                # В Void Linux ping находится в /usr/bin/ping
                res = subprocess.run(['ping', '-c', '1', '-W', '1', host], 
                                     capture_output=True, text=True)
                if res.returncode == 0:
                    match = re.search(r'time=([\d.]+)\s*ms', res.stdout)
                    latency = f"{match.group(1)}ms" if match else "unknown"
                    status = "UP"
                else:
                    status, latency = "DOWN", "N/A"
            except Exception:
                status, latency = "ERROR", "N/A"

            msg = f"Host: {host} | Status: {status} | Latency: {latency}"
            logging.info(msg)
            print(msg) # Для отладки в консоли

        time.sleep(60)

if __name__ == "__main__":
    run_daemon()
