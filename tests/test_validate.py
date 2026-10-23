import pytest

from src.txt_sql.validate.sql_guard import validate

tables = {"Customers"}


def test_validate_limits():
    validated = validate("SELECT * FROM CUSTOMERS", allowed_tables=tables, max_rows=4)
    assert "LIMIT" in validated


def test_validate_command():
    with pytest.raises(TypeError) as err_info:
        validate("DELETE FROM CUSTOMERS WHERE id=1", allowed_tables=tables)
    assert "Only SELECT queries are allowed" in str(err_info.value)


def test_validate_unauthorized():
    with pytest.raises(ValueError) as err_info:
        validate("SELECT * FROM Orders", allowed_tables=tables)
    assert "Access denied for table(s): {'orders'}" in str(err_info.value)


def test_validate_valid():
    validated = validate("SELECT * FROM CUSTOMERS", allowed_tables=tables, max_rows=4)
    assert validated
