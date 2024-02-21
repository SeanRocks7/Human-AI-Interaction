import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utilities import preprocessText

NAME = ["call", "me", "change", "my", "name", "to", "please", "rename", "switch", "yes", "sure"]
CHANGE_NAME_KEYWORDS = ["rename", "switch"]

def rememberName(path, userInput, threshold):
    df = pd.read_csv(path)

    # Assuming the dataset has 'Question' and 'Answer' columns
    questions = df['Question'].apply(preprocessText)

    # Vectorize the questions using tfidf
    vectorizer = TfidfVectorizer(analyzer='word')
    vecQuestions = vectorizer.fit_transform(questions)

    # Transform the query
    proccessedInput = preprocessText(userInput)
    vecQuery = vectorizer.transform([proccessedInput])

    # Compute similarities
    similarities = cosine_similarity(vecQuery, vecQuestions)

    # Find the most similar question
    max_similarity = np.max(similarities)

    if max_similarity > threshold:
        return 'ANSWER'
    else:
        return "UNKNOWN"

def switchName(userInput):
    text_tokens = word_tokenize(userInput)
    # Remove stopwords and name change keywords from the tokens
    nameTokens = []
    for word in text_tokens:
        if word.lower() not in stopwords.words('english') and word.lower() not in NAME:
            nameTokens.append(word)

    # Join the remaining tokens to form the name
    return ' '.join(nameTokens).strip()

def checkUserChangeName(userInput):
    for keyword in CHANGE_NAME_KEYWORDS:
        if keyword in userInput.lower():
            return True
    return False