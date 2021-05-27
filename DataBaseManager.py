from dbconfig import database,database_cursor
from models import Student,FeeDetail
from datetime import datetime

# Get operations
def get_student(student_id):
    query = f"SELECT * FROM student_details WHERE `id`='{student_id }'"
    database_cursor.execute(query)
    row = database_cursor.fetchone()
    student = Student(name=row[1],current_class=row[2],date_joined=row[3],fees=row[4])
    student.set_id(row[0])
    return student

def get_all_students():
    query = f"SELECT * FROM student_details"
    database_cursor.execute(query)
    students = []
    for row in database_cursor.fetchall():
        student = Student(name=row[1],current_class=row[2],date_joined=row[3],fees=row[4])
        student.set_id(row[0])
        students.append(student)
    
    return students

def get_fee_detail_for_student(student_id):
    query = f"SELECT * FROM fee_details WHERE `student_id`='{student_id}'"
    database_cursor.execute(query)
    feedetails = []
    for row in database_cursor.fetchall():
        feedetail = FeeDetail(row[1],row[2],row[3],row[4],row[5])
        feedetail.set_id(row[0])
        feedetails.append(feedetail)
    return feedetails

def get_fee_detail_for_month_and_year(month,year):
    query = f"SELECT * FROM fee_details WHERE `month`='{month}' AND `year`='{year}'"
    database_cursor.execute(query)
    feedetails = []
    for row in database_cursor.fetchall():
        feedetail = FeeDetail(row[1],row[2],row[3],row[4],row[5])
        feedetail.set_id(row[0])
        feedetails.append(feedetail)
    return feedetails
    



# Insertions
def insert_student(student):   
    query = f'''
    INSERT INTO student_details (`name`, `class`, `fees`, `date_joined`) 
    VALUES ('{student.get_name()}','{student.get_class()}','{student.get_fees()}','{student.get_date_joined()}')
    '''
   
    database_cursor.execute(query)
    database.commit()
    student.set_id(database_cursor.lastrowid)
 
    


def insert_fee(fee_detail):
    query = f'''
    INSERT INTO fee_details (`student_id`,`month`,`year`,`amount_paid`,`date_paid`)
    VALUES ('{fee_detail.get_student_id()}','{fee_detail.get_month()}','{fee_detail.get_year()}','{fee_detail.get_amount_paid()}','{fee_detail.get_date_paid()}')
    '''
    database_cursor.execute(query)
    database.commit()
    fee_detail.set_id(database_cursor.lastrowid)


# Update operations
def update_student(student):  
    query = f'''UPDATE student_details  
    SET `name`='{student.get_name()}',
        `class`='{student.get_class()}',
        `fees`='{student.get_fees()}',
        `date_joined`='{student.get_date_joined()}'
    WHERE `id`={student.get_id()}
    ''' 
    database_cursor.execute(query)
    database.commit()

def update_fee(fee_id):
    pass

# Delete operations
def delete_student(student_id): 
    query = f"DELETE FROM student_details WHERE `id`='{student_id}'"  
    database_cursor.execute(query)
    database.commit()

def delete_fee(fee_id):
    query = f"DELETE FROM fee_details WHERE `id`='{fee_id}'"  
    database_cursor.execute(query)
    database.commit()


