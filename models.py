class Student:
    def __init__(self,name,current_class,fees,date_joined):
        self.name = name
        self.current_class = current_class
        self.fees = fees
        self.date_joined = date_joined

    def set_id(self,id):
        self.id = id

    def __str__(self):
       return f'''
        Name: {self.name}
        Class: {self.current_class}
        Fees : {self.fees}
        Date Joined: {self.date_joined}
        '''

    def get_name(self):
        return self.name
    
    def get_class(self):
        return self.current_class
    
    def get_fees(self):
        return self.fees
    
    def get_date_joined(self):
        self.date_joined = self.date_joined.replace('/','-')
        return self.date_joined

    def get_id(self):
        return self.id

class FeeDetail:
    def __init__(self, student_id, month, year, date_paid, amount_paid):
        self.student_id = student_id
        self.month = month
        self.year = year
        self.date_paid = date_paid
        self.amount_paid = amount_paid

    def set_id(self,id):
        self.id = id

    def __str__(self):
       return f'''
        Student: {self.student_id}
        Month-Year: {self.month}-{self.year}
        Fees Paid : {self.amount_paid}
        Date Paid: {self.date_paid}
        '''

    def get_student_id(self):
        return self.student_id
    
    def get_month(self):
        return self.month

    def get_year(self):
        return self.year
    
    def get_amount_paid(self):
        return self.amount_paid
    
    def get_date_paid(self):
        return self.date_paid

    def get_id(self):
        return self.id
    