from mysql.connector import connect

database = connect(
            host="localhost",   
            user="root",
            passwd="",  
            database="tuition_management_system")

database_cursor = database.cursor()