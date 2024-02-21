import ssl
from nameManagement import switchName, checkUserChangeName
from flightDetails import cancelBooking, changeBooking, bookFlight
from nameManagement import rememberName
from smallTalk import smallTalkResponse
from intentMatching import getIntent
from utilities import checkTimeAndDate, timeBasedGreeting, determineSentiment
# Only need to use once if it hasn't been downloaded
#####################################################
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('universal_tagset')
####################################

namePath = '/Users/seankagan/PycharmProjects/COMP3074 - Human-AI Interaction/ChatBot/dataset/COMP3074-CW1-Dataset-name.csv'
smallTalkPath = '/Users/seankagan/PycharmProjects/COMP3074 - Human-AI Interaction/ChatBot/dataset/COMP3074-CW1-Dataset-small_talk.csv'

def main():
    userName = 'Unknown'
    greeting = timeBasedGreeting()
    print(f"{greeting} mate. Welcome to the Aussie Travel agency. Before we start can I please ask what your name is?")
    print("If you ever need to leave, just say 'exit' and I will move on to my next customer.")
    print('%s: ' %userName, end=" ")
    userInput = input()
    userName = switchName(userInput)
    while True:
        print('%s: ' %userName, end=" ")
        userInput = input()
        if userInput == 'exit':
            print('See you later mate!')
            break
        else:
            # Determine the sentiment of the user input
            sentiment = determineSentiment(userInput)

            # Rename the userName in real-time
            if checkUserChangeName(userInput):
                userName = switchName(userInput)
                print("TravelBot: No worries. Hi %s!" %userName)
                continue

            # Returns the name of the user when prompted to
            nameReply = rememberName(namePath, userInput, threshold=0.9)
            if nameReply != 'UNKNOWN':
                print("TravelBot: I know you. Your name is %s" %userName)
                continue

            # get the user intent for whether they would like to book, change or cancel a flight
            intent = getIntent(userInput, threshold=0.2)

            # Check for any smallTalk and return it in the form of print statements from the csv file
            smallTalk = smallTalkResponse(smallTalkPath, userInput, threshold=0.2)
            if intent == "book_flight":
                # Change the bot response based on user sentiment
                if sentiment == 'positive':
                    print(f"TravelBot: I'm glad you're looking forward to your trip, {userName}! Let's find you the perfect flight.")
                elif sentiment == 'negative':
                    print(f"TravelBot: It seems like you might be having a tough time, {userName}. I'll do my best to make the booking process smooth for you.")
                else:
                    print(f"TravelBot: Alright, {userName}, let's get your flight booked.")

                bookingNumber, origin, destination, flightType, returnDate, departureDate, passengers = bookFlight(userName)

                confirmationMessage = f"TravelBot: Thank you. I have noted that you're traveling from {origin} to {destination} on a {flightType} flight on {departureDate} with {passengers} passengers."
                if returnDate is not None:
                    confirmationMessage += f" You will also be returning on {returnDate}."
                print(confirmationMessage)
                print(f"TravelBot: Your corresponding booking number for the flight is: {bookingNumber}")

            elif intent == "change_flight":
                print("TravelBot: I can assist with changing your flight.")
                bookingNumber = input("TravelBot: Please enter your booking number: ")

                if changeBooking(bookingNumber, userName):
                    print(f"TravelBot: Your flight with booking number {bookingNumber} has been successfully updated.")
                else:
                    print("TravelBot: Sorry, no booking found with that number. Please check and try again.")

            elif intent == "cancel_flight":

                print("TravelBot: I can help you cancel a booking.")
                bookingNumberToCancel = input("Enter booking number to cancel: ")
                if cancelBooking(bookingNumberToCancel):
                    print(f"TravelBot: Booking {bookingNumberToCancel} cancelled successfully.")
                else:
                    print(f"TravelBot: Booking number {bookingNumberToCancel} not found.")

            elif smallTalk != 'UNKNOWN':
                print("TravelBot: " + smallTalk)
            elif 'time' in userInput:
                checkTimeAndDate('time')
                continue
            else:
                print("TravelBot: Apologies I don't understand. Please ask a different question.")

if __name__ == "__main__":
    main()