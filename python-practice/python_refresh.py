top = ["a#0", "b#1"]
merged = top
merged += ["c#2"]
#print(top)
merged = merged + ["d#3"]
#print(top, merged)

d = {"A": 0.03, "B": 0.02}
#print(list(d))                          # ['A', 'B']
#print(list(d.items()))                  # [('A', 0.03), ('B', 0.02)]
#print(list(zip(["A", "B"], [0.03, 0.02])))  # same as .items()

CHUNK_TEXT = {
    "lc.txt#0": "An LC is a written undertaking.",
    "lc.txt#1": "The applicant is the buyer.",
    "bg.txt#6": "A guarantee is a secondary obligation.",
}
labels = ["lc.txt#1", "bg.txt#6"]   # pretend these are the fused labels

# --- your line here ---
parts = []
#f"[{label}]\n{doc}" for label,doc in CHUNK_TEXT[label]
for label in labels:
    parts.append(f"[{label}]\n{CHUNK_TEXT[label]}")

#print(parts)

def add_score(scores, label):
    scores[label] = scores.get(label, 0) + 1
    scores = {}
    scores["X"] = 99

label_dict = {"A": 1}
add_score(label_dict, "A")
print(label_dict)

pairs = zip(["A", "B"], [1, 2])
d = dict(pairs)
print(len(d), list(pairs))