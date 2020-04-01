import random
import time

b = 0
s1 = time.time()
for i in range(100000):
    a = random.uniform(10, 20)
    print(a)
    b += a
s2 = time.time()

print(s2 - s1)
print(b / 100000)
