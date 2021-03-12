valueToRomanMappings = {"M" : 1000,
                        "D" : 500,
                        "C" : 100,
                        "L" : 50,
                        "X" : 10,
                        "IX" : 9,
                        "V" : 5,
                        "IV" : 4,
                        "I" : 1}


def fromValue(value):
    outputNumeral = ""
    for romanNumeral, mappedValue in valueToRomanMappings.items():
        while value >= mappedValue:
            outputNumeral += romanNumeral
            value -= mappedValue
    return outputNumeral
