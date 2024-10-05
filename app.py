from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal

# Create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/post_data/", response_model=schemas.PostData)
def create_post_data(post: schemas.PostDataCreate, db: Session = Depends(get_db)):
    db_post = models.PostData(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/post_data/{post_id}", response_model=schemas.PostData)
def read_post_data(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.PostData).filter(models.PostData.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/post_data/{post_id}", response_model=schemas.PostData)
def update_post_data(post_id: int, post: schemas.PostDataCreate, db: Session = Depends(get_db)):
    db_post = db.query(models.PostData).filter(models.PostData.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/post_data/{post_id}")
def delete_post_data(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.PostData).filter(models.PostData.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted successfully"}

# New API to get all post data
@app.get("/post_data/", response_model=list[schemas.PostData])
def get_all_post_data(db: Session = Depends(get_db)):
    posts = db.query(models.PostData).all()
    return posts
