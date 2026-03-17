"""This is an example test file to demonstrate various assertion methods in pytest."""
import pytest


def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("123", int)


def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'world') is False


def test_type():
    assert type("hello" is str)
    assert type("world" is not int)


def test_grater_and_less_than():
    assert 5 > 3
    assert 2 < 4


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 6 not in num_list
    assert all(num_list)
    assert not any(any_list)


class Student:
    """
    This is a simple Student class to demonstrate testing of class attributes and initialization.
    """

    def __init__(self, firs_name: str, last_name: str, major: str, years: int):
        self.firs_name = firs_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    """
        This fixture provides a default Student instance for testing purposes.
    :return: A Student instance with predefined attributes.
    """
    return Student("John", "Doe", "Computer Science", 3)


def test_person_initialization(default_employee):

    assert default_employee.firs_name == "John", 'First name should be "John"'
    assert default_employee.last_name == "Doe", 'Last name should be "Doe"'
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3
