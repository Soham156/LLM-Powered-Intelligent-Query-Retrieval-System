from fastapi import FastAPI
from main import app

# Vercel expects a variable named 'app' at the module level
# This ensures compatibility with Vercel's Python runtime
handler = app
