from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator
from re import sub


class BookFields(Enum):
    '''
    Book fields for `Book` model
    '''
    isbn = 'ISBN'
    title = 'Title'
    author = 'Author'
    genre = 'Genre'
    year = 'Year'
    copies = 'Copies'

    def __str__(self):
        return f'Enter {self.value} of the Book:'


class Book(BaseModel):
    '''
    Book model for validation and serialization.
    '''
    isbn: str | None = None
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    year: str | int | None = None
    copies: str | int | None = None

    class Config:
        # perform validation on assignment to attributes
        validate_assignment = True
        # strip whitespace from strings
        anystr_strip_whitespace = True

    @validator('*', pre=True)
    def validate_empty(cls, value, field):
        '''
        Pre validator for all fields.
        Checks if input value is not empty.
        '''
        if value is not None and not value:
            raise ValueError(
                f'{field.name.capitalize()} field cannot be empty.')
        return value

    @validator('year', 'copies')
    def validate_int(cls, value, field):
        '''
        Checks if input value is integer.
        '''
        if type(value) == int or value is None:
            return value

        try:
            int(value)
        except ValueError:
            raise ValueError(
                f'{field.name.capitalize()} field must be an integer.')
        return int(value)

    @validator('isbn')
    def validate_isbn(cls, isbn):
        '''
        Removes dashes and underscores from ISBN.
        Checks if it's lenght 13 digits and contains only digits.
        '''
        if isbn is None:
            return isbn
        # re.sub replaces  '-' and '_' with ''
        isbn = sub(r'[-_]', '', isbn)
        if len(isbn) != 13 or not isbn.isdigit():
            raise ValueError('Incorrect ISBN. Must be 13 digits.')
        return isbn

    @validator('year')
    def validate_year(cls, year):
        '''
        Checks if input year in the range 0 - current year.
        '''
        if year is None:
            return year
        if year < 0 or year > datetime.now().year:
            raise ValueError('Incorrect year')
        return year

    @validator('copies')
    def validate_copies(cls, copies):
        '''
        Checks if input copies in the range 0 - 10.
        '''
        if copies is None:
            return copies
        if copies < 0 or copies > 10:
            raise ValueError(
                'Incorrect number of copies. Must be in range 0-10.')
        return copies


# For testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':
    book = Book(
        isbn='978-14-49-357-35-1',
        title='Python Cookbook, 3rd Edition',
        author='David Beazley, Brian K. Jones',
        genre='Computers',
        year=2013,
        copies=4
    )
    book.isbn = None
    print(book.dict())
    book.isbn = '978-0-596-52068-7'
    book.title = ''
    book.year = -324
    book.copies = 11
    print(book.dict())