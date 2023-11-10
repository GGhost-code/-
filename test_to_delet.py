def make_number_correct(number):
    if number[0] == "8":
        number = "+7" + number[1:]
    else:
         number = "+" + number
    number = number[:2] + " " + number[2:]
    number = number[:6] + " " + number[6:]
    number = number[:10] + "-" + number[10:]
    number = number[:13] + "-" + number[13:]
    return number

print(make_number_correct('89854265560'))