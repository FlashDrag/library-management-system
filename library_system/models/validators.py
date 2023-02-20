from datetime import datetime
from pydantic import BaseModel, validator, conlist, constr
from ..views.tools import InputPrompts


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


class UserInput(BaseModel):
    isbn: str
    title: str
    author: str
    genre: str
    year: int
    copies: int

    @validator('isbn')
    def validate_isbn(cls, isbn):
        '''
        Removes dashes and checks if it's lenght 13 digits.
        '''
        isbn = isbn.replace('-', '')
        if len(isbn) != 13:
            raise ValueError('Incorrect ISBN. Must be 13 digits')
        return isbn

    @validator('year')
    def validate_year(cls, year):
        '''
        Checks if input year in the range 0 - current year.
        '''
        cls.validate_int(year)
        if year < 0 or year > datetime.now().year:
            raise ValueError('Incorrect year')

    @validator('copies')
    def validate_copies(cls, copies):
        '''
        Checks if input copies in the range 0 - 100.
        '''
        cls.validate_int(copies)
        if copies < 0 or copies > 100:
            raise ValueError('Incorrect number of copies')
        return copies

    @classmethod
    def validate_int(cls, value):
        '''
        Checks if input value is integer.
        '''
        try:
            int(value)
        except ValueError:
            raise ValueError('Must be integer')

    @classmethod
    def validate_empty(cls, value):
        '''
        Checks if input value is not empty.
        '''
        if not value.strip():
            raise ValueError('Cannot be empty')
        return value

    @classmethod
    def validate_input(cls, promt: InputPrompts, user_input: str):
        cls.validate_empty(user_input)

        promt_name = promt.name.lower()
        # execute existed validator method based on prompt name
        if promt_name in ['isbn', 'year', 'copies']:
            validator_method = getattr(cls, f'validate_{promt.name.lower()}')
            validator_method(user_input)
