
history = []
turns = 0

def add(msg):
    history.append(msg)

def bump():
    turns += 1

add("q1")
print(history)
bump()
print(turns)