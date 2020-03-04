# It's for Angela.

import random


def print_practice(a, b, operator, answer):
    print(f"{a} {operator} {b} =", end="")
    g = input()
    if int(g) == answer:
        print("Good!")
    else:
        print("No!!!")
    print()

def make_a_practice(operator, range_max):
    a = random.randint(1, range_max)
    b = random.randint(1, range_max)
    if operator == '+':
        print_practice(a, b, operator, a + b)
    elif operator == '-':
        a, b = max(a, b), min(a, b)
        print_practice(a, b, operator, a - b)
    elif operator == '*':
        print_practice(a, b, operator, a * b)

if __name__ == '__main__':
    type = input("""Please input your choice, 
    1 for 10以内加法
    2 for 10以内减法
    3 for 10以内加减法
    4 for 10以内乘法
    """)
    count = input("How many problems do you want to solve?\n")

    for i in range(int(count)):
        if type == "1":
            operator = "+"
        if type == "2":
            operator = "-"
        if type == "3":
            operator = random.choice("+-")
        make_a_practice(operator, 10)            