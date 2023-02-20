from pydantic import BaseModel, validator, conlist, constr


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
