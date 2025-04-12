import uvicorn
from app.main import app  # Ensure the path here is correct

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
