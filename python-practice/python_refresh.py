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
#print(label_dict)

pairs = zip(["A", "B"], [1, 2])
d = dict(pairs)
#print(len(d), list(pairs))

a = int('111',2)
#print(a)

def run_eval(name, rows):
    hits = 0
    for qid in ["lc-01", "lc-02", "lc-03"]:
        hits += 1
    rows.append((name, hits))
    rows = []
    rows.append(("vector", 0))
    return hits

table = []
n = run_eval("hybrid", table)
#print(n, table)

class SemanticCache:
    def __init__(self, entries=None):
        self.entries = entries if entries is not None else []

shared = []
a = SemanticCache(shared)
b = SemanticCache(shared)

a.entries.append("lc-01")
b.entries.append("lc-02")
#print(shared)
#b.entries = []
#b.entries.append("lc-02")

#print(len(a.entries), len(b.entries), len(shared))
#print(shared)

def add_turn(messages, role, content):
    messages.append({"role": role, "content": content})
    messages = []
    messages.append("x")
    return len(messages)

history = [{"role": "user", "content": "What is an LC?"}]
n = add_turn(history, "assistant", "tool_use...")
print(n, len(history))