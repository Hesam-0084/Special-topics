def calculator(number1 , number2 , operation):
    if operation == '+':
        return number1 + number2
    elif operation == '-':
        return number1 - number2
    elif operation == '*':
        return number1 * number2
    elif operation == '/':
        return number1 / number2
    else :
        return 'invalid operation'
while True :
    number_1 = float(input('Please enter the number 1 : '))
    number_2 = float(input('Please enter the number 2 : '))
    operation_ = input('Please enter the main opration(+ , - * , /) : ')
    
    result = calculator(number_1 , number_2 , operation_)

    print(f'the result is equal to : {result}')

    a = int(input('do you want to countinue ? '))
    if a == 1 :
        continue
    elif a == 0 :
        break
    else :
        print('invalid answer !!!')
        yes=int(input('do you want to continue ?'))
        if yes:
            continue
        else:
            break             
print('GooodBye')



