import time
import sys
class student():
    def __init__(self,name,rollno,marks):
        self.name=name
        self.rollno=rollno
        self.marks=marks
    def display(self):
        print("Name:",self.name)
        print("Roll no:",self.rollno)
        print("Marks:",self.marks)
    def update(self,new_marks):
        self.marks=new_marks
start_time=time.perf_counter()
student=student("kavana",20,92)
student.display()
student.update(97)
student.display()
end_time=time.perf_counter()
space_used=sys.getsizeof(student)
print("time taken:",end_time-start_time)
print("space used:",space_used)