import dbc,userLoginLib

dbc.create_new_user("naoto","n-saitou@snmochizuki.net",1,"test")
res = dbc.search_userinfo_from_name("naoto")

print(res[0])
print(res)
print(res[7])
print(type(res[0]))

print("トークンテスト")
ck = dbc.cktoken("NoTokena")
print(ck)
