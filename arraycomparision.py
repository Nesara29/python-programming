import sys
import time
MAX=3
class studentadt:
    def __init__(self):
        self.student=[None]*MAX
        self.count=0
    def add_student(self,name,rollno,marks):
        if self.count<MAX:
            self.student[self.count]={
                "name":name,
                "rollno":rollno,
                "marks":marks
            }
            self.count+=1
        else:
            print("array is full")
    def display(self):
        for i in range(self.count):
            s=self.student[i]
            print(s["name"],s["rollno"],s["marks"])

s= studentadt()
s.add_student("A",1,"A")
s.add_student("B",2,"B")
s.add_student("C",3,"C")
s.add_student("D",4,"D")
s.add_student("E",5,"E")
s.add_student("F",6,"F")
start_time=time.perf_counter()
s.display()
end_time=time.perf_counter()
print("time taken:",end_time-start_time)
print("space used:",sys.getsizeof(s.student))


