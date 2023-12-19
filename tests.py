import pytest
from main import BooksCollector

@pytest.fixture
def books_collector():
    return BooksCollector()

# Тест проверки добавления книги
@pytest.mark.parametrize("book_name", ["Книга 1"])
def test_add_new_book(books_collector, book_name):
    books_collector.add_new_book(book_name)
    assert book_name in books_collector.get_books_genre()

# Тест установки жанра книге
@pytest.mark.parametrize("new_genre, result",
                         [("Комедии", True), ("Мультфильмы", True), ("Фантастика", True), ("Ужасы", True), ("Детективы", True), ("Некорректный жанр", False)])
def test_add_genre(books_collector, new_genre, result):
    book_name = "Книга"
    books_collector.add_new_book(book_name)
    books_collector.set_book_genre(book_name, new_genre)
    is_genre_added = books_collector.get_book_genre(book_name) == new_genre
    assert (is_genre_added and result) or (not is_genre_added and not result)

# Тест получения жанра книги
@pytest.mark.parametrize("new_genre, expected_result", [("Фантастика", "Фантастика"), ("Некорректный жанр", "")])
def test_get_book_genre(books_collector, new_genre, expected_result):
    book_name = "Книга"
    books_collector.add_new_book(book_name)
    books_collector.set_book_genre(book_name, new_genre)
    assert books_collector.get_book_genre(book_name) == expected_result

# Тест получения списка книг конкретного жанра
def test_get_books_by_genre(books_collector):
    books_collector.add_new_book("Книга 1")
    books_collector.set_book_genre("Книга 1", "Фантастика")
    books_collector.add_new_book("Книга 2")
    books_collector.set_book_genre("Книга 2", "Фантастика")
    books_collector.add_new_book("Книга 3")
    books_collector.set_book_genre("Книга 3", "Фантастика")
    books_collector.add_new_book("Книга 4")
    books_collector.set_book_genre("Книга 4", "Ужасы")

    genre_books = books_collector.get_books_with_specific_genre("Фантастика")

    assert "Книга 1" in genre_books
    assert "Книга 2" in genre_books
    assert "Книга 3" in genre_books
    assert len(genre_books) == 3

# Тест проверки отсутствия книг с возрастным рейтингом в списке книг для детей
def get_children_books(books_collector):
    books_collector.add_new_book("Книга 1")
    books_collector.get_book_genre("Книга 1", "Детективы")
    books_collector.add_new_book("Книга 2")
    books_collector.get_book_genre("Книга 2", "Ужасы")
    books_collector.add_new_book("Книга 3")
    books_collector.get_book_genre("Книга 3", "Фантастика")
    books_collector.add_new_book("Книга 4")
    books_collector.get_book_genre("Книга 4", "Комедии")
    books_collector.add_new_book("Книга 5")
    books_collector.get_book_genre("Книга 5", "Мультфильмы")

    children_books = books_collector.get_books_for_children()

    assert "Книга 1" not in children_books
    assert "Книга 2" not in children_books
    assert "Книга 3" in children_books
    assert "Книга 4" in children_books
    assert "Книга 5" in children_books

# Тест проверки добавления книги в избранное
def test_add_book_in_favorites(books_collector):
    books_collector.add_new_book("Книга 1")
    books_collector.add_new_book("Книга 2")
    books_collector.add_book_in_favorites("Книга 1")
    books_collector.add_book_in_favorites("Книга 2")
    favorites = books_collector.get_list_of_favorites_books()
    assert "Книга 1" in favorites
    assert "Книга 2" in favorites

# Тест проверки удаления книги из избранного
def test_delete_book_from_favorites(books_collector):
    books_collector.add_new_book("Книга 1")
    books_collector.add_new_book("Книга 2")
    books_collector.add_book_in_favorites("Книга 1")
    books_collector.add_book_in_favorites("Книга 2")
    books_collector.delete_book_from_favorites("Книга 2")
    favorites = books_collector.get_list_of_favorites_books()
    assert "Книга 1" in favorites
    assert "Книга 2" not in favorites

# Тест проверки добавления невалидного названия книги
@pytest.mark.parametrize("invalid_book_name", ['', "a" * 41])
def test_add_invalid_book_name(books_collector, invalid_book_name):
    books_collector.add_new_book(invalid_book_name)
    assert invalid_book_name not in books_collector.get_books_genre()

# Тест проверки добавления несуществующей книги в избранное
def test_add_not_existed_book_in_favorites (books_collector):
    books_collector.add_book_in_favorites("Книга 1")
    favorites = books_collector.get_list_of_favorites_books()
    assert ("Книга 1") not in favorites
