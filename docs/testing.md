# Testing

## Contents

- [Manual Testing](#manual-testing)
    - [Application features](#application-features)
        - [Main menu](#main-menu)
        - [Add book](#add-book)
        - [Remove book](#remove-book)
        - [Check out book](#check-out-book)
        - [Return book](#return-book)
        - [Check Overdue borrowers](#check-overdue-borrowers)
        - [View Library Stocks](#view-library-stocks)
- [Automated Unit testing](#automated-unit-testing)
- [Bugs/Issues](#bugsissues)


## Manual Testing

### Application features
- #### Main menu
- [x] The main menu is displayed when the application is started or refreshed.
- #### Add book
- [x] Navigate to the `Add book` menu by entering code `1`
- [x] The `Add book` menu is displayed and provides the following option to search by: `ISBN`, `Title`, `Author`, `Genre`, `Year`.
- [x] Each option is selected by entering the corresponding code number and the app asks to enter the value of the field to search for.
- [x] Each value is validated and if the value is invalid, the app asks to enter the value again:
- ISBN - 13 digits
- Title, Author, Genre - not empty
- Year - digits in range 1 - current year
- [x] If the value is valid, the book is searched for in the `stock` worksheet by the selected field and validated value.
- [x] The application does not look for the value in the first row of the `stock` worksheet as it is the header.
- [x] If the books are found, they are displayed in tabular format and the app asks to select a book to add copies to.
- [x] If the book is not found, the app asks to enter the rest book details manually (isbn, title, author, genre, year and number of copies) and skip the first entered field as it saved in the Book object.
- [x] Seleted book displayed in tabular format and the app asks to enter the number of copies to add.
- [x] If the number of copies is invalid (not a digit or less than 1), the app notifies that and prompts to enter the number of copies again.
- [x] If the number of copies is valid, the book is added to the `stock` worksheet and the updated book is displayed in tabular format.
- [x] If the book with the same `ISBN` found in the `stock` worksheet, the book is immediately displayed and app asks to select the book to add copies to.
- [x] If the initial selected field was `ISBN` and book not found, the app asks to enter the rest book details manually (title, author, genre, year and number of copies) and the app does not check other fields in the `stock` worksheet as the `ISBN` is unique and other fields can be the same.
- [x] The Book successfully added to the `stock` worksheet and the updated book is displayed in tabular format.
- [x] The app prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


#### Remove book
- [x] Navigate to the `Remove book` menu by entering code `2`
- [x] The `Remove book` menu is displayed and provides the following option to search by: `ISBN`, `Title`, `Author`, `Genre`, `Year`.
- [x] Each option is selected by entering the corresponding code number and the app asks to enter the value of the field to search for.
- [x] Each value is validated and if the value is invalid, the app asks to enter the value again:
- ISBN - 13 digits
- Title, Author, Genre - not empty
- Year - digits in range 1 - current year
- [x] If the value is valid, the book is searched for in the `stock` worksheet by the selected field and validated value.
- [x] If the books are found, they are displayed in tabular format and the app asks to select a book to remove.
- [x] If the book is not found, the app notifies that and returns to the field selection menu.
- [x] Seleted book displayed in tabular format and the app asks to enter the number of copies to remove.
- [x] If the number of copies is invalid (not a digit or less than 1), the app notifies that and prompts to enter the number of copies again.
- [x] If the number of copies is valid, the number of copies of the selected book is updated in the `stock` worksheet and the updated book is displayed in tabular format.
- [x] If the number of copies is equal or greater than the number of copies in the `stock` worksheet, the book is removed completely from the `stock` worksheet.
- [x] The app removes the book completely from the `stock` worksheet if the option `Full book` is selected.
- [x] The app prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


#### Check out book
- [x] Navigate to the `Check out book` menu by entering code `3`
- [x] The `Check out book` menu is displayed and provides the following option to search by: `ISBN`, `Title`, `Author`, `Genre`, `Year`.
- [x] Each option is selected by entering the corresponding code number and the app asks to enter the value of the field to search for.
- [x] Each value is validated and if the value is invalid, the app asks to enter the value again:
ISBN - 13 digits, not empty; title, author, genre - not empty; year - digits in range 1 - current year
- [x] When entered value is valid, the book is searched for in the `stock` worksheet by the selected field and validated value.
- [x] If no books matching the search criteria, the app notifies that and returns to the field selection menu.
- [x] All found books are displayed in tabular format and the app asks to select a book to check out.
- [x] Selected book displayed in tabular format and the app asks to enter the borrower name.
- [x] If the borrower name is empty, the app notifies that and prompts to enter the borrower name again.
- [x] If the borrower name is not empty, the app asks to enter the due date in the folowing formats: `dd/mm/yyyy`, `dd-mm-yyyy`, `dd.mm.yyyy`.
- [x] Date is validated using `dateutil.parser.parse` and if the date is invalid, the app notifies that and prompts to enter the due date again.
- [x] If the date is in the past, the app notifies that and prompts to enter the due date again.
- [x] If book copies more than 1, a copy is removed from the `stock` worksheet and added to the `borrowed` worksheet with the borrower name current date and due date.
- [x] Updated book is displayed in tabular format with the number of copies decreased by 1.
- [x] If book copies equal to 1, the book is fully removed from the `stock` worksheet and added to the `borrowed` worksheet with the borrower name current date and due date and the app notifies that the book is completely checked out from the library stock.
- [x] The app prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


#### Return book
- [x] Navigate to the `Return book` menu by entering code `4`
- [x] The `Return book` menu is displayed and provides the following option to search by: `ISBN`, `Title`, `Author`, `Genre`, `Year`, `Borrower name`, `Borrow date`, `Due date`.
- [x] Each option is selected by entering the corresponding code number and the app asks to enter the value of the field to search for.
- [x] Each value is validated and if the value is invalid, the app asks to enter the value again: all fields - not empty; ISBN - 13 digits; year - digits in range 1 - current year; borrow date - not greater than current date; borrow date and due date - in the following formats: `dd/mm/yyyy`, `dd-mm-yyyy`, `dd.mm.yyyy`.
- [x] When entered value is valid, the book is searched for in the `borrowed` worksheet by the selected field and validated value.
- [x] If no books matching the search criteria, the app notifies that and returns to the field selection menu.
- [x] All found books are displayed in tabular format and the app asks to select a book to return.
- [x] When book is selected, it immediately displayed in tabular format and the app searches for the book in the `stock` worksheet by ISBN and if the book is found, the number of copies is increased by 1 and the book is updated in the `stock` worksheet and removed from the `borrowed` worksheet.
- [x] If the book is not found in the `stock`, the book is added to the `stock` worksheet with the number of copies equal to 1 and removed from the `borrowed` worksheet.
- [x] The app notifies that the book is returned and displays the updated book in tabular format with full information including the number of book row in the `stock` worksheet.
- [x] The app prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


#### Check Overdue borrowers
- [x] Navigate to the `Check Overdue borrowers` menu by entering code `5`
- [x] The app checks if there are any overdue books in the `borrowed` worksheet correctly.
- [x] If there are overdue books, the app notifies that and displays the list of overdue books sorted by due date in <em>ascending order</em> in tabular format.
- [x] If there are no overdue books, the app notifies that and prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


#### View Library Stocks
- [x] Navigate to the `View Library Stocks` menu by entering code `6`
- [x] The `viewing library` menu is displayed with the 2 options: `Library stock`, `Borrowed books`.
- [x] Library stock option is presented by entering code `1` and the app displays
7 sorted methods of viewing the library stock: `Spreadsheet order`, `ISBN`, `Title`, `Author`, `Genre`, `Year`, `Number of copies`.
- [x] Each method is selected by entering the corresponding code number and the app displays the library stock sorted by the selected field and selected order in tabular format in the corresponding order.
- [x] If the library stock is empty, the app notifies that and prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.
- [x] Borrowed books option is presented by entering code `2` and the app displays
9 sorted methods of viewing the borrowed books: `Spreadsheet order`, `ISBN`, `Title`, `Author`, `Genre`, `Year`, `Borrower name`, `Borrow date`, `Due date`.
- [x] Each method is selected by entering the corresponding code number and the app displays the borrowed books sorted by the selected field and selected order in tabular format in the corresponding order.
- [x] If the borrowed books are empty, the app notifies that and prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.

[Back to top](#contents)


## Automated testing
<!-- TODO HTML validation -->
<!-- [W3 Markup Validation](https://validator.w3.org/) - HTML Validation -->
<!-- TODO CSS validation -->
<!-- [W3 Jigsaw validation](https://jigsaw.w3.org/css-validator/) - CSS Validation -->
<!-- TODO flake8 -->
<!-- [flake8](https://flake8.pycqa.org/en/latest/) - Python code style: pep8, pyflakes and co -->
<!-- TODO mypy -->
<!-- [mypy](http://mypy-lang.org/) - Optional static typing for Python -->
<!-- TODO PEP8 validation -->
<!-- [PEP8](http://pep8online.com/) - Python code style: pep8 -->
<!-- TODO Unit testing -->
<!-- [Pytest](https://docs.pytest.org/en/stable/) - Unit testing -->
....

[Back to top](#contents)


## Bugs/Issues
...

#### Unresolved
....

### Error handing
<!-- TODO Pydantic Validation -->
- [x] The code intelligently handles empty or invalid data.
- [x] API calls that fail to execute or return data will be handled gracefully, with the site users notified in an obvious way
- [x] All input data is validated.
- [x] Internal errors are handled gracefully, and users are notified of the problem where appropriate.

[Back to top](#contents)

[Back to README.md](https://github.com/FlashDrag/library-management-system/blob/master/README.md#testing)