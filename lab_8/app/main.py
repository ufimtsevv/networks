from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="URL Saver API")

DATABASE_URL = "postgresql://book_user:password@db/book_parser"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

class URLResponse(BaseModel):
    url: str

    class Config:
        from_attributes = True

@app.get("/save_url")
async def save_url(url: str):
    db = SessionLocal()
    try:
        db_url = URL(url=url)
        db.add(db_url)
        db.commit()
        return {"status": "success", "url": url}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/get_urls", response_model=list[URLResponse])
async def get_urls():
    db = SessionLocal()
    try:
        urls = db.query(URL).all()
        return urls
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "URL Saver API. Use /save_url and /get_urls."}