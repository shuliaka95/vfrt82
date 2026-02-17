import json
import time
import subprocess
import logging
import re
import os

def run_daemon():
    # Загрузка конфига с явным указанием кодировки utf-8
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return

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
                # Выполнение ICMP запроса (1 пакет, таймаут 1 сек)
                res = subprocess.run(['ping', '-c', '1', '-W', '1', host], 
                                     capture_output=True, text=True)
                
                if res.returncode == 0:
                    # Извлечение latency с помощью регулярного выражения
                    match = re.search(r'time=([\d.]+)\s*ms', res.stdout)
                    latency = f"{match.group(1)}ms" if match else "unknown"
                    status = "UP"
                else:
                    status, latency = "DOWN", "N/A"
            except Exception as e:
                status, latency = f"ERROR ({type(e).__name__})", "N/A"

            msg = f"Host: {host} | Status: {status} | Latency: {latency}"
            logging.info(msg)
            print(msg) # Вывод в консоль для мониторинга

        # Ожидание 1 минуту перед следующей проверкой
        time.sleep(60)

if __name__ == "__main__":
    run_daemon()
