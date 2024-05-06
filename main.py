from sqlalchemy import Column, Integer, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from prettytable import PrettyTable

Base = declarative_base() 
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)  

class BookRepository:
    def __init__(self):  
        engine = create_engine('sqlite:///books.db', echo=False) 
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
 
    def create_book(self, title: str, author: str, genre: str):
        book = Book(title=title, author=author, genre=genre)
        self.session.add(book)
        self.session.commit()
        return book
    
    def get_books(self):
        return self.session.query(Book).all()

    def get_book_by_id(self, id: int):
        return self.session.query(Book).filter_by(id=id).first()
    
    def update_book(self, id: int, **fields): 
        query = update(Book).where(Book.id == id).values(fields)
        self.session.execute(query)
        return True

    def delete_book(self, book: Book):
        self.session.delete(book)
        self.session.commit()
        return True
    
    def close(self):
        self.session.close()
  
if __name__ == "__main__":
    book_repository = BookRepository() # create repository instance

    # Insert book
    book_repository.create_book("The Hobbit", "J,R,R Tolkien", "Fantasy")
    book_repository.create_book("1987", "George Orwell", "Dystopian Fiction")
    book_repository.create_book("To Kill a Mockingbird", "Harper Lee", "Southern Gothic, Bildungsroman")
    
    # Get all books
    table = PrettyTable(["id", "title", "author", "genre"])
    books = book_repository.get_books()  
    for book in books:
        table.add_row([book.id, book.title, book.author, book.genre]) 
    print(table)
    table.clear_rows()

    # Get book by id
    book = book_repository.get_book_by_id(1)
    table.add_row([book.id, book.title, book.author, book.genre]) 
    print(table)
    table.clear_rows()

    # Update a book
    fields = { 
        "title": "I am title",
        "author": "I am author",
        "genre": "I am genre"
    }
    book_repository.update_book(book.id, **fields)
    books = book_repository.get_books()  
    for book in books:
        table.add_row([book.id, book.title, book.author, book.genre]) 
    print(table)
    table.clear_rows()

    # Delete a book
    book = book_repository.get_book_by_id(1)
    book_repository.delete_book(book)
    books = book_repository.get_books()  
    for book in books:
        table.add_row([book.id, book.title, book.author, book.genre]) 
    print(table)

    book_repository.close()

    
