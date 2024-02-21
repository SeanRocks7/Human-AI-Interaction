from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utilities import preprocessText

intents = {
    "book_flight": ["book a flight", "I want to fly", "need a plane ticket", "reserve flight", "want to travel", "booking my flight"],
    "change_flight": ["change my booking", "reschedule my flight", "change flight date"],
    "cancel_flight": ["cancel my flight", "I need to cancel my ticket", "stop my reservation", "want to cancel"],
}

# Preprocess intents
for intent, texts in intents.items():
    intents[intent] = [preprocessText(text) for text in texts]

# Train a TF-IDF Vectorizer on the intents
all_texts = sum(intents.values(), [])
vectorizer = TfidfVectorizer()
vectorizer.fit(all_texts)

# Function to find the closest intent
def getIntent(userInput, threshold):
    processedInput = preprocessText(userInput)
    userVector = vectorizer.transform([processedInput])

    bestIntent = None
    maxSimilarity = 0

    for intent, texts in intents.items():
        intentVectors = vectorizer.transform(texts)
        similarity = np.max(cosine_similarity(intentVectors, userVector))

        if similarity > maxSimilarity:
            bestIntent = intent
            maxSimilarity = similarity

    if maxSimilarity >= threshold:
        return bestIntent
    else:
        return None