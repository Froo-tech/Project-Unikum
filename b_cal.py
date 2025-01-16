def b_cal(ball, max_b):
    res = (100 * ball) / max_b
    if res >= 80:
        print(f'5:{res:.2f}')
        print("Баллов до следующей оценки: максимальная оценка")
    elif res >= 66:
        print(f'4:{res:.2f}')
        balls_to_5 = (87 * max_b) / 100 - ball
        print(f"Баллов до 5: {balls_to_5:.2f}")
    elif res >= 42:
        print(f'3:{res:.2f}')
        balls_to_4 = (66 * max_b) / 100 - ball
        print(f"Баллов до 4: {balls_to_4:.2f}")
    elif res >= 20:
        print(f'2:{res:.2f}')
        balls_to_3 = (42 * max_b) / 100 - ball
        print(f"Баллов до 3: {balls_to_3:.2f}")
    else:
        print(f'1:{res:.2f}')
        balls_to_2 = (20*max_b) / 100 - ball
        print(f"Баллов до 2: {balls_to_2:.2f}")


b_cal(220.33, 274.88)
