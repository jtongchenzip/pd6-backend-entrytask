CREATE TABLE post (
    id      SERIAL  PRIMARY KEY,
    title   VARCHAR NOT NULL,
    content VARCHAR NOT NULL
);

CREATE TABLE comment (
    id      SERIAL  PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES post(id),
    content VARCHAR NOT NULL
);