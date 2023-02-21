from datetime import datetime
from pydantic import BaseModel, validator, conlist, constr
from re import sub

class NonEmptyStr(BaseModel):
    '''
    Validates string for non empty value.
    '''
    str_value: constr(min_length=1, strip_whitespace=True)  # type: ignore


class UniqueStringsList(BaseModel):
    '''
    Validates list and it's values:
    Check if the list not empty and contains unique non empty strings.
    Does not modify the list.
    '''
    # ckeck if list is not empty and contains unique values
    lst: conlist(str, min_items=1, unique_items=True)  # type: ignore

    @validator('lst', each_item=True)
    def check_each_string(cls, item):
        '''
        Checks each list's item if it non empty.
        :param item: list's item
        :return: item if it's not empty
        '''
        if not item.strip():
            raise ValueError('Options list cannot contain empty strings')
        return item

    def to_dict(self) -> dict[int, str]:
        '''
        Converts list to dictionary.
        :return: dictionary with numbered list's items
        '''
        return {i + 1: item for i, item in enumerate(self.lst)}


class IntInRange(BaseModel):
    '''
    Validates user code input for correct range.
    '''
    num_range: int
    num: int

    @validator('num')
    def validate_num_range(cls, num, values):
        '''
        Check if the num is in the range.
        :param num: user input
        :param values: code range
        :return: code if it's in the range
        '''
        if num not in range(1, values['num_range'] + 1):
            raise ValueError(
                f'Code must be in range 1-{values["num_range"]}')
        return num


class Book(BaseModel):
    isbn: str
    title: str
    author: str
    genre: str
    year: str | int
    copies: str | int

    @validator('*', pre=True)
    def validate_empty(cls, value, field):
        '''
        Pre validator for all fields.
        Checks if input value is not empty.
        '''
        tested_value = value.strip() if isinstance(value, str) else value
        if not tested_value:
            raise ValueError(f'{field.name.capitalize()} field cannot be empty.')
        return value

    @validator('year', 'copies')
    def validate_int(cls, value, field):
        '''
        Checks if input value is integer.
        '''
        if type(value) == int:
            return value

        try:
            int(value)
        except ValueError:
            print(value)
            raise ValueError(f'{field.name.capitalize()} field must be an integer.')
        return int(value)

    @validator('isbn')
    def validate_isbn(cls, isbn):
        '''
        Removes dashes and underscores from ISBN.
        Checks if it's lenght 13 digits and contains only digits.
        '''
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
        if year < 0 or year > datetime.now().year:
            raise ValueError('Incorrect year')
        return year

    @validator('copies')
    def validate_copies(cls, copies):
        '''
        Checks if input copies in the range 0 - 10.
        '''
        if copies < 0 or copies > 10:
            raise ValueError('Incorrect number of copies. Must be in range 0-10.')
        return copies


# For testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':
    book = Book(
        isbn='978-034-52-9-60-61',
        title='The Lord of the Rings',
        author='J.R.R. Tolkien',
        genre='Fantasy',
        year=1954,
        copies='4'
    )
    print(book.dict())
