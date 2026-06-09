import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

with app.test_client() as client:
    resp = client.patch('/extracted', json={'updated_field': 'test value'})
    print('STATUS', resp.status_code)
    print('CONTENT-TYPE', resp.content_type)
    data = resp.get_data(as_text=True)
    print('BODY PREVIEW (first 800 chars):')
    print(data[:800])
