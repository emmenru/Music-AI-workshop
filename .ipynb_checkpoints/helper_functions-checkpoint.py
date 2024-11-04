def get_user_input():
    global user_number
    while True:
        try:
            user_number = float(input("Please enter a number: "))
            break
        except ValueError:
            print("That's not a valid number. Please try again.")

