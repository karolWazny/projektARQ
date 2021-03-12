def fromValue(value):
    outputNumeral = ""
    while value >= 1000:
        outputNumeral += "M"
        value -= 1000
    while value >= 500:
        outputNumeral += "D"
        value -= 500
    while value >= 100:
        outputNumeral += "C"
        value -= 100
    while value >= 50:
        outputNumeral += "L"
        value -= 50
    while value >= 10:
        outputNumeral += "X"
        value -= 10
    while value >= 5:
        outputNumeral += "V"
        value -= 5
    while value >= 1:
        outputNumeral += "I"
        value -= 1
    return outputNumeral
