from dataclasses import dataclass, field 
from datetime import datetime

@dataclass
class Story:  
    _id: str
    image: str
    temperature: float
    max_new_tokens: int
    top_p: float
    repetition_penalty: float
    result: str
    # rating: int = 0
    date: datetime 
    type: str='story'
    created_time: datetime = field(default_factory=datetime.utcnow)

# step1: define a User class
# step2: in routes.py import this User
@dataclass
class User:
    _id: str
    email: str
    password: str
    stories: list[str] = field(default_factory=list) # list of story id that user've created
    # the User will keep track of what stories they have added

@dataclass
class StoryPdf:
    _id: str
    pdfs: list[str]
    image: str
    temperature: float
    max_new_tokens: int
    top_p: float
    repetition_penalty: float
    chunk_size: int
    chunk_overlap: int
    top_k: int
    result: str
    # rating: int = 0
    date: datetime
    type: str='storyPdf'
    created_time: datetime = field(default_factory=datetime.utcnow)
    # in index.html page will sort all stories by created time





