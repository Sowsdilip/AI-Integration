nums = [1,2,3,4,5,6]
words = ["lc", "bank", "invoice", "swift", "bl"]
text = "ABCDEFGHIJ"

numsquare = [x**2 for x in nums]
upper_case_words = [word.upper() for word in words]
even_nums = []
for x in nums:
    if x%2 == 0:
        print(x)
        even_nums.append(x)
even_num_short = [x for x in nums if x%2 ==0]

lengths = []
for w in words:
    lengths.append(len(w))

length_short = [len(w) for w in words]

three_words = []
for w in words:
    if len(w) > 3:
        three_words.append(w)

step = 2
text_parts = [text[start:start+step] for start in range(0,len(text),step)]

size,overlap = 2,0
chunks = [text[start:start+size] for start in range(0,len(text),size-overlap)]

print(nums)
print(numsquare)
print(even_nums)
print(upper_case_words)
print(lengths)
print(length_short)
print(even_num_short)
print(three_words)
print(text_parts)
print(chunks)