import random

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utilities import preprocessText

def smallTalkResponse(path, input, threshold):
    df = pd.read_csv(path)
    df['processedQuestions'] = df['Question'].apply(preprocessText)

    # TF-IDF
    tfidf_vec = TfidfVectorizer(analyzer='word')
    X_tfidf = tfidf_vec.fit_transform(df['Question']).toarray()
    df_tfidf = pd.DataFrame(X_tfidf, columns=tfidf_vec.get_feature_names_out())

    # process query
    input_tfidf = tfidf_vec.transform([input.lower()]).toarray()

    # cosine similarity
    similarity = cosine_similarity(df_tfidf, input_tfidf)

    maxSimilarity = np.max(similarity)

    if maxSimilarity > threshold:
        idArgmax = np.where(similarity == np.max(similarity, axis=0))
        randomId = np.random.choice(idArgmax[0])
        return df['Answer'].loc[randomId]
    else:
        return 'UNKNOWN'

