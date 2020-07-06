import nltk.data

# Setup
sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")

# Hardcoded word lists
yesnowords = ["can", "could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]


# Take in a tokenized question and return the question type and body
def processquestion(qwords):
    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx + 1:]
    type = "MISC"

    # Determine question type
    if questionword in ["who", "whose", "whom"]:
        type = "PERSON"
    elif questionword == "where":
        type = "PLACE"
    elif questionword == "when":
        type = "TIME"
    elif questionword == "how":
        if target[0] in ["few", "little", "much", "many"]:
            type = "QUANTITY"
            target = target[1:]
        elif target[0] in ["young", "old", "long"]:
            type = "TIME"
            target = target[1:]

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]

    # Return question data
    return (type, target)

question = "Where is Canada?"

print(question)
qwords = nltk.word_tokenize(question.replace('?', ''))
questionPOS = nltk.pos_tag(qwords)
(type, target) = processquestion(qwords)

print(type)