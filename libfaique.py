
def addbook():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    bn=input("plz enter book name:")
    ba=input("plz enter the author name:")
    c=input("plz enter book code:")
    t=int(input("plz enter total books:"))
    s=input("plz enter subject:")
    data=(bn,ba,c,t,s)
    sql="insert into books values(%s,%s,%s,%s,%s);"
    mycur=mydb.cursor()
    mycur.execute(sql,data)
    mydb.commit()

    print("book added successfully")
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()
    
def dbook():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    ac=input("plz enter book code ,which you want to delete:")
    a="delete from books where bcode=%s;"
    data=(ac,)
    mycur=mydb.cursor()
    mycur.execute(a,data)
    mydb.commit()
    print("book deleted successfully")
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()

def dispbook():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    a="select * from books;"
    mycur=mydb.cursor()
    mycur.execute(a)
    myresult=mycur.fetchall()
    
    for i in myresult:
        print("⇸")
        print("BOOKNAME:",i[0])
        print("AUTHOR:",i[1])
        print("BOOK CODE:",i[2])
        print("TOTAL:",i[3])
        print("SUBJECT:",i[4])

    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()


def returnbook():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    n=input("plz enter student name:")
    r=input("plz enter reg no.:")
    co=input("plz enter book code:")
    t=int(input("plz enter  date(yyyy-mm-dd):"))
    q=int(input("plz enter quantity issue:"))
    data=(n,r,co,t,q)
    a="insert into returnbook values(%s,%s,%s,%s,%s);"
    mycur=mydb.cursor()
    mycur.execute(a,data)
    mydb.commit()
    a="delete from issue where regno=%s and bcode=%s and quantityissue=%s;"
    mycur=mydb.cursor()
    mycur.execute(a,(r,co,q,))
    mydb.commit()
    sql="update books set totalbook=totalbook+%s where bcode=%s;"
    mycur.execute(sql,(q,co,))
    mydb.commit()
    
    print("book return successfully by",n)
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()

def reportreturnbooks():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    a="select * from  returnbook ;"
    mycur=mydb.cursor()
    mycur.execute(a)
    myresult=mycur.fetchall()
    for i in myresult:
        print(" ⇸[ [ NAME:",i[0] ,"] ,","[ REGNO:",i[1],"] ,""[ BOOK CODE:",i[2],"] ,""[ RETURN DATE",i[3], "]")
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()
    
def issuebook():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    mycur=mydb.cursor()
    n=input("plz enter student name:")
    r=input("plz enter reg no.:")
    co=input("plz enter book code:")
    t=int(input("plz enter date(yyyy-mm-dd):"))
    q=input("plz enter quantity issue:")
    data=(n,r,co,t,q)
    a="insert into issue values(%s,%s,%s,%s,%s);"
    mycur=mydb.cursor()
    mycur.execute(a,data)
    mydb.commit()
    sql="update books set totalbook=totalbook-%s where bcode=%s;"
    mycur.execute(sql,(q,co,))
    mydb.commit()
    print("book issued successfully to",n)
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()

def reportisssue():
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="faique05",database="lms")
    a="select * from issue;"
    mycur=mydb.cursor()
    mycur.execute(a)
    myresult=mycur.fetchall()
    for i in myresult:
        print(" ⇸ [ [ NAME:",i[0],"] " ",[ REGNO:",i[1],"]"", [ BOOK CODE:",i[2],"]"",[ ISSUE DATE",i[3],"] ]")
    wait=input('𝔭𝔯𝔢𝔰𝔰 𝔢𝔫𝔱𝔢𝔯 𝔱𝔬 𝔠𝔬𝔫𝔱𝔦𝔫𝔲𝔢...')
    main()    
def main():
    print("""
❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄

   ◦•●◉✿1=sᴛᴜᴅᴇɴᴛ ✿◉●•◦        
◦•●◉✿ 2=ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ✿◉●•◦    

❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄
""")
    c=int(input("plz enter the id number"))
    if c==1:
        print("""


     
☘☘ WELCOME  TO THE "MyLIBRO" LIBRARY ☘☘

♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡
♡                              
♡  ❊ 1=To display the books  
♡  ❊ 2=To issue book         
♡  ❊ 3=To return book        
♡  ❊ 4=For the menu          
♡  ❊ 5=To exit               
♡                              
♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡
    """)
        choice=int(input("𝓅𝓁𝑒𝒶𝓈𝑒 𝑒𝓃𝓉𝑒𝓇 𝓉𝒽𝑒 𝓉𝒶𝓈𝓀 𝓃𝓊𝓂𝒷𝑒𝓇..  "))
        
        if choice==1:
            dispbook()
        elif choice==2:
            issuebook()
        elif choice==3:
            returnbook()
        elif choice==4:
            main()
        elif choice==5:
            print("☘☘ 𝓽𝓱𝓪𝓷𝓴𝔂𝓸𝓾  ☘☘")
            exit()
    elif c==2:
        x=int(input("plz enter the pass wd"))
        if x==123:
            print ("welcome")

            print("""
♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡
    ❊ 1=To display the books
    ❊ 2=To view issue table 
    ❊ 3=To view return table
    ❊ 4=To delete the book
    ❊ 5=To add a new book
    ❊ 6=To main menu
♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡
        """)

            y=int(input("𝓅𝓁𝑒𝒶𝓈𝑒 𝑒𝓃𝓉𝑒𝓇 𝓉𝒽𝑒 𝓉𝒶𝓈𝓀 𝓃𝓊𝓂𝒷𝑒𝓇..  "))
            if y==1:
                dispbook()
            elif y==2:
                reportisssue()
            elif y==3:
                reportreturnbooks()
            elif y==4:
                dbook()
            elif y==5:
                addbook()
            elif y==6:
                main()
            else:
                 print("ｅｘｉｔ")
                 exit()
                 
        
        else:
            exit()




main()




                    


def bookup(co):
    import mysql.connector as m
    mydb=m.connect(host="localhost",user="root",passwd="123",database="lms")
    co=input("plz enter book code:")
    t=int(input("plz enter date:"))
    q=input("plz enter quantity issue:")
    a="select total from books where bcode=%s"
    sql="update books set total=%s-q where bcode=%S+co;"
    d=()
    mycur.execute(sql,d)
    mydb.commit()
    wait=input('press enter to continue....')
    main()

