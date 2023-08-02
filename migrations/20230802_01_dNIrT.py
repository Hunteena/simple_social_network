"""
Initial
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        'CREATE TABLE IF NOT EXISTS users ('
        '	id serial PRIMARY KEY,'
        '	username varchar(100) UNIQUE NOT NULL,'
        '	email varchar(100) NOT NULL,'
        '	"password" varchar(100) NOT NULL'
        ');'
    ),
    step(
        'CREATE TABLE IF NOT EXISTS posts ('
        '	id serial PRIMARY KEY,'
        '	user_id int NOT NULL REFERENCES users ON DELETE CASCADE,'
        '	title varchar(200) NOT NULL,'
        '	"text" text NOT NULL,'
        '	created_at timestamp DEFAULT now(),'
        '	updated_at timestamp'
        ');'
    ),
    step(
        'CREATE TABLE IF NOT EXISTS likes ('
        '	id serial PRIMARY KEY,'
        '	post_id int NOT NULL REFERENCES posts ON DELETE CASCADE,'
        '	user_id int NOT NULL REFERENCES users ON DELETE CASCADE,'
        '	"like" bool,'
        '	UNIQUE (post_id, user_id)'
        ');'
    )
]
