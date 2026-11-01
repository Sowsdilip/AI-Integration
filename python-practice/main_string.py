def log_hit(question, seen=None):
    if seen is None:
        seen = []
    seen.append(question)
    return seen
a = log_hit("What is an LC?")
b = log_hit("Who is the beneficiary?")
print(a)
print(a is b)


labels = ["letter_of_credit.txt#0", "ucp600.txt#3"]
for rank, label in enumerate(labels):
    print(rank, label)
for rank, label in enumerate(labels, start=1):
    print(rank, label)