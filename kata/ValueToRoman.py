def romanNumeralFromValue(value):
    outputNumeral = ""
    while value >= 1000:
        outputNumeral += "M"
        value -= 1000
    while value >= 100:
        outputNumeral += "C"
        value -= 100
    while value >= 10:
        outputNumeral += "X"
        value -= 10
    while value >= 1:
        outputNumeral += "I"
        value -= 1
    return outputNumeral
