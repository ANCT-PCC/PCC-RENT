import dbc,userLoginLib,os,sys

#bc.create_new_user("齋藤 直人","s203120","s203120@edu.asahikawa-nct.ac.jp",0,"test",5,31,"Not Set")
dbc.create_new_user("齋藤 直人(テスト)","naoto","s203120@edu.asahikawa-nct.ac.jp",0,"test",5,31,"Not Set")

dbc.create_new_item("00","1億円","銀行強盗で入手","金庫","借りられません","NoPic")
#dbc.create_new_item(1,"10億円","宝くじで当たった","金庫","借りられません","NoPic")
#dbc.rent_item(1,"10億円","高専を買収","s203120")
result = dbc.rent_item("00","1億円","貧しい人たちへ配布","naoto")
print(result)
#a=input(".../>\n")

#result=dbc.return_item("00")
#print(result)