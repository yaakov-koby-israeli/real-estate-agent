import re

# Hebrew/English letters, spaces, and the punctuation found in names: ' " ׳ -
NAME_PATTERN = re.compile(r"^[A-Za-zא-ת'\"׳\- ]{2,40}$")
ISRAELI_MOBILE_PATTERN = re.compile(r"^05\d{8}$")


def normalize_name(raw: str) -> str | None:
    """Return a cleaned name, or None if it isn't a valid name."""
    name = " ".join(raw.split())
    if not NAME_PATTERN.match(name):
        return None
    if sum(char.isalpha() for char in name) < 2:
        return None
    return name


def normalize_phone(raw: str) -> str | None:
    """Return an Israeli mobile number as 05XXXXXXXX, or None if it isn't valid."""
    phone = re.sub(r"[\s\-()]", "", raw)
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("972"):
        phone = "0" + phone[3:]
    if not ISRAELI_MOBILE_PATTERN.match(phone):
        return None
    return phone
