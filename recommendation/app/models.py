from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(String(50), unique=True, index=True)
    username = Column(String(20))
    created_at = Column(TIMESTAMP)

class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True)
    description = Column(Text)
    release_date = Column(Date)
    video_url = Column(String(100))
    cluster_id = Column(Integer)
    created_at = Column(TIMESTAMP)

class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String(20))

class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)

class Rating(Base):
    __tablename__ = 'ratings'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    rating = Column(DECIMAL(2, 1))
    watched_duration = Column(Integer)
    created_at = Column(TIMESTAMP)

class RecommendationCache(Base):
    __tablename__ = 'recommendation_cache'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))