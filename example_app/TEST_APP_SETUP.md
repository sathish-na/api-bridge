# Example App - API Bridge

This is a sample FastAPI application that demonstrates how to use the `api_bridge` library to generate APIs dynamically from a database.

## 📌 Installation

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ..
```

## Run App

```
uvicorn v1_impl:app --reload
uvicorn v2_impl:app --reload
uvicorn v3_impl:app --reload
```
