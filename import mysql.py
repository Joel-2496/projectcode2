import mysql.connector
import matplotlib.pyplot as pt


mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="2496",
    database="python_video"
)

mycursor = mydb.cursor()


#------------------------SQL commands--------------------------

def insert():
    brand = input("BrandID: ")
    country = input("Country: ")
    year = input("Year: ")
    sales = input("Sales: ")

    sql = "insert into sales (BrandID, Country, Sales_Year, Sales) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (brand, country, year, sales))
    mydb.commit()
    print("Inserted")


def update():
    idd = input("SalesID to update: ")

    sql = "select * from sales where SalesID=%s"
    mycursor.execute(sql, (idd,))

    data = mycursor.fetchone()

    if data:
        print("Record Exists.")

        new_sales = input("New Sales Value: ")

        sql = "update sales set Sales=%s where SalesID=%s"
        mycursor.execute(sql, (new_sales, idd))
        mydb.commit()

        print("Updated")
    else:
        print("Record doesn't exist")


def delete():
    idd = input("SalesID To Delete: ")

    sql = "select * from sales where SalesID=%s"
    mycursor.execute(sql, (idd,))

    data = mycursor.fetchone()

    if data:
        print("Record Exists.")

        sql = "delete from sales where SalesID=%s"
        mycursor.execute(sql, (idd,))
        mydb.commit()

        print("Deleted")
    else:
        print("Record doesn't exist")


def display():
    mycursor.execute("select * from sales")

    for row in mycursor.fetchall():
        print(row)


def search():
    idd = input("SalesID to search: ")

    sql = "select * from sales where SalesID=%s"
    mycursor.execute(sql, (idd,))

    data = mycursor.fetchone()

    if data:
        print(data)
    else:
        print("Record doesnt exist")


#------------------------selection functions--------------------------

def choose_brand():

    while True:
        print("1.Honda")
        print("2.Nissan")
        print("3.Return")

        userinput = input("Enter choice:")

        if userinput == "1":
            return 1, "Honda"

        elif userinput == "2":
            return 2, "Nissan"

        elif userinput == "3":
            return None, None

        else:
            print("Invalid input")


def choose_country():

    while True:
        print("1.Japan")
        print("2.India")
        print("3.USA")
        print("4.Exit")

        userinput = input("Enter choice:")

        if userinput == "1":
            return "Japan"

        elif userinput == "2":
            return "India"

        elif userinput == "3":
            return "USA"

        elif userinput == "4":
            return None

        else:
            print("Invalid Input")


#-------------------------Graph menu----------------------------

def graph():

    while True:

        print("\nANALYSIS OF SALES OF CARS")
        print("1.Company comparison (same country)")
        print("2.Final combined visual")
        print("3.Return to main menu")


        choice2 = input("Enter your choice: ").strip()


        # Company comparison

        if choice2 == "1":

            country = choose_country()

            if country is None:
                continue


            years = []
            honda = []
            nissan = []


            mycursor.execute(f"SELECT DISTINCT Sales_Year FROM sales WHERE Country='{country}' ORDER BY Sales_Year")

            for row in mycursor.fetchall():
                years.append(row[0])


            mycursor.execute(f"SELECT Sales FROM sales WHERE Country='{country}' AND BrandID=1 ORDER BY Sales_Year")

            for row in mycursor.fetchall():
                honda.append(row[0])


            mycursor.execute(f"SELECT Sales FROM sales WHERE Country='{country}' AND BrandID=2 ORDER BY Sales_Year")

            for row in mycursor.fetchall():
                nissan.append(row[0])


            pt.figure(figsize=(8,5))

            pt.plot(years,honda,marker="o",label="Honda")
            pt.plot(years,nissan,marker="o",label="Nissan")

            pt.title(f"Honda vs Nissan in {country}")
            pt.xlabel("Year")
            pt.ylabel("Sales")
            pt.legend()
            pt.grid(True)

            pt.show()


        # Final visual

        elif choice2 == "2":

            countries=["Japan","USA","India"]
            Honda_sales=[]
            Nissan_sales=[]


            for c in countries:

                mycursor.execute(f"SELECT SUM(Sales) FROM sales WHERE BrandID=1 AND Country='{c}'")

                data=mycursor.fetchone()[0]

                Honda_sales.append(data)


            for c in countries:

                mycursor.execute(f"SELECT SUM(Sales) FROM sales WHERE BrandID=2 AND Country='{c}'")

                data = mycursor.fetchone()[0]

                Nissan_sales.append(data)

            x = [0, 1, 2]

            pt.bar(
                [i - 0.2 for i in x],
                Honda_sales,
                width=0.4,
                label="Honda"
            )

            pt.bar(
                [i + 0.2 for i in x],
                Nissan_sales,
                width=0.4,
                label="Nissan"
            )

            pt.xticks(x, countries)

            pt.title("Honda vs Nissan Sales Across Countries")
            pt.xlabel("Country")
            pt.ylabel("Total Sales")

            pt.legend()

            pt.show()



        elif choice2 == "3":
            break


        else:
            print("Invalid choice")



#-------------------------Main menu----------------------------

while True:

    print("\nMain Menu")
    print("1. Display")
    print("2. Insert")
    print("3. Update")
    print("4. Delete")
    print("5. Search")
    print("6. Graphs")
    print("7. Exit")


    choice=input("Enter your choice: ").strip()

    if choice=="1":
        display()
    elif choice=="2":
        insert()

    elif choice=="3":
        update()

    elif choice=="4":
        delete()

    elif choice=="5":
        search()

    elif choice=="6":
        graph()

    elif choice=="7":
        break

    else:
        print("Invalid choice")
