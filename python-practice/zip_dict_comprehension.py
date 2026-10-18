ids = ["a1","b1","c1"]
texts = ["LC","Bill of Lading","LG","Invoice"]
pairs = list(zip(ids,texts))

print(pairs)
lookup = dict(zip(ids,texts),strict = True)

for pair in pairs:
    print(pair[0])

for id,text in pairs:
    print(id,text)


print(lookup["a1"])