def temperature_converter() :
    print('Hey, this is The Temperature Converter,\nAll what you need to do is choose the unit of measurement and there you go.')
    quest = input("Let's get started\nChoose your unit either 'C' or 'F'\nEnter its letter :")
    v = int(input('Enter the Value : '))
    final_value = 0
    if quest == 'C' : 
        var = 32 + v * 1.8000
        final_value += var
        return str(v) + ' Celesius is equal to  ' + str(final_value) + ' Fahrenheit.'
    elif quest == 'F' : 
        var = (( 32 - v ) / 1.8000)
        final_value += var
        if v > 32 : 
            return str(v) + ' Fahrenheit is equal to ' + str((final_value)) + ' Celesius.'
        else : 
            return str(v) + ' Fahrenheit is equal to -' + str((final_value)) + ' Celesius.'
    else : 
        return 'See you soon.'

print(temperature_converter())