from app.start import on_startup
from app.library_manager import add_book



def main():
    library = on_startup()
    add_book(library)

if __name__ == '__main__':
    main()
