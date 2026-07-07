from mood_analyzer import MoodAnalyzer

m = MoodAnalyzer()

tests = [
    'I love this class',                            # positive
    'This is a terrible day',                        # negative
    'I am not happy about this',                     # negation → negative
    'Not bad at all',                                # negation → positive
    'Just got the offer 🎉🎉🎉',                    # emoji → positive
    'Kind of a rough day 😔',                        # emoji → negative
    'Lowkey stressed but kind of proud of myself',   # mixed? proud missing
    'It is what it is',                              # neutral
    'I love this but I also hate it',                # mixed!
]

for t in tests:
    print(m.explain(t))
    print()