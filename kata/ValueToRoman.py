
def romanNumeralFromValue(value):
    outputNumeral = ""
    if value == 200:
        return "CC"
    elif value >= 100:
        outputNumeral += "C"
        value -= 100
    while value >= 10:
        outputNumeral += "X"
        value -= 10
    while value >= 1:
        outputNumeral += "I"
        value -= 1
    return outputNumeral