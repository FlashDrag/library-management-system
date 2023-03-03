# Testing

## Contents

- [Manual Testing](#manual-testing)
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
- [x] Each value is validated and if the value is invalid, the app asks to enter the value again.
- [x] If the value is valid, the book is searched for in the `stock` worksheet by the selected field and validated value.
- [x] If the books are found, they are displayed in tabular format and the app asks to select a book to add copies to.
- [x] If the book is not found, the app asks to enter the rest book details manually (isbn, title, author, genre, year and number of copies) and skip the first entered field as it saved in the Book object.
- [x] Seleted book displayed in tabular format and the app asks to enter the number of copies to add.
- [x] If the number of copies is invalid, the app notifies that and prompts to enter the number of copies again.
- [x] If the number of copies is valid, the book is added to the `stock` worksheet and the updated book is displayed in tabular format.
- [x] If the book with the same `ISBN` found in the `stock` worksheet, the book is immediately displayed and app asks to select the book to add copies to.
- [x] If the initial selected field was `ISBN` and book not found, the app asks to enter the rest book details manually (title, author, genre, year and number of copies) and the app does not check other fields in the `stock` worksheet as the `ISBN` is unique and other fields can be the same.
- [x] The Book successfully added to the `stock` worksheet and the updated book is displayed in tabular format.
- [x] The app prompts to enter any key to return to the main menu.
- [x] The app returns to the main menu.
<!-- - [x] ... -->

#### Remove book
<!-- - [x] Navigate to the `Remove book` menu by entering code `2` -->

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