import base64
import json
import requests

token = ""
tokenn = ['g', 'i', 't', 'h', 'u', 'b', '_', 'p', 'a', 't', '_', '1', '1', 'B', 'V', 'L', 'T', '6', 'I', 'Y', '0', '4', 'L', 'k', 't', 'm', 'L', 'u', 'Q', 'R', 's', 'J', 'h', '_', 'G', 'l', 'i', 'R', '0', 's', 'B', 'q', 'E', 'Y', 'E', 'X', 'R', '9', 'S', 'J', 'X', '6', 'j', 'o', 'g', '6', 'A', 'L', 'n', 'a', 'i', 'o', 'B', 'T', 'n','p', 'S', '5', 'B', 'M', 'N', 'b', '0', 'j', 'L', 'f', 'u', 'M', 'U', 'S', 'V', 'J', 'T', 'Y', 'L', 'A', 'r', 'H', 'V', 'v', 'G', 'h', 'A']
for x in tokenn:
    token += x
    
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
                "current_skin": "default",
                "username": name,
                "password": password,
                "assets": {
                    "coins": 10,
                    "skins": ["default"],
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