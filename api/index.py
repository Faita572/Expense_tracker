from app import app, init_db

# Initialize database tables on cold start
init_db()

# Exposed serverless handler for Vercel
app_handler = app