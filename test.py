import dbc,userLoginLib


res = dbc.search_userinfo_from_name("齋藤直人")

print(res[0])
print(res[2])
print(type(res[0]))