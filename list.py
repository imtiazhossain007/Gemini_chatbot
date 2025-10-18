x= [10,13,14,16,17,18,19,21,22,27]
for i in range(len(x)):
    if(x[i]%2==0):
        print(x[i])

letters=["apple","anaconda","dog","cat"]
letters.sort()
print(letters)

x= [10,13,14,16,17,18,19,21,22,27]
sum=0
avg=0
for i in range(len(x)):
    sum+=x[i]
avg=sum/len(x)
print("The Sum:",sum,"\nThe Average:",avg)


x= [10,13,14,16,17,18,10,21,22,17]
cpy_x=[]
for i in x:
    if i not in cpy_x:
        cpy_x.append(i)
print(cpy_x)


x= [10,13,14,16,17,18,10,21,22,17]
y= [2,34,56,7,8,8,9,97,6,4]
x.extend(y)
x.sort()
print(x)

x=int(input("Enter the Number:"))
flg=0
for i in range(2,x//2):
    if(x%i==0):
        flg+=1
if(flg==0):
    print("The number is prime")
else:
    print("The number is not prime")