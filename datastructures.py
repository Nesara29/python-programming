from operator import truediv

print("primitive data structures")
a=5
b=2.5
c='x'
d=True
print("Integer value:",a)
print("float value:",b)
print("character value:",c)
print("Boolean value:",d)

print("Non primitive data structures")
#list
numbers=[10,20,30,40]
print(numbers)
numbers.append(50)
print(numbers)
#tuple
colors=['red','green','blue']
print("tuple elements are:",colors)
print("second element:",colors[1])
#set
fruits=['apple','banana','orange']
print(fruits)
fruits.remove('orange')
fruits.append("papaya")
print(fruits)
#Dictionary
student={
    "name":"kavana",
    "age":20,
    "course":"python"
}
print(student)
student["age"]=17
print(student["name"])
print(student)
