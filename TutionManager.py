import tkinter as tk
from tkinter import ttk,messagebox
from tkcalendar import DateEntry,Calendar
import mysql.connector

'''
TutionManager
Homepage
StudentDetailsPage
FeeDetailsPage
DummyPage
StudentDetails
AddStudent
DataBaseManager
'''



class TutionManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.title(self,"Tution Manager")
        tk.Tk.geometry(self, '400x400')

        
            
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0,weight = 1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (HomePage,StudentDetailsPage, FeeDetailsPage, DummyPage):

            frame = f(self.container, self)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)


        

        
    def show_frame(self, cont):

        #print(self,cont)
        
        frame = self.frames[cont]

        frame = cont(self.container, self)

        frame.grid(row=0, column=0, sticky="nsew")
        
        frame.tkraise()

   



class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        studentDetails = ttk.Button(self, text = 'Student Details',command = lambda: controller.show_frame(StudentDetailsPage))
        studentDetails.pack(pady=10,padx=10)

        feeDetails = ttk.Button(self, text = 'Fee Details',command = lambda: controller.show_frame(FeeDetailsPage))
        feeDetails.pack(pady=10,padx=10)

        addStudent = ttk.Button(self, text = 'Add Student',command = lambda: AddStudent().mainloop())
        addStudent.pack(pady=10,padx=10,side = 'top')

    def getStudent(self):
        studentDetails = AddStudent()
        studentDetails.mainloop()

        newStudent = studentDetails.st
        newStudent.printDetails()

        dbm = DataBaseManager(newStudent)
        dbm.insert()


class StudentDetailsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        labels = ['ID','Name','Date Joined','Exam','Fees']

        dbm = DataBaseManager()

        values = dbm.getValues()

     
        for i,label in enumerate(labels):
            ttk.Label(self,text=label).grid(row=0,column=i,padx=10,pady=10)
            
        for i,val in enumerate(values):
            ttk.Label(self,text=val[0]).grid(row=i+1,column=0,padx=10,pady=10)
            ttk.Label(self,text=val[1]).grid(row=i+1,column=1,padx=10,pady=10)
            ttk.Label(self,text=val[2]).grid(row=i+1,column=2,padx=10,pady=10)
            ttk.Label(self,text=val[3]).grid(row=i+1,column=3,padx=10,pady=10)
            ttk.Label(self,text=val[4]).grid(row=i+1,column=4,padx=10,pady=10)
            
        
        ttk.Button(self,text="BACK",command=lambda: controller.show_frame(HomePage)).grid(row=len(values) + 1,columnspan=5)
                
        #label = ttk.Label(self, text = "Student Details Page")
        #label.pack(pady=10,padx=10)

        #button = ttk.Button(self, text = 'Click me',command = lambda: controller.show_frame(HomePage))
        #button.pack(pady=10,padx=10)

        
        

        

class FeeDetailsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text = "Fee Details Page")
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = 'Click me',command = lambda: controller.show_frame(HomePage))
        button.pack(pady=10,padx=10)

    
class DummyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        

        label = ttk.Label(self, text = "Dummy")
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = 'Click me',command = lambda: controller.show_frame(HomePage))
        button.pack(pady=10,padx=10)
   

class StudentDetails():
    def __init__(self, name, date, exam, fees):
       self.name = name
       self.date = date
       self.exam = exam
       self.fees = fees

    def printDetails(self):
        print(self.name, self.date, self.exam, self.fees)

    def getName(self):
        return self.name

    def getExam(self):
        return self.exam

    def getFees(self):
        return self.fees

    def getDate(self):
       self.date = self.date.replace('/','-')
       return self.date

    


class AddStudent(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        #tk.Tk.geometry(self, '600x600')

        self.resizable(0,0)
        
        container = tk.Frame(self)

        container.pack(side='top')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.nameLabel =ttk.Label(container,text = "Name:").grid(row=0,column=0,pady=20,padx=20)
        self.nameEntry =ttk.Entry(container)
        self.nameEntry.grid(row=0,column=1,pady=20,padx=20)

        
        self.djLabel =ttk.Label(container,text = "Date Joined:").grid(row=1,column=0,pady=20,padx=20)
        self.djEntry = DateEntry(container, text="Select Date",background='darkblue',foreground='white', date_pattern = 'yyyy/mm/dd')
        self.djEntry.grid(row=1,column=1,pady=20,padx=20)

        self.examLabel = ttk.Label(container,text = "Exam:").grid(row=2,column=0,pady=20,padx=20)
        self.examEntry = ttk.Entry(container)
        self.examEntry.grid(row=2,column=1,pady=20,padx=20)

        self.feesLabel = ttk.Label(container,text = "Fees:").grid(row=3,column=0,pady=20,padx=20)
        self.feesEntry = ttk.Entry(container)
        self.feesEntry.grid(row=3,column=1,pady=20,padx=20)

       
        ttk.Button(self, text = 'ADD',command = self.onClick).pack(pady=20,padx=20)
        
        self.grab_set()
        self.focus()

    def onClick(self):
        newStudent = StudentDetails(self.nameEntry.get(), self.djEntry.get(), self.examEntry.get(), self.feesEntry.get())
        dbm = DataBaseManager()

        if newStudent.name == "" or newStudent.exam == "" or not newStudent.fees.isdigit():
            messagebox.showinfo("Wrong info", "Check your details")
        else:         
            try:
                dbm.insert(newStudent)
                messagebox.showinfo("SUCCESS", "Student Added successfully")
                #newStudent.printDetails()
                self.destroy()
            except:
                #print(e)
                messagebox.showinfo("Failure", "Student can't be added")


class DataBaseManager:
    def __init__(self):
       
        self.mydb = mysql.connector.connect(
            host="localhost",   
            user="root",
            passwd="vijay123",  
            database="mydatabase")

        self.mycursor = self.mydb.cursor()
    
    def insert(self,student):
        print(student.getName(), student.getDate(), student.getExam(), student.getFees())
        q_student = "INSERT INTO studentdetails (name,datejoined,exam,fees) VALUES (%s,%s,%s,%s)"
        q_fees = "INSERT INTO (name,datepaid,amountpaid) VALUES (%s,%s,%s)" 


        self.mycursor.execute(q_student,(student.getName(), student.getDate(), student.getExam(), student.getFees()))
        self.mycursor.execute(q_fees,(student.getName(),None,None))
    
        self.mydb.commit()


    def getValues(self):
        q = "SELECT * FROM studentdetails"
        self.mycursor.execute(q)
        
        return self.mycursor.fetchall()





app = TutionManager()
app.mainloop()
        




