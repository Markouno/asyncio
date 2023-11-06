import asyncio
import aiohttp
from more_itertools import chunked
from models import Character, Session, init_db
from datetime import datetime
from pprint import pprint

CHUNK_SIZE = 10


async def edit_data(person, person_id):
    if 'url' in person:
        person.pop('url')
        person['id'] = person_id
        return person
    else:
        pass


async def paste_to_db(people, people_id_chunk):
    async with Session() as session:
        zip_data = zip(people, people_id_chunk)

        edited_people = [edit_data(person, people_id) for person, people_id in zip_data]
        correct_data = await asyncio.gather(*edited_people)
        pprint(correct_data)
        print('-'*50)

        characters = [Character(json=person) for person in correct_data]

        session.add_all(characters)
        await session.commit()


async def get_character(person_id, session):
    response = await session.get(f'https://swapi.py4e.com/api/people/{person_id}/')
    json = await response.json()
    return json


async def main():
    await init_db()

    async with aiohttp.ClientSession() as session:
        for people_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
            coros = [get_character(person_id, session) for person_id in people_id_chunk]
            result = await asyncio.gather(*coros)
            await paste_to_db(result, people_id_chunk)


start = datetime.now()
asyncio.run(main())
print(datetime.now() - start)



