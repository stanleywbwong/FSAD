# a classic

for i in range(1, 101):
    to_print = ""
    if i % 3 == 0:
        to_print += "Fizz"
    if i % 5 == 0:
        to_print += "Buzz"
    if not len(to_print):
        to_print += str(i)
    print(to_print)
    