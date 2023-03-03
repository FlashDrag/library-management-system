import logging
from datetime import datetime
from dateutil.parser import parse
from dateutil.parser import ParserError
import re

import gspread as gs
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

from library_system.models.worksheets_cfg import WorksheetSets, WorksheetSet
from library_system.models.book import Book, BookFields, BorrowFields

logger = logging.getLogger(__name__)


class Library:
    '''
    Library class that connects to a Google Sheet and provides methods to interact with it.

    Class attributes:
    :param `SCOPE`: Google API scope.

    Instance attributes:
    :param `sheet_name`: Name of the Google Sheet.
    :param `creds_path`: Path to credentials file.

    :param `_SHEET`: `Spreadsheet` instance.
    :param `isConnected`: indicates if the Library is connected to the Google Sheet.
    '''

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        self._sheet_name = sheet_name
        self._creds_path = creds_path

        self.s_sheet: gs.Spreadsheet | None = None
        self.isConnected: bool = False

    def connect(self) -> None:
        '''
        Connect to the Google Sheet specified in the `sheet_name` parameter,
        using the credentials in the file at `creds_path`.
        - Create `s_sheet` attr as a `Spreadsheet` instance of the Google Sheet
        - Set `isConnected` attr to `True` if the connection is successful
        '''
        try:
            scope = Credentials.from_service_account_file(
                self._creds_path, scopes=self.SCOPE)
            client = gs.authorize(scope)
            self.s_sheet = client.open(self._sheet_name)
            self.isConnected = True
        except FileNotFoundError:
            logger.error(f'Credentials file not found at {self._creds_path}.')
        except GoogleAuthError:
            logger.error(
                'GoogleAuthError: Check your credentials or try again later.')
        except gs.exceptions.SpreadsheetNotFound:
            logger.error(f'Spreadsheet {self._sheet_name} not found!')
        except gs.exceptions.GSpreadException as e:
            logger.error(e)
        except Exception as e:
            # catch-all Exception block is still included to handle any unexpected errors that may occur
            logger.error(f"An unexpected error occurred: {type(e)}: {e}")

    def set_worksheets(self, w_sets: list[WorksheetSets]) -> None:
        '''
        Sets worksheets for the `Library` instance.
        Add new worksheets to the `Google Spreadsheet`
        if they don't exist based on `WorksheetSet` parameters of `w_sets` list.

        Creates `gspread.Worksheet` instances for each `Google Worksheet`
        and adds them to the apropriated `WorksheetSet` dicts as `w_sheet` parameter.

        :param w_sets: list of `WorksheetSets` enums containing the `WorksheetSet` dicts
        '''
        if self.s_sheet is None:
            raise gs.exceptions.GSpreadException(
                'Spreadsheet is not connected.')

        # get the list of worksheets titles from the google spreadsheet
        google_sheet_titles = list(
            map(lambda sheet: sheet.title, self.s_sheet.worksheets()))

        for w_set in w_sets:
            title = w_set.value['title']
            headers = w_set.value['fields']

            if title not in google_sheet_titles:
                worksheet = self.s_sheet.add_worksheet(
                    title, rows=100, cols=len(headers)
                )
            else:
                worksheet = self.s_sheet.worksheet(title)

            # update the first row with the headers
            worksheet.update('A1', [headers])
            # set gspread Google worksheet instance to `WorksheetSet` dict to `w_sheet` parameter
            w_set.value['w_sheet'] = worksheet

    def search_books(self, book_value: str, book_field: BookFields | BorrowFields, w_set: WorksheetSet) -> list[dict]:
        # TODO: exlude worksheet header row from search
        '''
        Search a book value with the specified worksheet header - `book_field` and
        in the specified worksheet - `w_set`.

        :param `book_value`: validated book value search for.
        :param `book_field`: The worksheet header to search by.
        :param `w_set`: The worksheet to search in.

        :return: A list of dictionaries containing the book details.

        Example return:
        [{'isbn': '9781449357351', 'title': 'Python Cookbook', 'author': 'David Beazley, Brian K. Jones',
         'genre': 'Computers', 'year': '2013', 'copies': '16', 'cell_row': 84},]
        '''

        worksheet = w_set['w_sheet']
        # get the name of the enum value, which is the same as the header name
        field = book_field.name

        if worksheet is None:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )

        # get the column number of the header
        header: gs.Cell | None = worksheet.find(
            field, in_row=1, case_sensitive=False
        )
        if header is None:
            raise ValueError(
                f"Can't to find the header <{field}> in the worksheet <{w_set['title']}>"
            )
        col_num = header.col

        # find all cells with the specified value in the column of the header
        if book_field.name in (
                BookFields.title.name, BookFields.author.name, BookFields.genre.name, BorrowFields.borrower_name.name):
            # match the value substring
            regex = re.compile(rf'.*{book_value}.*', re.IGNORECASE)
        else:
            # match the exact value
            regex = re.compile(rf'^{book_value}$', re.IGNORECASE)
        matched_cells: list[gs.Cell] = worksheet.findall(
            regex, in_column=col_num, case_sensitive=False
        )

        # create a list of dictionaries containing the book details
        headers = w_set['fields']
        result_list = []
        for cell in matched_cells:
            # skip the header row
            if cell.row == 1:
                continue
            value_list = worksheet.row_values(cell.row)
            value_dict = dict(zip(headers, value_list))
            value_dict['cell_row'] = cell.row
            result_list.append(value_dict)

        return result_list

    def add_book_copies(self, book_to_add: dict, w_set: WorksheetSet, copies_to_add: int) -> dict:
        '''
        Add copies to the existing book in the stock worksheet.

        :param book_to_add: A dictionary containing the book details.
        :param w_set: The `WorksheetSet` to add the book copies to.
        :param copies_to_add: The number of copies to add.
        :return: Dictionary containing a book with updated number of copies.
        '''
        w_sheet = w_set['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )
        cell_row = book_to_add.get('cell_row')
        if not cell_row:
            raise ValueError(
                f"Can't to find the cell row <{cell_row}> in the worksheet <{w_set['title']}>"
            )
        current_copies = book_to_add.get(BookFields.copies.name)
        if not current_copies or not current_copies.isdigit():
            new_num_copies = copies_to_add
        else:
            new_num_copies = int(current_copies) + copies_to_add
        field = 'copies'
        header = w_sheet.find(
            field, in_row=1, case_sensitive=False
        )
        if not header:
            raise ValueError(
                f"Can't to find the header <{field}> in the worksheet <{w_set['title']}>"
            )
        col_num = header.col

        w_sheet.update_cell(cell_row, col_num, new_num_copies)
        book_to_add[BookFields.copies.name] = new_num_copies
        return book_to_add

    def append_book(self, book: Book | dict, w_set: WorksheetSet):
        '''
        Append a book to the worksheet.
        Will be added only the fields specified in the given `WorksheetSet`.

        :param book: A `Book` model instance.
        :param w_set: The `WorksheetSet` to append the book to.
        :return: A dictionary containing the book details.
        '''
        w_sheet = w_set['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Failed to connect worksheet <{w_set['title']}>"
            )
        fields = w_set['fields']
        if isinstance(book, Book):
            # create a dictionary from Book model values,
            # containing only the fields specified in the given `WorksheetSet`
            book_to_add = book.dict(include=set(fields))
            if not book_to_add:
                raise ValueError(
                    f"Can't to add an empty book to the worksheet <{w_set['title']}>"
                )
        elif isinstance(book, dict):
            book_to_add = book
        book_to_add.setdefault('copies', 1)  # add copies field if not exists
        # get the values of the book dictionary in the same order as the headers in the worksheet
        values = [book_to_add.get(field) for field in fields]
        w_sheet.append_row(values)
        return book_to_add

    def remove_book(
            self, book_to_remove: dict, w_set: WorksheetSet, copies_to_remove: int = 1, totally: bool = False
    ) -> dict | None:
        '''
        Remove a book from the worksheet.

        :param book_to_remove: A dictionary containing the book details.
        :param w_set: The `WorksheetSet` to remove the book from.
        :param copies_to_remove: The number of copies to remove.
        :param totally: If `True` the book row will be removed from the worksheet.
        :return: A dictionary containing the updated book details or None if book totally deleted
        '''
        w_sheet = w_set['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )
        cell_row = book_to_remove['cell_row']
        current_copies = book_to_remove.get(BookFields.copies.name)
        if totally or not current_copies or not current_copies.isdigit():
            w_sheet.delete_row(cell_row)
            return None

        new_num_copies = int(current_copies) - copies_to_remove
        if new_num_copies <= 0:
            w_sheet.delete_row(cell_row)
            return None

        field = 'copies'
        header = w_sheet.find(
            field, in_row=1, case_sensitive=False
        )
        if not header:
            raise ValueError(
                f"Can't to find the header <{field}> in the worksheet <{w_set['title']}>"
            )
        col_num = header.col

        w_sheet.update_cell(cell_row, col_num, new_num_copies)
        book_to_remove[BookFields.copies.name] = new_num_copies
        return book_to_remove

    def check_out_book(self, book_to_check_out: dict):
        '''
        Check out a book from the library stock.

        :param book_to_check_out: A dictionary containing the book details.
        :return: A dictionary containing the updated book details.
        '''
        stock_set = WorksheetSets.stock.value
        borrowed_set = WorksheetSets.borrowed.value

        # add a book to the borrowed worksheet with the borrower's details
        self.append_book(book_to_check_out, borrowed_set)

        # remove a single copy of the book from the library stock
        upd_book = self.remove_book(book_to_check_out, stock_set)

        return upd_book

    def return_book(self, book_to_return: dict) -> dict:
        '''
        Return a book to the library stock and remove it from the borrowed worksheet.

        :param book_to_return: A dictionary containing the book details.
        :return: A dictionary containing the updated book details.
        '''
        book_field = BookFields.isbn
        book_value = book_to_return.get(book_field.name)
        w_set = WorksheetSets.stock.value
        if not book_value:
            raise ValueError(
                f"Can't to find the book value {book_field.name} in book_to_return dict"
            )
        found_books = self.search_books(book_value, book_field, w_set)
        if len(found_books) > 0:
            upd_book = self.add_book_copies(found_books[0], w_set, 1)
        else:
            upd_book = self.append_book(book_to_return, w_set)

        # remove the book from the borrowed worksheet
        self.remove_book(
            book_to_return, WorksheetSets.borrowed.value, totally=True)

        return upd_book

    def get_overdue_borrowers(self) -> list[dict]:
        '''
        Get a list of overdue borrowers.

        :return: A list of dictionaries containing the overdue borrowers details.
        '''
        w_set = WorksheetSets.borrowed.value
        w_sheet = w_set['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )

        overdue_borrowers = w_sheet.get_all_records(head=1)
        # add the cell row number to each book dictionary
        overdue_borrowers_with_cell_row = [
            {**book, 'cell_row': i + 2} for i, book in enumerate(overdue_borrowers)
        ]

        # filter out the books that are overdue
        today = datetime.today()
        overdue_borrowers = []
        for book in overdue_borrowers_with_cell_row:
            due_date = book.get(BorrowFields.due_date.name)
            if due_date and isinstance(due_date, str):
                try:
                    # convert the due date string to a date object
                    due_date = parse(due_date, dayfirst=True)
                except (ParserError, ValueError, OverflowError):
                    continue
                else:
                    if due_date < today:
                        overdue_borrowers.append(book)
        # sort the overdue borrowers by due date (ascending)
        sorted_borrowers = sort_data(
            BorrowFields.due_date.name, overdue_borrowers)
        return sorted_borrowers

    def get_library_stock(
            self,
            w_set: WorksheetSet,
            field: BookFields | BorrowFields | None = None,
            reverse: bool = False
    ) -> list[dict]:
        '''
        Get the library stock.
        If a field is provided then the stock will be sorted by that field.

        :param w_set: The worksheet set to get the stock from.
        :param field: The field to sort the stock by.
        :param reverse: If `True` the stock will be sorted in descending order.
        :return: A list of dictionaries containing the library stock.
        '''
        w_sheet = w_set['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )
        dicts = w_sheet.get_all_records(head=1)
        # add the cell row number to each book record
        records = [
            {**book, 'cell_row': i + 2} for i, book in enumerate(dicts)
        ]
        order_by = field.name if field else None
        if not order_by:
            return records
        # sort the records by the field
        sorted_records = sort_data(order_by, records, reverse)
        return sorted_records


def sort_data(key: str, records: list[dict], reverse: bool = False) -> list[dict]:
    '''
    Sorts the list of dictionaries by the key value:
    - If key is `date` then sort by date if date valid else put it at the end of the list with the same date string.
    - If key is `isbn`, `copies` or `year` then sort by int value if int valid
    else put it at the end of the list with the same int string.
    - If key is any other string then sort by string value.

    :param key: key to sort by
    :param records: list of dictionaries
    :param reverse: sort in reverse order
    :return: sorted list of dictionaries
    '''
    if key in (BorrowFields.borrow_date.name, BorrowFields.due_date.name):
        def sort_date(d):
            try:
                return parse(d[key], dayfirst=True)
            except (ParserError, ValueError, OverflowError):
                if reverse:
                    return datetime.min
                else:
                    return datetime.max
        # sort by date if date valid else put it at the end of the list with the same date string
        sorted_records = sorted(records, key=sort_date, reverse=reverse)
    else:
        if key in (BookFields.isbn.name, BookFields.copies.name, BookFields.year.name):
            def sort_int(d):
                '''sort by int value'''
                try:
                    return int(d[key])
                except ValueError:
                    if reverse:
                        return float('-inf')  # smallest float
                    else:
                        return float('inf')  # largest float
            sorted_records = sorted(records, key=sort_int, reverse=reverse)
        else:
            # sort by string value
            sorted_records = sorted(
                records, key=lambda d: str(d[key]), reverse=reverse)

    return sorted_records


# for testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':
    from library_system.config import SHEET_NAME, CREDS_PATH

    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')

    library.set_worksheets(list(WorksheetSets))

    # append book
    book = Book(
        isbn='978-3-16-148410-0',
        title='The Lord of the Rings',
        author='J.R.R. Tolkien',
        genre='Fantasy',
        year='2001',
        copies='2',
        borrower_name='John Doe',
        borrow_date='2023-02-25',
        due_date='2023-04-1',
    )
    appended_book = library.append_book(book, WorksheetSets.stock.value)
    print(f'Appended book: {appended_book}')

    # search books
    book = Book(title='Lord of the Rings')
    book_field = BookFields.title
    found_books = library.search_books(
        book[book_field.name], book_field, WorksheetSets.stock.value
    )
    print(
        f'Found books matching the {book_field.value} "{book[book_field.name]}": {found_books}')

    # add book copies
    book_to_add = found_books[0]
    copies = 8
    updated_book = library.add_book_copies(
        book_to_add, WorksheetSets.stock.value, copies
    )
    print(f'Updated book: {updated_book}')

    # remove book copies
    # search
    book = Book(title='Lord of the Rings')
    book_field = BookFields.title
    found_books = library.search_books(
        book[book_field.name], book_field, WorksheetSets.stock.value
    )
    print(
        f'Found books matching the {book_field.value} "{book[book_field.name]}": {found_books}')

    # remove
    book_to_remove = found_books[0]
    copies_to_remove = 20
    removed_book = library.remove_book(
        book_to_remove, WorksheetSets.stock.value, copies_to_remove
    )
    if removed_book:
        print(f'Updated book: {removed_book}')
    else:
        print('Book totally removed')
