# FEYZA OZKEFE
# Spelling Corrector with Functions

import re
from collections import Counter
from sklearn import metrics

print("Welcome to the spell corrector")
dictionaryFile = input("Please enter the dictionary file: ")


def tokens(text):
    return re.findall(r'\w+', text.lower())


WORDS = Counter(tokens(open(dictionaryFile).read()))


def P(word, N=sum(WORDS.values())):
    """Probability of `word`."""
    return WORDS[word] / N


def correction(word):
    """Most probable spelling correction for word."""
    return max(candidates(word), key=P)


def candidates(word):
    """Generate possible spelling corrections for word."""
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words):
    """The subset of `words` that appear in the dictionary of WORDS."""
    return set(w for w in words if w in WORDS)


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def readTextFile(textFileName):
    with open(textFileName) as f:
        return f.read().split()


def readCorrectTextFile(CorrectTextFileName):
    with open(CorrectTextFileName) as f:
        return f.read().split()


def spellCorrector(wordList):
    correctedWords = []
    for i in range(0, len(wordList)):
        correctedWords.append(correction(wordList[i]))
    return correctedWords


# Prints the corrected words in the text file(not neccassary for the assg)
def printCorrected(corrected):
    print("Corrected words are:")
    for word in corrected:
        print(word)


def writeTextFile(corrected):
    with open('correct.txt', 'w') as f:
        for word in corrected:
            f.write("%s\n" % word)


def main():
    textFile = input("Please enter the text file: ")
    textList = readTextFile(textFile)
    print("length of text file:", len(textList))
    correctedList = spellCorrector(textList)
    writeTextFile(correctedList)
    print("File saved successfully.")
    correctFile = input("Please enter the correct word list file for accuracy: ")
    correctList = readCorrectTextFile(correctFile)

    # Calculate the accuracy score: score
    accuracy_tfidf = metrics.accuracy_score(correctList, correctedList)
    print("Accuracy score is: ", accuracy_tfidf)


main()
