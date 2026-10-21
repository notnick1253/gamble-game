import base64
import json
import requests


headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

def check_acc(url):
    check = requests.get(url, headers=headers)
    
    if check.status_code == 404:
        return True
    elif check.status_code == 200:
        print("Der Account existiert bereits.")
        return False
    else:
        print(f"Prüfung fehlgeschlagen: {check.status_code}")
        print(check.text)
        return False

def create_acc(name, password):
    url = f"https://api.github.com/repos/notnick1253/acc_server/contents/accounts/{name}.json"
    
    if check_acc(url):
    
        data = {
            "user": {
                "playing": False,
                "username": name,
                "password": password,
                "assets": {
                    "coins": 10,
                    "skins": [],
                    "playtime/h": 0
                }
            }
        }

        content = base64.b64encode(
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("utf-8")


        response = requests.put(
            url,
            headers=headers,
            json={
                "message": f"Account für {name} erstellen",
                "content": content,
            },
        )

username = input("username: ")
password = input("password: ")

create_acc(username, password)