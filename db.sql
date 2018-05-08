CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    post INTEGER NOT NULL,
    user INTEGER NOT NULL,
    datetime_int INTEGER NOT NULL,
    content TEXT DEFAULT ""
);
