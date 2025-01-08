from pass_manager import *
reg_or_log = 0
if reg_or_log == 0:
    reg_or_log = int(input("Введите 1 для входа и 2 для регистрации. "))
    if reg_or_log == 1:
        starus = log()
        data = exe(starus[1])
        print(f"Ваш username: {data[1]}\nВаша почта: {data[2]}\nВаш возраст: {data[3]}")
    elif reg_or_log == 2:
        re = reg()
        log(re[1],re[2])
        data = exe(re[1])
        print(f"Ваш username: {data[1]}\nВаша почта: {data[2]}\nВаш возраст: {data[3]}")
