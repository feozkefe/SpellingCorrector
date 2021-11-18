import re
from collections import Counter

print("Welcome to the spell corrector")


# dictionaryFile = input("Please enter the dictionary file: ")


def tokens(text):
    return re.findall(r'\w+', text.lower())


WORDS = Counter(tokens(open("ANAHTAR-KELIME.txt").read()))


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


def spellCorrector(wordList):
    correctedWords = []
    for i in range(0, len(wordList)):
        correctedWords.append(correction(wordList[i]))
    return correctedWords


def printCorrected(corrected):
    print("Corrected words are:")
    for word in corrected:
        print(word)


def inputWords(word):
    wordList = []
    words = re.findall(r'\S+', word)
    for i in range(0, len(words)):
        wordList.append(words[i])
    return wordList


def main():
    wrdFromUser = input("Please enter the words to be corrected: ")
    wordList = inputWords(wrdFromUser)
    print("entered word/words: ", wordList)
    correctedList = spellCorrector(wordList)
    printCorrected(correctedList)


main()
