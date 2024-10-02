# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from dotenv import load_dotenv
# import time

# load_dotenv()
# db_password =  os.getenv("DB_PASSWORD")


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password=db_password,cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection to databse is successful")
#         break

#     except Exception as error:
#         print("Connection failed")
#         print(F"Error: {error}")
#         time.sleep(3)

from datetime import datetime, timezone


print(datetime.now())
# print(datetime.utcnow())
print(datetime.now(timezone.utc))
