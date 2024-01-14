from datetime import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {'message': 'Hello world!'}

@app.post('/post')
def post():
    new_row = Timestamp(id=len(post_db), timestamp=int(datetime.now().timestamp()))
    post_db.append(new_row)
    return new_row

@app.get('/dog')
def get_dog(kind: DogType = None):
    if kind is None:
        return list(dogs_db.values())
    return [dog for dog in dogs_db.values() if dog.kind == kind]

@app.post('/dog')
def create_dog(dog: Dog):
    if dog.pk in [dog.pk for dog in dogs_db.values()]:
        raise HTTPException(status_code=404, detail='chosen pk exists')
    dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{pk}')
def get_dog(pk: int):
    if pk in [dog.pk for dog in dogs_db.values()]:
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=404, detail='chosen pk does not exist')

@app.patch('/dog/{pk}')
def get_dog(pk: int, dog: Dog):
    if pk in [dog.pk for dog in dogs_db.values()]:
        dogs_db[pk] = dog
    else:
        raise HTTPException(status_code=404, detail='chosen pk does not exist')
    return dog
