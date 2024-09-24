ans1 = input("Кормит детей молоком?\n")
ans1 = ans1.lower()
if ans1 == "да" or ans1 == "yes":
    ans2 = input("Ест мясо?\n")
    ans2 = ans2.lower()
    if ans2 == "да" or ans2 == "yes":
        print("Это хищник")
    elif ans2 == "нет" or ans2 == "no":
        print("Не могу понять")
    else:
        print("Вы ввели что-то не то")
elif ans1 == "нет" or ans1 == "no":
    ans2 = input("Есть перья?\n")
    ans2 = ans2.lower()
    if ans2 == "да" or ans2 == "yes":
        print("Это птица")
    elif ans2 == "нет" or ans2 == "no":
        ans3 = input("Дышит жабрами?\n")
        ans3 = ans3.lower()
        if ans3 == "да" or ans3 == "yes":
            print("Это рыба")
        elif ans3 == "нет" or ans3 == "no":
            print("Не могу понять")
        else:
            print("Вы ввели что-то не то")
    else:
        print("Вы ввели что-то не то")
else:
    print("Вы ввели что-то не то")