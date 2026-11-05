import pytest

from app.services.validation import normalize_name, normalize_phone


@pytest.mark.parametrize("raw, expected", [
    ("יעקב", "יעקב"),
    ("  יעקב   כהן ", "יעקב כהן"),
    ("John Smith", "John Smith"),
    ("בן-דוד", "בן-דוד"),
    ("O'Brien", "O'Brien"),
    ("ז'קלין", "ז'קלין"),
])
def test_valid_names(raw, expected):
    assert normalize_name(raw) == expected


@pytest.mark.parametrize("raw", [
    "",
    "   ",
    "א",
    "--",
    "יעקב123",
    "<script>",
    "א" * 41,
])
def test_invalid_names(raw):
    assert normalize_name(raw) is None


@pytest.mark.parametrize("raw", [
    "0501234567",
    "050-1234567",
    "050 123 4567",
    "(050) 123-4567",
    "+972501234567",
    "+972-50-123-4567",
    "972501234567",
])
def test_valid_phones_are_normalized(raw):
    assert normalize_phone(raw) == "0501234567"


@pytest.mark.parametrize("raw", [
    "",
    "050123456",      # too short
    "05012345678",    # too long
    "031234567",      # landline
    "0601234567",     # not 05X
    "05O1234567",     # letter O instead of zero
    "abc",
])
def test_invalid_phones(raw):
    assert normalize_phone(raw) is None
