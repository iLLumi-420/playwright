import psycopg2
import json

conn = psycopg2.connect(
    dbname="linkedin_data",
    user="postgres",
    password="postgres",
    host="localhost"
)
cursor = conn.cursor()

with open('./data.json', 'r') as f:
    data = json.load(f)

for item in data:
    cursor.execute(
        """
        INSERT INTO linkedin_posts (comments_number, likes_number, post_urn, text, posted_by, company_name, company_url, post_hashtag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            item.get('comments_number'),
            item.get('likes_number'),
            item.get('post_urn'),
            item.get('text'),
            item.get('posted_by'),
            item.get('company_name'),
            item.get('company_url'),
            item.get('post_hashtag')
        )
    )

conn.commit()

cursor.execute("SELECT * FROM linkedin_posts LIMIT 10")
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
conn.close()
