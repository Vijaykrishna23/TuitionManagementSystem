from typing import get_type_hints
import DataBaseManager
from models import Student,FeeDetail
import tkinter as tk
from tkinter import StringVar, ttk,messagebox
from tkcalendar import DateEntry,Calendar

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

        for f in (HomePage, StudentDetailsPage, FeeDetailsPage,  DummyPage):

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

        addFee = ttk.Button(self, text = 'Add Fee',command = lambda: AddFee().mainloop())
        addFee.pack(pady=10,padx=10,side = 'top')

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

        self.currentClassLabel = ttk.Label(container,text = "Class:").grid(row=2,column=0,pady=20,padx=20)
        self.currentClassEntry = ttk.Entry(container)
        self.currentClassEntry.grid(row=2,column=1,pady=20,padx=20)

        self.feesLabel = ttk.Label(container,text = "Fees:").grid(row=3,column=0,pady=20,padx=20)
        self.feesEntry = ttk.Entry(container)
        self.feesEntry.grid(row=3,column=1,pady=20,padx=20)

       
        ttk.Button(self, text = 'ADD',command = self.onClick).pack(pady=20,padx=20)
        
        self.grab_set()
        self.focus()

    def onClick(self):
        newStudent = Student(name=self.nameEntry.get(), date_joined=self.djEntry.get(), current_class=self.currentClassEntry.get(), fees=self.feesEntry.get())

        print(newStudent)

        if newStudent.name == "" or newStudent.current_class == "" or not newStudent.fees.isdigit():
            messagebox.showinfo("Wrong info", "Check your details")
        else:         
            try:
                DataBaseManager.insert_student(newStudent)
                messagebox.showinfo("SUCCESS", "Student Added successfully")
                #newStudent.printDetails()
                self.destroy()
            except:
                #print(e)
                messagebox.showinfo("Failure", "Student can't be added")

class StudentDetailsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        labels = ['ID','Name','Date Joined','Exam','Fees']

        students = DataBaseManager.get_all_students()

     
        for i,label in enumerate(labels):
            ttk.Label(self,text=label).grid(row=0,column=i,padx=10,pady=10)
            
        for i,student in enumerate(students):
            ttk.Label(self,text=i+1).grid(row=i+1,column=0,padx=10,pady=10)
            ttk.Label(self,text=student.get_name()).grid(row=i+1,column=1,padx=10,pady=10)
            ttk.Label(self,text=student.date_joined).grid(row=i+1,column=2,padx=10,pady=10)
            ttk.Label(self,text=student.get_class()).grid(row=i+1,column=3,padx=10,pady=10)
            ttk.Label(self,text=student.get_fees()).grid(row=i+1,column=4,padx=10,pady  =10)
        

        for i,student in enumerate(students):
            btn = ttk.Button(self,text="Delete")
            btn.grid(row=i+1,column=5,padx=10,pady=10)
            btn.bind("<Button-1>",lambda event,arg=student.get_id(): self.deleteStudent(event,arg))
            btn.bind()
            


        ttk.Button(self,text="BACK",command=lambda: controller.show_frame(HomePage)).grid(row=len(labels) + 1,columnspan=5)
                

    def deleteStudent(self,event,arg):
        try:
            DataBaseManager.delete_student(student_id=arg)
            messagebox.showinfo("SUCCESS", "Student Delete successfully")
            self.destroy()
        except Exception as e:
            messagebox.showinfo("Failure", "Student can't be Deleted")
            print(e)

        
class FeeDetailsPage(tk.Frame):


    months = ['Jan','Feb','Mar','Apr','May','Jun',"Jul",
        'Aug','Sep','Oct','Nov','Dec']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # label = ttk.Label(self, text = "Fee Details Page")
        # label.pack(pady=10,padx=10)

        self.monthDropDown = ttk.Combobox(self,width=10)
        self.monthDropDown['values'] = tuple(month for month in self.months)
        self.monthDropDown.current(0)
        self.monthDropDown.grid(row=0,column=0,pady=10)
        
        

        self.yearEntry = ttk.Entry(self,width=10)
        self.yearEntry.insert(0,"2021")
        self.yearEntry.grid(row=0,column=1,pady=10)

        self.submitButton = ttk.Button(self,text="Submit",command= self.listFees)
        self.submitButton.grid(row=0,column=2,pady=10)



    def listFees(self):
        month = self.monthDropDown.get()
        year = self.yearEntry.get()
        feeDetails = DataBaseManager.get_fee_detail_for_month_and_year(month,year)
        i=1
        for fee in feeDetails:
            student = DataBaseManager.get_student(fee.get_student_id())
            ttk.Label(self,text=student.get_name()).grid(row=i,column=0,padx=10,pady=10)
            ttk.Label(self,text=fee.get_date_paid()).grid(row=i,column=1,padx=10,pady=10)
            i+=1

        ttk.Button(self,text="BACK",command=lambda: self.controller.show_frame(HomePage)).grid(row=len(feeDetails) + 1,columnspan=5)




class AddFee(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.resizable(0,0)
        
        container = tk.Frame(self)

        container.pack(side='top')
        
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.studentsList = DataBaseManager.get_all_students()
        self.studentNamesVariable = StringVar(container)
        
        self.studentNamesLabel =ttk.Label(container,text = "Student Name:").grid(row=0,column=0,pady=20,padx=20)
        self.studentNamesDropDown = ttk.Combobox(container,textvariable=self.studentNamesVariable)
        self.studentNamesDropDown['values'] = tuple(st.get_name() for st in self.studentsList)
        self.studentNamesDropDown.bind('<<ComboboxSelected>>', self.onDropDownChanged)    
        self.studentNamesDropDown.grid(row=0,column=1,pady=20,padx=20)

         


        self.dateLabel =ttk.Label(container,text = "Date Paid:").grid(row=1,column=0,pady=20,padx=20)
        self.dateEntry = DateEntry(container, text="Select Date",background='darkblue',foreground='white', date_pattern = 'yyyy/mm/dd')
        self.dateEntry.grid(row=1,column=1,pady=20,padx=20)

        self.amountPaidLabel = ttk.Label(container,text = "Amount Paid:").grid(row=2,column=0,pady=20,padx=20)
        self.amountPaidEntry = ttk.Entry(container)
        self.amountPaidEntry.grid(row=2,column=1,pady=20,padx=20)

        # self.feesLabel = ttk.Label(container,text = "Fees:").grid(row=3,column=0,pady=20,padx=20)
        # self.feesEntry = ttk.Entry(container)
        # self.feesEntry.grid(row=3,column=1,pady=20,padx=20)

       
        ttk.Button(self, text = 'ADD',command = self.onClick).pack(pady=20,padx=20)
        
        self.initializeValues()
        
        self.grab_set()
        self.focus()
    
    def initializeValues(self):
        self.studentNamesDropDown.current(0)
        currentStudent = self.studentsList[0]
        self.amountPaidEntry.delete(0,tk.END)
        self.amountPaidEntry.insert(0,currentStudent.get_fees())

    
    def onDropDownChanged(self , event):
        currentStudentIndex = self.studentNamesDropDown.current()
        currentStudent = self.studentsList[currentStudentIndex]
        self.amountPaidEntry.delete(0,tk.END)
        self.amountPaidEntry.insert(0,currentStudent.get_fees())

    def onClick(self):

        months = ['None','Jan','Feb','Mar','Apr','May','Jun',"Jul",
        'Aug','Sep','Oct','Nov','Dec']

        currentStudentIndex = self.studentNamesDropDown.current()

        currentStudent = self.studentsList[currentStudentIndex]
        
        date_selected = self.dateEntry.get_date()
        month = months[date_selected.month]
        year = date_selected.year
        amount_paid = self.amountPaidEntry.get()

        newFee = FeeDetail(student_id=currentStudent.get_id(),month=month,year=year,date_paid=date_selected,amount_paid=amount_paid)
        print(newFee)

        
        try:
            DataBaseManager.insert_fee(newFee)
            messagebox.showinfo("SUCCESS", "Fees added")
            self.destroy()
        except:
            messagebox.showinfo("Failure", "Fees can't be added")
       



class DummyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        

        label = ttk.Label(self, text = "Dummy")
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = 'Click me',command = lambda: controller.show_frame(HomePage))
        button.pack(pady=10,padx=10)
