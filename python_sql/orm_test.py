import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(sqlalchemy.__version__)

"""
Пример использования SQLalchemy не по прямому назначению
"""
engine = sqlalchemy.create_engine("postgresql+psycopg2://postgre:password@localhost:5432/test_db")

collection = engine.connect()

result = collection.execute("SELECT * FROM book")
for row in result:
    print('title', row['title'])

result.close()

trans = collection.begin()
try:
    collection.execute(
        "INSERT INTO book(book_id, title, isbn, publiched_id, weight) VALUES (10, 'worst book', 1111, 2, 10)")
    trans.commit()
except:
    trans.rollback()
    raise

with collection.begin() as trans:
    collection.execute(
        "INSERT INTO book(book_id, title, isbn, publiched_id, weight) VALUES (11, 'worst book', 1111, 1, 11)")

result = collection.execute("SELECT * FROM book")
for row in result:
    print('title', row['title'])

"""
Использование SQLalchemy по прямому назначению
"""

Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    rating = Column(Float)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

author = Author(author_id=18, full_name='Dan Brown', rating=4.7)
session.add(author)

session.commit()

# также можно делать запросы по API
for item in session.query(Author).order_by(Author.rating):
    print(item.full_name, ' ', item.rating)

print('_____________________________')  # для визуального отделения одного вывода цикла от другого

# можно наложить фильтр
for item in session.query(Author).filter(Author.rating > 4.5):
    print(item.full_name, ' ', item.rating)
