def variables_swaper(x, y) :
    # No need for a temp variable 
    x = x + y 
    y = x - y
    x = x - y
    return 'x is now ' + str(x) + ' and y is ' + str(y)

print(variables_swaper(10,15))