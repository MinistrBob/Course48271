import string

text = "bobrovsky dmitry"

formatted = string.capwords(text, sep=None)

formatted2 = string.capwords(text, sep="o")

print(formatted)
print(formatted2)
print(text.capitalize())
