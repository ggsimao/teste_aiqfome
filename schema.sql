DROP TABLE IF EXISTS Favorites;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR (50) NOT NULL,
    user_email VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE Favorites (
    fav_id SERIAL PRIMARY KEY,
    prod_id INTEGER NOT NULL,
    user_id INTEGER REFERENCES Users(user_id),
    CONSTRAINT unique_fav UNIQUE (prod_id, user_id)
);