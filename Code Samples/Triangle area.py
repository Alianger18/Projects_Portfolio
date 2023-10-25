def triangle_area(base, height) : 
    b = base
    h = height
    return (b * h) / 2

quest = input("Hey, do you want to calculate the triangle area ? What's Your answer : ")

while quest != 'n' : 
    try :  
        base = int(input("Enter the base specification : "))
        height = int(input("Enter the height specification : "))
    except : 
        TypeError
    print(triangle_area(base, height))
    tr_again = input("Do you have any other triangle to calculate its area ? Press 'Y' to try again or 'N' to quit : ")
    if tr_again == 'y' or tr_again == 'Y' : 
        continue
    else : 
        break
