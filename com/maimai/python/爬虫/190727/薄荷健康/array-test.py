from array import array

result = [x + 1 for x in range(1)]

print(result)



a=[[1, 2], [3, 4], [5, 6]]

b = tuple(tuple([y for y in x]) for x in a)

print(b)