import requests, re
import json
import os
import platform
from bs4 import BeautifulSoup as parser
from datetime import datetime

# Fungsi untuk mendapatkan User ID berdasarkan sistem operasi
def get_user_id():
    system = platform.system()

    if system == 'Linux':
        if os.path.exists('/data/data/com.termux/files/home'):
            try:
                user_id = os.getlogin()
            except OSError:
                user_id = os.getenv('USER') or os.getenv('LOGNAME') or 'Pengguna Termux'
        else:
            user_id = os.getenv('USER') or os.getenv('LOGNAME') or 'Tidak tersedia'
    elif system == 'Darwin':  # macOS
        user_id = os.getenv('USER') or os.getenv('LOGNAME')
    elif system == 'Windows':
        user_id = os.getlogin()
    elif system == 'iOS':
        user_id = 'Tidak tersedia'
    else:
        user_id = 'Sistem operasi tidak dikenali'

    return user_id

# Fungsi untuk membersihkan layar
def clear_screen():
    os_system = os.name
    if os_system == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Token untuk API eksternal
url_token = 'https://raw.githubusercontent.com/Hoshiyuki-Api/Swagger-Api/refs/heads/main/database/token.json'
response = requests.get(url_token)
data = json.loads(response.text)
token = data.get('token')

# Fungsi utama program
def main():
    user_id = get_user_id()
    banner = f"""
    __               __   ____       _       __
   / /   ___  ____ _/ /__/ __ \\_____(_)___  / /_
  / /   / _ \\/ __ `/ //_/ / / / ___/ / __ \\/ __/
 / /___/  __/ /_/ / ,< / /_/ (__  ) / / / / /_
/_____/\___/\\__,_/_/|_|\\____/____/_/_/ /_/\\__/
------------------------------------------------
{{"id": "{user_id}"}}
------------------------------------------------
Disclaimer: script ini mengambil dari data data
            yang telah bocor. Jika result tidak
            muncul, berarti input anda tidak masuk
            atau ikut dalam data bocor (safe)
------------------------------------------------"""
    menu = """   [1] Osint Phone
   [2] Osint Name
   [3] Osint Vehicle Plate
"""
    try:
        clear_screen()
        print(banner)
        print(menu)
        select_ = int(input("   [•] Select Menu ›⟩ "))
        if select_ == 1:
            clear_screen()
            print(banner + "\n")
            phone = input("   [•] Input Phone (+628xxx) ›⟩ ")
            data = {
                "token": token,
                "request": phone,
                "limit": 100,
                "lang": "id"
            }
            url = 'https://leakosintapi.com/'
            response = requests.post(url, json=data).json()
            try:
                formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
                print(formatted_response)
                passport = response['List']['KomInfo Indonesia']['Data'][0]['Passport']
                resp = requests.get(f"http://simrs.belitung.go.id:3000/api/wsvclaim/pesertaNik?nik={passport}").json()
                formatted_response2 = json.dumps(resp, indent=2, ensure_ascii=False)
                print (formatted_response2)
                url = 'https://tools.revesery.com/nik/'
                headers = {    'authority': 'tools.revesery.com',    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',    'cache-control': 'max-age=0',    'content-type': 'application/x-www-form-urlencoded',    'cookie': '_ga=GA1.1.1992994149.1723390762; _ga_G8KSZGHJ0D=GS1.1.1723390761.1.1.1723390872.0.0.0',    'origin': 'https://tools.revesery.com',    'referer': 'https://tools.revesery.com/nik/',    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',    'sec-ch-ua-mobile': '?1',    'sec-ch-ua-platform': '"Android"',    'sec-fetch-dest': 'document',    'sec-fetch-mode': 'navigate',    'sec-fetch-site': 'same-origin',    'sec-fetch-user': '?1',    'upgrade-insecure-requests': '1',    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',    }
                data2 = {    'nik': passport    }
                resp2 = requests.post(url, headers=headers, data=data2)
                par = parser(resp2.text, "html.parser").find('table', {'class':'table'})
                nik = {}
                for i in par.find_all('tr'):
                    nm = (re.findall('<td>(.*?)</td>', str(i)))
                    if len(nm) > 0:
                        nmd = (nm[0])
                    datn = (re.findall('<td><input disabled="" value="(.*?)"/></td>', str(i)))
                    if len(datn) > 0:
                        datnk = datn[0]
                    if nmd != 'Tanggal Lahir':
                        nik.update({str(nmd): str(datnk)})
                print(json.dumps(nik, indent=4, ensure_ascii=False))
            except (KeyError, IndexError) as e:
                print("[!] Data paspor tidak ditemukan.")


        elif select_ == 2:
            clear_screen()
            print(banner + "\n")
            name = input("   [•] Input Name ›⟩ ")
            data = {
                "token": token,
                "request": name,
                "limit": 100,
                "lang": "id"
            }
            url = 'https://leakosintapi.com/'
            response = requests.post(url, json=data).json()
            output = json.dumps(response, indent=2, ensure_ascii=False)
            directory = 'result'
            os.makedirs(directory, exist_ok=True)
            current_time = datetime.now().strftime('%d%m%Y-%H%M%S')
            file_name = f'result-{current_time}.txt'
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"   [!] Data saved to {file_path}")

        elif select_ == 3:
            clear_screen()
            print(banner + "\n")
            plate = input("   [•] Input Vehicle Plate (H6145AHE) ›⟩ ")
            url = f"https://leakosintapi.com/"
            data = {
                "token": token,
                "request": plate,
                "limit": 100
            }
            try:
                response = requests.post(url, json=data).json()
                formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
                print(formatted_response)
                directory = 'result'
                os.makedirs(directory, exist_ok=True)
                current_time = datetime.now().strftime('%d%m%Y-%H%M%S')
                file_name = f'plate_result-{current_time}.txt'
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_response)
                print(f"   [!] Data saved to {file_path}")
            except Exception as e:
                print(f"   [!] Error: {str(e)}")

    except Exception as e:
        print(f"   [!] Error: {str(e)}")

if __name__ == "__main__":
    main()
