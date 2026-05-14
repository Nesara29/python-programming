class student():
    def __init__(self,name,rollno,marks):
        self.name=name
        self.rollno=rollno
        self.marks=marks
    def display(self):
        print("student details:")
        print("name:",self.name)
        print("Rollno:",self.rollno)
        print("Marks:",self.marks)
    def update(self,new_marks):
        self.marks=new_marks
student=student("kavana",20,90)
student.display()
print("updated marks:")
student.update(95)
student.display()
