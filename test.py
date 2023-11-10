import dbc,json


res = dbc.get_all_users()


for i in range(len(res)):
    print("\n")
    for j in range(len(res[0])):
        print(res[i][j])