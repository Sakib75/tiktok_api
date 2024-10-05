from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PostData(Base):
    __tablename__ = "post_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    search_query = Column(Text)
    author_username = Column(Text)
    video_url = Column(Text)
    description = Column(Text)
