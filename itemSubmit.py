import dbc,csv

conn = dbc.startConnection()

def itemSubmit():
    csvfile = open("itemList.csv","r",encoding="utf-8")

    file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    print("ファイルをロードしました。")


    flag =0
    for row in file:
        dbc.create_new_item(conn,number=row[0],name=row[1],desc="未設定",resource=row[2],rental='なし',picture='なし')
        flag+=1

    csvfile.close()

def itemDelete():
    csvfile = open("delitemList.csv","r",encoding="utf-8")

    file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    print("ファイルをロードしました。")


    flag =0
    for row in file:
        dbc.delete_item(conn,row[0])
        flag+=1

    csvfile.close()

if __name__ == '__main__':
    itemSubmit()