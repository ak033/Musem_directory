import mysql.connector
import time


tables = {

    "ART_OBJECT": ["ID_NO", "ARTIST_NAME", "OBJECT_YEAR", "TITLE", "ORIGIN", "DECRIPTION", "EPOCH"],
    "ARTIST": ["ARTIST_NAME", "DATE_BORN", "DATE_DIED", "COUNTRY_ORIGIN", "EPOCH", "MAIN_STYLE", "DESCRIPTION"],
    "BORROWED": ["BORROWED_ID", "NAME_OF_COLLECTION", "DATE_BORROWED", "DATE_RETURNED"],
    "COLLECTIONS": ["COLLECTION_NAME", "COLLECTION_TYPE", "COLLECTION_DESCRIPTION", "ADDRESS", "PHONE",
                    "CONTACT_PERSON"],
    "EXHIBITIONS": ["EXHIBITION_NAME", "START_DATE", "END_DATE"],
    "OTHER": ["OTHER_ID", "TYPE_ART", "STYLE"],
    "PAINTING": ["PAINTING_ID", "PAINT_TYPE", "DRAW_ON", "STYLE"],
    "PERMANENT_COLLECTIONS": ["PC_ID", "DATE_AQQUIRED", "PC_STATUS", "COST"],
    "SCULPTURE": ["STRUCTURE_ID", "MATERIAL", "HEIGHT", "WEIGHT", "STYLE"],
    "DISPLAYS": ["OBJECT_NUM", "EXHIBITION_NAME"],


}


parent = ["ARTIST", "ARTOBJECT", "COLLECTION", "EXHIBITION"]
illegal = ["ARTISTNAME", "IDNUM", "COLLECTIONNAME", "EXBNNAME", "OBJECTIDNUM"]

def column(select,options):
    x = str(options[select])

    print("")
    print(f"Table Columns for {options[select]}")
    print("-"*70)


    #display columns for table
    query = ("DESCRIBE")
    cur.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \"{options[select]}\"")
    rows = cur.fetchall()
    size = len(rows)
    e = 1;
    for i in range(size):
        for j in range(len(rows[i])):
            formatted = str(rows[i][j])
            formatted = (formatted).ljust(20)
            print("{}. {}".format(e,formatted), end=" ")
            e += 1;
        print()
    print("-"*70)
    print("What columns would you like to display?")
    yn = "N"
    while yn == "N":
        select1 = (input("Enter '*' For All columns, or enter the number of the column name: "))
        if select1 == "*":
            print("You Have Selected all")
        if select1 != "*":
            print(f"You have selected: {tables[x][select1-1]}")
        yn = input("Are you Sure? (Yes = Continue / N = Go back to choose table): ").upper()
        if yn == "N":
            break
        print("-"*35)

    if select1 != "*":
        cur.execute(f"select {tables[x][select1-1]} from {options[select]}")
    else:
        cur.execute(f"select * from {options[select]}")
    col_names = cur.column_names #column names
    search_result = cur.fetchall() #what ever user wants to see
    print("Search found ", len(search_result), " Entries: \n")
    header_size = len(col_names) #size of how many column names
    for i in range(header_size):
        print("{:<50s}".format(col_names[i]), end='')
    print()
    print(15 * header_size * '-')
    for row in search_result:
        for val in row:
            print("{:<50s}".format(str(val)), end='')
        print()
    print()

def admin():
    print("\n" * 10)
    print("-" * 70)
    print("Hello Admin!")
    print("-" * 70)
    print("Options")
    print('1. Enter an SQL command')
    print('2. Run the SQL Script')
    selections = (input('Enter your option: '))

    if selections == '1':
        print("\n\n")
        yn = "N"
        while yn == "N":
            print("Selected: Enter an SQL Command,")
            yn = input("would you like to continue? (Y/N): ").upper()
        sqlCommand = str(input('Enter your SQL Command: '))
        cur.execute(sqlCommand)
        rows = cur.fetchall()
        size = len(rows)
        for i in rows:
            print(i)

    elif selections == '2':
        file_name = input('Please enter the filename: ')
        fd = open(file_name, 'r')
        filesql = fd.read()
        fd.close()
        sqlcommands = filesql.split(';')
        for command in sqlcommands:
            # if command == ';':
            #     print("breaks")
            #     break
            try:
                cur.execute(command)
                print(f'{command}   Successful')
                print("-" * 70)
                time.sleep(0.2)
            except:
                print("Commands Successful")
                break
        cxn.commit()



def employee():
    print("\n" * 5)
    print("Options")
    print("_" * 60)
    print('1. Lookup info in database')
    print('2. Insert')
    print('3. Update')
    print('4. Delete')
    choice = int(input('Input option you would like to do: '))
    table_choice = ''
    print("-" * 50)

    cur.execute("show tables")
    rows = cur.fetchall()
    size = len(rows)

    e = 1
    for i in range(size):
        for j in range(len(rows[i])):
            formatted = str(rows[i][j])
            formatted = (formatted).ljust(20)
            print("{}. {}".format(e, formatted), end=" ")
            e += 1
        print()
    print("-" * 70)

    # choice 1
    if choice == 1:
        cond_state = ""
        sql = ""

        select_table = str(input('Type the name of the table that you would like to display: ').upper())
        tables_len = len(tables[(select_table)])
        attributes_count = input(f'Input the number of attributes to display. Enter * for all attributes). Max attributes =  {tables_len}: ')
        if (attributes_count == '*'):
            choose_attribute.append('*')
            attributes_count = 1
        else:
            attributes_count = int(attributes_count)
        choose_attribute = []

        cur.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \"{select_table}\"")
        rows = cur.fetchall()
        size = len(rows)
        e = 1
        for i in range(size):
            for j in range(len(rows[i])):
                formatted = str(rows[i][j])
                formatted = (formatted).ljust(20)
                print("{}. {}".format(e, formatted), end=" ")
                e += 1
            print()
        print("-" * 70)

        choose_attribute.append(input(
            "Please enter the attribute you want to be selected from the table. Enter '*' for all attributes): ").upper())
        q = input("Would you like to add conditions?(Y/N): ")
        if q != "N":
            cond_int = int(input('Please input the amount of conditions for the query: '))
        else:
            cond_int = 0
        if cond_int > 0:
            cond_statement = input(
                "Please Enter the condition you wish to add: ").upper()
            for i in range(cond_int - 1):
                union_join = input('AND or OR: ').upper()
                condition = input(
                    "Please input your condition: ").upper()
                cond_statement = f"{cond_statement} {union_join} {condition}"

        distinct_vals = input('Do you only want to add distinct values? (Y/N): ').upper()
        if distinct_vals == 'Y':
            sql = "SELECT"
        else:
            sql = "SELECT DISTINCT"

        for i in range(attributes_count):
            if i < attributes_count - 1:
                sql = f"{sql} {choose_attribute[i]},"
            else:
                sql = f"{sql} {choose_attribute[i]}"
        if cond_int > 0:
            sql = f"{sql} FROM {table_choice} WHERE {cond_statement}"
        else:
            sql = f"{sql} FROM {table_choice}"

        cur.execute(sql)
        rows = cur.fetchall()
        size = len(rows)
        for i in range(size):
            for j in range(len(rows[i])):
                formatted = str(rows[i][j])
                formatted = (formatted).ljust(20)
                print(formatted, end=" ")
            print()

#CHOICE 2 HERE NAINA
    if choice == 2:
        select_table = input('Choose table you would like to insert into: ')
        while select_table not in list(tables.keys()):
            select_table = input('Input table you would like to insert into: ')

        print('1. Insert using file')
        print('2. Insert through prompts')
        choices = int(input('Input option you would like to do: '))

        if choices == 1:
            file_name = input('Please input filename: ')
            fd = open(file_name, 'r')
            sql_file = fd.read()
            fd.close()
            sql_commands = sql_file.splitlines()
            for command in sql_commands:
                cur.execute(command)
                print(f'{command}   Row Inserted')

        if choices == 2:
            loops = int(input('Input number of items you would like to insert: '))
            for i in range(loops):
                inp = []
                sql = "INSERT INTO " + select_table + " ("
                for i in range(len(tables[select_table])):
                    inp.append(input(f"Please enter {tables[select_table][i]}: "))
                    if i <= len(tables[select_table]) - 2:
                        sql = sql + tables[select_table][i] + ", "
                sql = sql + tables[select_table][len(tables[select_table]) - 1]
                sql = sql + ") VALUES ("
                for i in range(len(tables[select_table]) - 1):
                    sql = sql + "%s, "
                sql = sql + "%s)"
                NEWDATA = tuple(inp)
                cur.execute(sql, DATA)
                print('New Row has been Inserted!')


    if choice == 3:
        select_table = str(input('Type the name of the table that you would like to display: ').upper())
        cur.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \"{select_table}\"")
        rows = cur.fetchall()
        size = len(rows)
        e = 1;
        for i in range(size):
            for j in range(len(rows[i])):
                formatted = str(rows[i][j])
                formatted = (formatted).ljust(20)
                print("{}. {}".format(e, formatted), end=" ")
                e += 1;
            print()
        print("-" * 70)
        dict = []
        sel_update = input('Please Enter the Column you would like to update: ').upper()
        if ((sel_update in illegal) or (sel_update not in tables[select_table])):
            print("INVALID ATTRIBUTE!")
            return

        key_val = int(input('How many Primary Keys in this Attribute?: '))
        key = []

        for e in range(key_val):
            key.append(input('Please Enter the Name of the chosen Primary key: ').upper())
        dict.append(input(f'Please Enter your updated value for: {sel_update}: '))


        sql = "UPDATE " + select_table + " SET " + sel_update + " = %s WHERE "
        keylen = len(key)

        for k in range(keylen):
            dict.append(input(f'Please Enter the value of: {key[k]}: '))
            if k < len(key) - 1:
                sql = sql + key[k] + " = %s AND "
            else:
                sql = sql + key[k] + " = %s"
        value = tuple(dict)
        cur.execute(sql, value)
        print('Item Successfully Updated!')


  #Choice 4
    if choice == 4:
        select_table = str(input("Please input the table you would like to delete from: ")).upper()
        if select_table in parent:
            print('This table contains parent key, cannot delete from this table')
            return

        key_value = int(input('Please input the number of attributes to search: '))
        search = []
        value = []

        for i in range(key_val):
            choose_attribute = input('Please enter name of search attribute: ').upper()
            attribute_value = input('Please enter the value to be deleted: ').upper()
            search.append(choose_attribute)
            value.append(attribute_value)

        sql = "DELETE FROM " + select_table + " WHERE "
        for i in range(key_value):
            if i < key_value - 1:
                sql = f"{sql}{search[i]} = '{value[i]}' AND"
            else:
                sql = f"{sql} {search[i]} = '{value[i]}'"

        cur.execute(sql)
        print('Row has been deleted')

    cxn.commit()

def guest():
    options = {1:"Art_Object", 2:"Artist",3:"Borrowed",4:"Collections",5:"Exhibitions",
               6:"Other", 7:"Painting", 8:"Permanent_Collections",9:"Sculpture"}
    #this block fetches the table names for the user to select
    print("\n"*5)
    print("Guest Menu")
    print("-"*70)
    print("Options")
    print("-------")
    cur.execute("show tables")
    rows = cur.fetchall()
    size = len(rows)
    e = 1;
    for i in range(size):
        for j in range(len(rows[i])):
            formatted = str(rows[i][j])
            formatted = (formatted).ljust(20)
            print("{}. {}".format(e,formatted), end=" ")
            e += 1;
        print()
    print("-"*70)
    #gets user input, if they do want to change mind, they can
    yn = "N"
    while yn == "N":
        select = int(input("Select an option: "))
        print("You have selected: {}".format(options[select]))
        yn = input("Are you Sure? (Y/N): ").upper()
        print("-"*35)
    column(select,options)

if __name__ == '__main__':
    print("="*70)
    print('Welcome to the Museum database, please login!')
    # users = ['admin', 'guest', 'employee', 'root']
    print("In order to proceed, please select your role from the list below")
    print("-"*70)
    print("|- 1. Admin\n|- 2. Employee\n|- 3. Guest")
    print("="*70)
    selection = input("Enter choice: ")

    connection_db = "MUSEUM"
    if selection in ['1', '2']:
        print("|"*2)
        user_name = input("Enter Username: ")
        pass_word = input("Enter Password: ")
    else:
        user_name = "guest"
        pass_word = None

    cxn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database=connection_db,
        user=user_name,
        password=pass_word
    )

    cur = cxn.cursor()
    if selection == '1':
        admin()
    if selection == '2':
        employee()
    if selection == '3':
        guest()

    while True:
        choice = input('Do you want to continue? (Y/N): ').upper()
        if selection == '1':
            admin()
        if selection == '2':
            employee()
        if selection == '3':
            guest()
        else:
            break

    cxn.close()
