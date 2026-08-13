import string
import secrets


def generate_password(
    length,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):

    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError(
            "At least one character type must be selected."
        )

    if length < 8:
        raise ValueError(
            "Password length must be at least 8."
        )

    password = ""

    for _ in range(length):
        password += secrets.choice(characters)

    return password


def test_password_length():

    password = generate_password(12)

    assert len(password) == 12


def test_minimum_password_length():

    password = generate_password(8)

    assert len(password) == 8


def test_password_with_uppercase():

    password = generate_password(
        12,
        use_uppercase=True,
        use_lowercase=False,
        use_numbers=False,
        use_symbols=False
    )

    assert all(
        char in string.ascii_uppercase
        for char in password
    )


def test_password_with_numbers():

    password = generate_password(
        12,
        use_uppercase=False,
        use_lowercase=False,
        use_numbers=True,
        use_symbols=False
    )

    assert all(
        char in string.digits
        for char in password
    )


def test_password_invalid_length():

    try:

        generate_password(5)

        assert False

    except ValueError:

        assert True


def test_password_no_character_types():

    try:

        generate_password(
            10,
            False,
            False,
            False,
            False
        )

        assert False

    except ValueError:

        assert True