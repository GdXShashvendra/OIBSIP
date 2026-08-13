def test_greeting():
    response = "Hello! How can I help you?"
    assert "Hello" in response


def test_time_format():
    time_value = "14:35"
    assert len(time_value) == 5
    assert time_value[2] == ":"


def test_date_format():
    date_value = "13-08-2026"
    assert len(date_value) == 10
    assert date_value[2] == "-"
    assert date_value[5] == "-"


def test_search_query():
    query = "Python programming"
    assert query.strip() != ""