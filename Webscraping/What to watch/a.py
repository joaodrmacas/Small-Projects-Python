from re import sub
a = "(ad asd 2=)015"
b = sub("[^0-9]", "", a)
print(b)