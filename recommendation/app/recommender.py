import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import SVC
import numpy as np
from sqlalchemy.orm import Session
from .models import Movie, Rating, User, MovieGenre
from .database import get_db

# Preprocesamiento de datos
def preprocess_movies(db: Session):
    movies = db.query(Movie).all()
    descriptions = [movie.description for movie in movies]

    # TF-IDF vectorización
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)

    # K-Means clustering
    kmeans = KMeans(n_clusters=10, random_state=42)
    movie_clusters = kmeans.fit_predict(tfidf_matrix)

    for movie, cluster in zip(movies, movie_clusters):
        movie.cluster_id = cluster
        db.add(movie)
    db.commit()

    return tfidf_matrix, movie_clusters

# Filtrado Colaborativo
def collaborative_filtering(db: Session, user_id: int):
    ratings = db.query(Rating).all()
    user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    user_ids = [rating.user_id for rating in ratings]
    movie_ids = [rating.movie_id for rating in ratings]

    ratings_matrix = pd.pivot_table(pd.DataFrame([(r.user_id, r.movie_id, r.rating) for r in ratings], columns=["user_id", "movie_id", "rating"]),
                                    index='user_id', columns='movie_id', values='rating').fillna(0)

    user_vector = ratings_matrix.loc[user_id].values
    distances = ratings_matrix.apply(lambda row: np.sum(np.abs(row - user_vector)), axis=1)
    similar_users = distances.nsmallest(10).index
    similar_users_ratings = ratings_matrix.loc[similar_users]

    recommendations = similar_users_ratings.mean().sort_values(ascending=False)
    watched_movies = [r.movie_id for r in user_ratings]

    return recommendations[~recommendations.index.isin(watched_movies)].index.tolist()

# Filtrado Basado en Contenido
def content_based_filtering(db: Session, user_id: int, tfidf_matrix, movie_clusters):
    user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    liked_movies = [rating.movie_id for rating in user_ratings if rating.rating > 3.5]
    
    if not liked_movies:
        return []

    liked_movie_indices = [idx for idx, movie in enumerate(db.query(Movie).all()) if movie.movie_id in liked_movies]
    liked_movie_clusters = [movie_clusters[idx] for idx in liked_movie_indices]
    
    similar_movies = []
    for cluster in liked_movie_clusters:
        similar_movies += [movie.movie_id for idx, movie in enumerate(db.query(Movie).all()) if movie_clusters[idx] == cluster]

    similarity_matrix = cosine_similarity(tfidf_matrix)
    similar_movie_indices = [idx for idx, movie in enumerate(db.query(Movie).all()) if movie.movie_id in similar_movies]

    movie_scores = {}
    for idx in liked_movie_indices:
        for sim_idx in similar_movie_indices:
            if sim_idx not in movie_scores:
                movie_scores[sim_idx] = similarity_matrix[idx, sim_idx]

    movie_scores = sorted(movie_scores.items(), key=lambda item: item[1], reverse=True)
    return [db.query(Movie).all()[idx].movie_id for idx, _ in movie_scores[:10]]

# Modelo de Predicción
def svm_prediction(db: Session, user_id: int):
    # Preparar datos para el entrenamiento del SVM
    data = []
    ratings = db.query(Rating).all()
    for rating in ratings:
        user = db.query(User).filter(User.user_id == rating.user_id).first()
        movie = db.query(Movie).filter(Movie.movie_id == rating.movie_id).first()
        data.append([user.user_id, movie.movie_id, movie.cluster_id, rating.rating])

    df = pd.DataFrame(data, columns=['user_id', 'movie_id', 'cluster_id', 'rating'])
    df['like'] = df['rating'].apply(lambda x: 1 if x > 3.5 else 0)

    X = df[['user_id', 'movie_id', 'cluster_id']]
    y = df['like']

    svm = SVC(probability=True)
    svm.fit(X, y)

    # Predecir la probabilidad de que al usuario le guste cada película
    predictions = []
    for movie in db.query(Movie).all():
        user_data = [[user_id, movie.movie_id, movie.cluster_id]]
        prob = svm.predict_proba(user_data)[0][1]
        predictions.append((movie.movie_id, prob))

    predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
    return [movie_id for movie_id, _ in predictions[:10]]

# Recomendar Películas
def recommend_movie(user_id: int):
    db = next(get_db())

    # Preprocesar películas
    tfidf_matrix, movie_clusters = preprocess_movies(db)

    # Filtrado colaborativo
    collab_recommendations = collaborative_filtering(db, user_id)

    # Filtrado basado en contenido
    content_recommendations = content_based_filtering(db, user_id, tfidf_matrix, movie_clusters)

    # Modelo de predicción
    svm_recommendations = svm_prediction(db, user_id)

    # Combinar y priorizar recomendaciones
    combined_recommendations = list(set(collab_recommendations + content_recommendations + svm_recommendations))

    return combined_recommendations[:2]  # Limitar a las 10 principales recomendaciones
