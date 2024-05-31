import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import SVC
from sqlalchemy.event import listen
from .models import User, Movie, Rating, RecommendationCache
from .database import engine

# Configuración de la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def preprocess_movies():
    db = SessionLocal()
    try:
        movies = db.query(Movie).all()
        if not movies:
            return

        descriptions = [movie.description for movie in movies]
        
        # Convertir descripciones a vectores TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        
        # Agrupar las películas en clusters usando K-Means
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(tfidf_matrix)
        clusters = kmeans.labels_
        
        # Actualizar la base de datos con el cluster de cada película
        for i, movie in enumerate(movies):
            movie.cluster_id = int(clusters[i])
            db.add(movie)
        db.commit()
    finally:
        db.close()

def collaborative_filtering(user_id):
    db = SessionLocal()
    try:
        ratings = pd.read_sql(db.query(Rating).statement, db.bind)
        user_ratings = ratings[ratings['user_id'] == user_id]

        if user_ratings.empty:
            return []

        rating_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating')
        rating_matrix = rating_matrix.fillna(0)

        user_similarity = cosine_similarity(rating_matrix)
        user_similarity = pd.DataFrame(user_similarity, index=rating_matrix.index, columns=rating_matrix.index)

        similar_users = user_similarity[user_id].sort_values(ascending=False).index[1:11]

        similar_users_ratings = rating_matrix.loc[similar_users]
        mean_ratings = similar_users_ratings.mean(axis=0)
        recommendations = mean_ratings[mean_ratings > 0].sort_values(ascending=False).index.tolist()

        return recommendations
    finally:
        db.close()

def content_based_filtering(user_id):
    db = SessionLocal()
    try:
        user_ratings = db.query(Rating).filter(Rating.user_id == user_id, Rating.rating >= 4).all()
        if not user_ratings:
            return []

        liked_movie_ids = [rating.movie_id for rating in user_ratings]
        liked_movies = db.query(Movie).filter(Movie.movie_id.in_(liked_movie_ids)).all()

        if not liked_movies:
            return []

        liked_clusters = set(movie.cluster_id for movie in liked_movies)
        candidate_movies = db.query(Movie).filter(Movie.cluster_id.in_(liked_clusters)).all()

        if not candidate_movies:
            return []

        candidate_descriptions = [movie.description for movie in candidate_movies]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(candidate_descriptions)

        user_movie_descriptions = [movie.description for movie in liked_movies]
        user_tfidf_matrix = vectorizer.transform(user_movie_descriptions)

        similarities = cosine_similarity(user_tfidf_matrix, tfidf_matrix).mean(axis=0)
        similarity_scores = list(zip(candidate_movies, similarities))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        recommendations = [movie.movie_id for movie, _ in similarity_scores]
        return recommendations
    finally:
        db.close()

def svm_prediction(user_id):
    db = SessionLocal()
    try:
        ratings = pd.read_sql(db.query(Rating).statement, db.bind)
        if ratings.empty:
            return []

        rating_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating')
        rating_matrix = rating_matrix.fillna(0)

        X = rating_matrix.drop(columns=user_id, errors='ignore')
        y = rating_matrix[user_id].fillna(0)
        
        model = SVC(probability=True)
        model.fit(X, y)

        predicted_ratings = model.predict_proba(X)[:, 1]
        movie_ids = X.columns
        recommendations = sorted(zip(movie_ids, predicted_ratings), key=lambda x: x[1], reverse=True)

        recommendations = [movie_id for movie_id, _ in recommendations]
        return recommendations
    finally:
        db.close()

def recommend_movie(user_id):
    db = SessionLocal()
    try:
        # Intentar obtener recomendación desde el cache
        cached_rec = get_cached_recommendation(user_id)
        if cached_rec:
            return cached_rec

        user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()

        if not user_ratings:
            return recommend_general_movie()

        if len(user_ratings) < 5:
            content_recs = content_based_filtering(user_id)
            if content_recs:
                movie_id = content_recs[0]
                update_recommendation_cache(user_id, movie_id)
                movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
                return {"movie_id": movie.movie_id, "title": movie.title, "video_url": movie.video_url}
            else:
                return recommend_general_movie()

        preprocess_movies()
        collab_recs = collaborative_filtering(user_id)
        content_recs = content_based_filtering(user_id)
        svm_recs = svm_prediction(user_id)

        all_recs = collab_recs + content_recs + svm_recs
        unique_recs = list(dict.fromkeys(all_recs))

        for rec in unique_recs:
            movie = db.query(Movie).filter(Movie.movie_id == rec).first()
            if movie:
                update_recommendation_cache(user_id, rec)
                return {"movie_id": movie.movie_id, "title": movie.title, "video_url": movie.video_url}
    finally:
        db.close()

def recommend_general_movie():
    db = SessionLocal()
    try:
        random_movie = db.query(Movie).order_by(func.random()).first()
        return {"movie_id": random_movie.movie_id, "title": random_movie.title, "video_url": random_movie.video_url}
    finally:
        db.close()

def get_cached_recommendation(user_id):
    db = SessionLocal()
    try:
        cached_rec = db.query(RecommendationCache).filter(RecommendationCache.user_id == user_id).first()
        if cached_rec:
            movie = db.query(Movie).filter(Movie.movie_id == cached_rec.movie_id).first()
            return {"movie_id": movie.movie_id, "title": movie.title, "video_url": movie.video_url}
        return None
    finally:
        db.close()

def update_recommendation_cache(user_id, movie_id):
    db = SessionLocal()
    try:
        # Eliminar entrada existente
        db.query(RecommendationCache).filter(RecommendationCache.user_id == user_id).delete()
        # Insertar nueva recomendación
        new_cache = RecommendationCache(user_id=user_id, movie_id=movie_id)
        db.add(new_cache)
        db.commit()
    finally:
        db.close()

def handle_new_rating(mapper, connection, target):
    user_id = target.user_id
    recommend_movie(user_id)

listen(Rating, 'after_insert', handle_new_rating)
