import asyncio

"""
async for - нужен для работы с асинхронными запросами...
"""


async def fetch_doc(doc):
    await asyncio.sleep(1)
    return doc


async def get_pages(docs):
    for cur_doc in docs:
        doc = await fetch_doc(cur_doc)
        for page in doc:
            await asyncio.sleep(1)
            yield page


async def main():
    async for page in get_pages(['doc_1', 'doc_2', 'doc_3', 'doc_4']):
        print(f'Finally {page}')


if __name__ == '__main__':
    asyncio.run(main())
