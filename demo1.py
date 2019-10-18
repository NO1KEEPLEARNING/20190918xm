list =['a','b','c','d','e']
import random
import string
s = string.ascii_lowercase.upper()
for i in range(120):
    num1 =random.randint(0,9)
    num2 =random.randint(0,9)
    num3 =random.randint(0,9)
    num4 =random.randint(0,9)
    r = random.choice(s)
    print('闽B',num1,num2,num3,num4,r)
