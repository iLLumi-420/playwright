from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

print(EMAIL, PASSWORD)