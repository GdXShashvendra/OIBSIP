def calculate_bmi(weight, height):
    return weight / (height ** 2)


def classify_bmi(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def test_bmi_calculation():

    bmi = calculate_bmi(70, 1.75)

    assert round(bmi, 2) == 22.86


def test_underweight():

    assert classify_bmi(17.5) == "Underweight"


def test_normal():

    assert classify_bmi(22) == "Normal"


def test_overweight():

    assert classify_bmi(27) == "Overweight"


def test_obese():

    assert classify_bmi(32) == "Obese"


def test_bmi_boundary_normal():

    assert classify_bmi(18.5) == "Normal"


def test_bmi_boundary_overweight():

    assert classify_bmi(25) == "Overweight"


def test_bmi_boundary_obese():

    assert classify_bmi(30) == "Obese"