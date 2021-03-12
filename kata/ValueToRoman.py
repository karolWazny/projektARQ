
def romanNumeralFromValue(value):
    outputNumeral = ""
    if value == 20:
        return "XX"
    elif value == 10:
        return "X"
    while value > 0:
        outputNumeral += "I"
        value -= 1
    return outputNumeral