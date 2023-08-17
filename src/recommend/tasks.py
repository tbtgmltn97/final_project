from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
import redis
from django.conf import settings
import datetime 
import json


with open('secrets.json') as f:
   secrets = json.loads(f.read())

@shared_task(bind=True)
def store_input_data_in_redis(self, input_data):
    redis_conn = redis.Redis(host=secrets["redis_host"], port=secrets["redis_port"], db=secrets["redis_db"], password= secrets["redis_pw"])
    print(redis_conn)
    # redis_conn = celery_app.backend.client
    date = datetime.datetime.now()
    redis_key = f"input_data:{date}"
    redis_conn.set(redis_key, ",".join(input_data))
    
@shared_task
def send_data_to_fastapi(data):
    url = 'http://34.64.174.219:8001/process'  # FastAPI 엔드포인트 주소
    response = requests.post(url, json={"input_data": data})
    return response.json()


