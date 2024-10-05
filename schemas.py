from pydantic import BaseModel

class PostDataBase(BaseModel):
    search_query: str
    author_username: str
    video_url: str
    description: str

class PostDataCreate(PostDataBase):
    pass

class PostData(PostDataBase):
    id: int

    class Config:
        orm_mode = True
