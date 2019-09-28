from decimal import Decimal
q = 2.5+0.0000001
t=format((float(q or 0)*100)/100.0,'.0f')
print(t)