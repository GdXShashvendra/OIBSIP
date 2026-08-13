from datetime import datetime


def format_message(
    username,
    message,
    timestamp
):

    return (
        f"[{timestamp}] "
        f"{username}: "
        f"{message}"
    )


def validate_username(username):

    return (
        username is not None
        and username.strip() != ""
    )


def validate_message(message):

    return (
        message is not None
        and message.strip() != ""
    )


def test_message_format():

    result = format_message(
        "Alice",
        "Hello Bob",
        "14:35"
    )

    assert result == (
        "[14:35] Alice: Hello Bob"
    )


def test_username_validation():

    assert validate_username(
        "Alice"
    ) is True


def test_empty_username():

    assert validate_username(
        ""
    ) is False


def test_message_validation():

    assert validate_message(
        "Hello"
    ) is True


def test_empty_message():

    assert validate_message(
        ""
    ) is False


def test_whitespace_message():

    assert validate_message(
        "   "
    ) is False


def test_timestamp_format():

    timestamp = datetime.now().strftime(
        "%H:%M"
    )

    assert len(timestamp) == 5
    assert timestamp[2] == ":"