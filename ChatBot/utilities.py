import datetime as dt
import string

import nltk
import numpy as np
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocessText(text):
    # Tokenize, lemmatize, and remove stop words and punctuation
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if
              word not in set(stopwords.words('english')) and word not in string.punctuation]
    return " ".join(tokens)

def checkTimeAndDate(str):
    # Return the current date and time
    date = dt.datetime.now()
    if str == 'time':
        hour = date.strftime("%H")
        minute = date.strftime("%M")
        second = date.strftime("%S")
        year = date.year
        month = date.month
        day = date.day
        print("TravelBot: The current time is %s:%s:%s and date is %s/%s/%s." %(hour, minute, second, day, month, year))

def timeBasedGreeting():
    # Change the greeting based on the time of day
    current_hour = dt.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

sentimentCorpus = [
    "happy", "good", "great", "fantastic", "positive", "thrilled"
    "bad", "sad", "terrible", "negative", "upset"
]

# Create the vectorizer and fit it to the sentimentCorpus
vectorizer = TfidfVectorizer()
tfidfMatrix = vectorizer.fit_transform(sentimentCorpus)

def determineSentiment(userInput):
    # Vectorize the user input
    userInputVector = vectorizer.transform([userInput.lower()])

    # Compute cosine similarity between the user input and the corpus
    similarityScores = cosine_similarity(userInputVector, tfidfMatrix)

    # Determine if input is closer to positive or negative sentiment
    positiveScore = np.mean(similarityScores[0][:5])  # Scores corresponding to positive sentiments
    negativeScore = np.mean(similarityScores[0][5:])  # Scores corresponding to negative sentiments

    # Returns current user sentiment
    if positiveScore > negativeScore:
        return 'positive'
    elif positiveScore < negativeScore:
        return 'negative'
    else:
        return 'neutral'
