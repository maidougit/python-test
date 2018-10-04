import redis;

r = redis.Redis(host='127.0.0.1',port=7001,password='geweiredis',db=2)
#u1
r.setbit('u1', 1, 1)
r.setbit('u1', 30,1)

#u2
r.setbit('u2',110,1)
r.setbit('u2',300,1)

#u101
for i in range(3, 365,3):
    r.setbit('u101',i,1)

#u105
for i in range(4, 365, 2):
    r.setbit('u105',i,1)

userList = r.keys('u*')
print (userList)

Au = []
Nau = []
for u in userList:
    loginCount = r.bitcount(u)
    if loginCount > 100:
        Au.append((u, loginCount))
    else:
        Nau.append((u, loginCount))

for l in Au:
    print (l[0] + ' is a Active user.' + str(l[1]))

print ("-------------------------")

for l in Nau:
    print (l[0] + 'is not a Active user.' + str(l[1]))

