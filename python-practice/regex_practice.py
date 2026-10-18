import re
text = "   \n   A para.\n\n\nB para.\n  \nC para."
print(text.split("\n\n"))
print(text.splitlines())
print(re.split(r"\n\s*\n", text))

cleanedText = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
print(cleanedText)

print(sorted([("a", 0.3), ("b", 0.9)], key=lambda x: x[1], reverse=True)[1])