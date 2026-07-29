#!/bin/bash
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --host 0.0.0.0 --port $PORT 
