import requests,json

data_origin = {
    "uname":"s203120",
    "passwd":"Kusopass"
}

data = [data_origin]

jsn = json.dumps(data)

res = requests.post(url='http://localhost:443/login_phase',json=jsn)

print(res.status_code)