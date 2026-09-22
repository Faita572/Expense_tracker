import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, init_db 

try:
    init_db()
except Exception as e:
    print(f"DB Init Note: {e}")  

app = app