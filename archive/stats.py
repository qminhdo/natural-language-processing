def avg(nums):
    return sum(nums)/len(nums)

def l_sqr(nums):
    return [n**2 for n in nums]

def var(X):
    return sum((x - avg(X))**2 for x in X) / len(X)

print(avg([23,32,43,54])==38.0)
print(sum(l_sqr([23,32,43,54]))==6318)
print(var([23,32,43,54])==135.5)