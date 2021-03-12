
def romanNumeralFromValue(value):
    outputNumeral = ""
    if value == 100:
        return "C"
    while value >= 10:
        outputNumeral += "X"
        value -= 10
    while value >= 1:
        outputNumeral += "I"
        value -= 1
    return outputNumeral