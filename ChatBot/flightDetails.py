import datetime
import random
import string

destinations = ["New York", "London", "Paris", "Tokyo", "Berlin", "Dubai", "Toronto", "Los Angeles", "Amsterdam", "Sao Paulo", "Sydney", "Melbourne", "Shanghai"]

def generateBookingNumber():
    # Random string of 6 characters (letters and digits)
    randomStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return f"BK-{randomStr}"

def getFlightDetails(userName):
    # Collecting flight details from the user
    print("TravelBot: Let's book your flight. First, where are you flying from?")
    print("Available cities:", ", ".join(destinations))

    # Get the origin from where the user is travelling from
    origin = None
    while not origin:
        city = input("%s: " % userName).strip().title()
        if city in destinations:
            origin = city
        else:
            print("TravelBot: Please enter a valid city from the list.")

    print("TravelBot: Great, now where are you flying to?")
    print("Available cities:", ", ".join(destinations))

    # Get the destination from where the user is travelling to
    destination = None
    while not destination:
        city = input("%s: " % userName).strip().title()
        if city in destinations:
            if city == origin:
                print("TravelBot: The destination cannot be the same as the origin. Please choose a different destination.")
            else:
                destination = city
        else:
            print("TravelBot: Please enter a valid city from the list.")

    # Check whether the user is on a direct or return flight
    while True:
        print("TravelBot: Is this a direct flight or a return flight? (Please answer 'direct' or 'return')")
        flightType = input("%s: " %userName).lower()
        if flightType in ["direct", "return"]:
            break
        else:
            print("TravelBot: Please answer with 'direct' or 'return'.")

    # Get the departure date and ensure it is a date that is not from the past
    while True:
        print("TravelBot: What is your departure date? (Please use DD-MM-YYYY format)")
        departureDateStr = input("%s: " %userName)
        try:
            departureDate = datetime.datetime.strptime(departureDateStr, "%d-%m-%Y").date()
            if departureDate < datetime.date.today():
                print("TravelBot: Please enter a future date.")
            else:
                break
        except ValueError:
            print("TravelBot: Please enter a valid date in the format DD-MM-YYYY.")

    # Put in a return date if the user desires a return trip and ensure it is from the future and after departure date
    returnDate = None
    if flightType == "return":
        while True:
            print("TravelBot: What is your return date? (Please use DD-MM-YYYY format)")
            return_date_str = input("%s: " %userName)
            try:
                returnDate = datetime.datetime.strptime(return_date_str, "%d-%m-%Y").date()
                if returnDate < datetime.date.today():
                    print("TravelBot: Please enter a future date.")
                elif returnDate <= departureDate:
                    print("TravelBot: Return date must be after the departure date.")
                else:
                    break
            except ValueError:
                print("TravelBot: Please enter a valid date in the format DD-MM-YYYY.")

    # Check the number of passengers travelling
    while True:
        print("TravelBot: How many passengers will be traveling?")
        try:
            passengers = int(input("%s: " %userName))
            if passengers < 1 or passengers > 10:
                print("TravelBot: The number of passengers must be between 1 and 10.")
            else:
                break
        except ValueError:
            print("TravelBot: Please enter a valid number for the number of passengers.")

    return origin, destination, flightType, returnDate, departureDate, passengers

def bookFlight(userName):
    origin, destination, flightType, returnDate, departureDate, passengers = getFlightDetails(userName)

    # Generate a new booking number
    bookingNumber = generateBookingNumber()

    # Save the booking
    saveBooking(bookingNumber, origin, destination, departureDate, passengers)

    return bookingNumber, origin, destination, flightType, returnDate, departureDate, passengers

def saveBooking(bookingNumber, origin, destination, departureDate, passengers):
    # Append to bookings.txt when a user makes a new booking
    with open("bookings.txt", "a") as file:
        file.write(f"{bookingNumber},{origin},{destination},{departureDate},{passengers}\n")

def cancelBooking(bookingNumber):
    # Cancel the bookiong and remove it from the booking.txt file
    with open("bookings.txt", "r") as file:
        bookings = file.readlines()

    with open("bookings.txt", "w") as file:
        cancelled = False
        for booking in bookings:
            if not booking.startswith(bookingNumber):
                file.write(booking)
            else:
                cancelled = True

        return cancelled

def changeBooking(bookingNumber, userName):
    # Finds the user booking that the user wishes to change and update it without changing booking number
    updated = False
    with open("bookings.txt", "r") as file:
        bookings = file.readlines()

    newBookings = []
    for booking in bookings:
        parts = booking.strip().split(',')
        if parts[0] == bookingNumber:
            # Found the booking, now get new details
            origin, destination, departureDate, returnDate, passengers, flightType = getFlightDetails(userName)
            updated_booking = f"{bookingNumber},{origin},{destination},{departureDate},{passengers},{flightType},{returnDate if returnDate else 'N/A'}\n"
            newBookings.append(updated_booking)
            updated = True
        else:
            newBookings.append(booking)

    # Rewrite the updated bookings back to the file
    with open("bookings.txt", "w") as file:
        file.writelines(newBookings)

    return updated