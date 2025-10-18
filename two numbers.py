l1=[2,3,4]
l2=[5,6,7]
l3=[]
l1.reverse()
l2.reverse()
print(l1)
num1=0
num2=0
for i in l1:
    num1=num1*10+i
print (num1)
for i in l2:
    num2=num2*10+i
print(num2)
total=num1+num2
print (total)
total=str(total)
print(total)
print(type(total))
for i in total:
         print(i)
         l3.append(i)
l3.reverse()
print(l3)
    


