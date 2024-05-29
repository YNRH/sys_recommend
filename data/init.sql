
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
    video_url VARCHAR(100),
    cluster_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(20) NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INT REFERENCES movies(movie_id) ON DELETE CASCADE,
    genre_id INT REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE ratings (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    movie_id INT REFERENCES movies(movie_id) ON DELETE CASCADE,
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
('Western'),      -- 17
('Biography');      -- 18


INSERT INTO movies (title, description, release_date, video_url) VALUES
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption in their friendship.', '1994-10-14', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('The Godfather', 'The story of the Corleone family under patriarch Vito Corleone, focusing on the transformation of his youngest son, Michael, from reluctant family outsider to ruthless mafia boss.', '1972-03-24', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('The Dark Knight', 'When the mentally challenged Joker wreaks havoc and chaos on Gotham City, Batman must face him and endure unimaginable consequences to ultimately save the town.', '2008-07-18', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('The Lord of the Rings: The Return of the King', 'Gandalf and Aragorn lead the World of Men against Sauron is army to draw his gaze away from Minas Tirith, as Frodo and Sam journey to Mordor to destroy the One Ring.', '2003-12-17', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Pulp Fiction', 'The lives of two mob hit men, a boxer, and a gangster is wife intertwine in a series of violent events across Los Angeles.', '1994-09-23', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Schindler is List', 'The true story of Oskar Schindler, a German businessman who saved the lives of over a thousand Jews during the Holocaust.', '1993-12-15', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('12 Angry Men', 'A jury deliberates the fate of a young man accused of murdering his father in this classic courtroom drama.', '1957-04-11', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Fight Club', 'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much, much more.', '1999-10-15', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Forrest Gump', 'The life of Forrest Gump, a small-town Alabama man with an IQ of 75, is chronicled through decades of American history.', '1994-06-11', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('The Matrix', 'A computer hacker learns that the world he lives in is actually a computer simulation and he is responsible for liberating humanity from the machines.', '1999-03-31', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),

('Soul', 'A New York jazz musician who dreams of playing on the most prestigious stage in the world finds himself on an unexpected journey to "The Great Before", a realm where souls are created before being sent to Earth. There, he must find a way to inspire a new, cynical soul to discover the joy of life.', '2020-12-25', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Nomadland', 'Fern, a sixty-year-old woman who loses everything during the Great Recession, decides to buy a truck and embark on a journey through the American West. Along the way, she meets other nomads and experiences the freedom and beauty of life on the road. ', '2020-11-20', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Tenet', 'A secret agent travels through time to prevent World War III from starting. He must use innovative technology to reverse the course of time and save the world.', '2020-09-03', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Mank', 'A look at the life of Herman J. Mankiewicz, the screenwriter of the movie Citizen Kane. The film chronicles Mankiewicz is struggle to complete the script as he battles alcoholism and studio pressure. ', '2020-12-04', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Promising Young Woman', ' Cassie, a young woman seeking revenge against men who prey on drunk women, finds herself in a dangerous situation when she falls in love with a young doctor.', '2020-06-12', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('The Father', 'An 81-year-old man with dementia lives with his daughter, who struggles to care for him while he refuses to accept his illness. The film explores memory, identity and family love. ', '2020-06-08', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Judas and the Black Messiah', 'The true story of Fred Hampton, a leader of the Black Panther Party, and William Neal, an FBI informant who infiltrated the party. The film explores the complexity of the Black Lives Matter movement and the cost of political activism.', '2020-02-12', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Minari', 'A Korean-American family moves to a rural farm in Arkansas in the 1980s. The film explores the themes of cultural identity, the fight for the American dream, and family resilience. ', '2020-02-25', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Wonder Woman 1984', 'Diana Prince faces two new enemies in the 1980s: Maxwell Lord, a greedy businessman, and Cheetah, a warrior woman seeking revenge. The film explores themes such as love, sacrifice and the power of truth.', '2020-12-25', 'https://www.youtube.com/watch?v=OM0tSTEQCQA'),
('Cruella', 'The origin story of Cruella de Vil, the villain of 101 Dalmatians. The film explores ambition, revenge and rebellion against social norms.', '2020-05-28', 'https://www.youtube.com/watch?v=OM0tSTEQCQA');


--('aa1', 'A', '1999-03-31'),
--('aaa2', 'A', '1999-03-31');


-- Link movies to genres using movie_id and genre_id based on your data
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 6), -- The Shawshank Redemption (Drama)
(2, 5), -- The Godfather (Crime)
(3, 1), -- The Dark Knight (Action)
(4, 7), -- The Lord of the Rings: The Return of the King (Fantasy)
(5, 5), -- Pulp Fiction (Crime)
(6, 9), -- Schindler's List (History)
(7, 6), -- 12 Angry Men (Drama)
(8, 5), -- Fight Club (Crime)
(9, 6), -- Forrest Gump (Drama)
(10, 14),  -- The Matrix (Sci-Fi)

(11, 3),
(11, 4),
(11, 6),
(12, 6),
(13, 1),
(13, 14),
(13, 15),
(14, 6),
(14, 18),
(15, 15),
(15, 4),
(16, 6),
(17, 18),
(17, 6),
(17, 9),
(18, 6),
(19, 1),
(19, 2),
(19, 7),
(20, 4),
(20, 6);

