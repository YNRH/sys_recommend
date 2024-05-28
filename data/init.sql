
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    cookie_id VARCHAR(50) NOT NULL UNIQUE,
    username VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    release_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(20) NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INT REFERENCES movies(movie_id),
    genre_id INT REFERENCES genres(genre_id),
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE ratings (
    user_id INT REFERENCES users(user_id),
    movie_id INT REFERENCES movies(movie_id),
    rating DECIMAL(2, 1) CHECK (rating >= 0 AND rating <= 5),
    watched_duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id)
);


INSERT INTO genres (genre_name) VALUES
('Action'),       -- 1
('Animation'),    -- 3
('Adventure'),    -- 2
('Comedy'),       -- 4
('Crime'),        -- 5             
('Drama'),        -- 6
('Fantasy'),      -- 7
('Family'),       -- 8
('History'),      -- 9
('Horror'),       -- 10
('Musical'),      -- 11
('Mystery'),      -- 12
('Romance'),      -- 13
('Sci-Fi'),       -- 14
('Thriller'),     -- 15
('War'),          -- 16
('Western');      -- 17


INSERT INTO movies (title, description, release_date) VALUES
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption in their friendship.', '1994-10-14'),
('The Godfather', 'The story of the Corleone family under patriarch Vito Corleone, focusing on the transformation of his youngest son, Michael, from reluctant family outsider to ruthless mafia boss.', '1972-03-24'),
('The Dark Knight', 'When the mentally challenged Joker wreaks havoc and chaos on Gotham City, Batman must face him and endure unimaginable consequences to ultimately save the town.', '2008-07-18'),
('The Lord of the Rings: The Return of the King', 'Gandalf and Aragorn lead the World of Men against Sauron is army to draw his gaze away from Minas Tirith, as Frodo and Sam journey to Mordor to destroy the One Ring.', '2003-12-17'),
('Pulp Fiction', 'The lives of two mob hit men, a boxer, and a gangster is wife intertwine in a series of violent events across Los Angeles.', '1994-09-23'),
('Schindler is List', 'The true story of Oskar Schindler, a German businessman who saved the lives of over a thousand Jews during the Holocaust.', '1993-12-15'),
('12 Angry Men', 'A jury deliberates the fate of a young man accused of murdering his father in this classic courtroom drama.', '1957-04-11'),
('Fight Club', 'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much, much more.', '1999-10-15'),
('Forrest Gump', 'The life of Forrest Gump, a small-town Alabama man with an IQ of 75, is chronicled through decades of American history.', '1994-06-11'),
('The Matrix', 'A computer hacker learns that the world he lives in is actually a computer simulation and he is responsible for liberating humanity from the machines.', '1999-03-31'),


--('aa1', 'A', '1999-03-31'),
--('aaa2', 'A', '1999-03-31');


-- Link movies to genres using movie_id and genre_id based on your data
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 13), -- The Shawshank Redemption (Drama)
(2, 15), -- The Godfather (Crime)
(3, 14), -- The Dark Knight (Action)
(4, 16), -- The Lord of the Rings: The Return of the King (Fantasy)
(5, 15), -- Pulp Fiction (Crime)
(6, 16), -- Schindler's List (History)
(7, 13), -- 12 Angry Men (Drama)
(8, 15), -- Fight Club (Crime)
(9, 13), -- Forrest Gump (Drama)
(10, 14);  -- The Matrix (Sci-Fi)
