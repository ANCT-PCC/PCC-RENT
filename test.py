import dbc,userLoginLib

dbc.create_new_user("s203120","s203120@edu.asahikawa-nct.ac.jp",0,"test")
res = dbc.search_userinfo_from_name("s203120")
