from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, Sentence0),
    Implication(AKnave, Not(Sentence0)),   
)

# Puzzle 1
# A says "We are both knaves."
Sentence1 = And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, Sentence1),
    Implication(AKnave, Not(Sentence1)),
)

# Puzzle 2
# A says "We are the same kind."
Sentence3 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
Sentence4 = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, Sentence3),
    Implication(AKnave, Not(Sentence3)),
    Implication(BKnight, Sentence4),
    Implication(BKnave, Not(Sentence4)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
Sentence5 = Or(AKnight, AKnave)
# B says "A said 'I am a knave'."
Sentence6 = Implication(AKnight, AKnave)
# B says "C is a knave."
Sentence7 = CKnave
# C says "A is a knight."
Sentence8 = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Implication(AKnight, Sentence5),
    Implication(AKnave, Not(Sentence5)),
    Implication(BKnight, Sentence6),
    Implication(BKnave, Not(Sentence6)),
    Implication(BKnight, Sentence7),
    Implication(BKnave, Not(Sentence7)),
    Implication(CKnight, Sentence8),
    Implication(CKnave, Not(Sentence8)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
