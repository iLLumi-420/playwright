import psycopg2
import json

conn = psycopg2.connect(
    dbname="linkedin_data",
    user="postgres",
    password="postgres",
    host="localhost"
)
cursor = conn.cursor()

with open('./data.json', 'r') as file:
    data = json.load(file)

# cursor.execute("DROP TABLE linkedin_posts")
# cursor.execute("""
#     CREATE TABLE linkedin_posts (
#             id SERIAL PRIMARY KEY,
#             post_id VARCHAR(255),
#             post_url VARCHAR(255),
#             comments INTEGER,
#             reactions INTEGER,
#             reaction_type JSONB,
#             hashtag VARCHAR(255),
#             media VARCHAR(255),
#             text TEXT,
#             publisher VARCHAR(255),
#             publisher_url VARCHAR(255),
#             shared INTEGER
#     )
# """)

# for item in data:
#     cursor.execute(
#         """
#         INSERT INTO linkedin_posts (id, post_id, post_url, comments, reactions, reaction_type, hashtag, media, text, publisher, publisher_url, shared)
#         VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """,
#         (
#             item.get('post_id'),
#             item.get('post_url'),
#             item.get('comments'),
#             item.get('reactions'),
#             json.dumps(item.get('reaction_type')),
#             item.get('hashtag'),
#             item.get('media'),
#             item.get('text'),
#             item.get('publisher'),
#             item.get('publisher_url'),
#             item.get('shared')
#         )
#     )


conn.commit()

cursor.execute("SELECT * FROM linkedin_posts LIMIT 10")
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
conn.close()
