import json,requests,hashlib

#接続先情報
CAS_ADDR = 'https://pcc-cas.nemnet-lab.net/auth' #リモートサーバ

#この関数で認証を行います
def Authenticate(username:str,password:str,system_token:str):
    passwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    headers = {"Content-Type": "application/json"}
    data = [{
        "username":username,
        "password":passwd_hash,
        "system_token":system_token
    }]
    jsondata = json.dumps(data)
    res = requests.post(url=CAS_ADDR,data=jsondata,headers=headers)

    result = res.json()
    status_code = res.status_code

    return status_code,result