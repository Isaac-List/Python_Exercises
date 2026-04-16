"""
Program to summarize a text by keeping sentences which hold a high number
of significant words and fewer stop words.
"""

import re, statistics, argparse

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

def tokenize_text(text: str) -> list:
    """
    Produce a list of tokens - alphanumeric words of length >= 1
    Excludes punctuation, values in all-lowercase
    """
    return re.findall(r'\w+', text.lower())

def build_frequency_map(wordlist: list) -> dict:
    """
    Produce a dictionary where keys are words which appear in the
    source text excluding stop words, and values are a count of
    that word.
    """
    frequency_map = dict()
    stop_words = set(stopwords.words("english"))

    # Build the frequency map
    for word in wordlist:
        if word not in stop_words:
            if word in frequency_map:
                frequency_map[word] += 1.0
            else:
                frequency_map[word] = 1.0

    # If text is all stop words, return empty dict
    if not frequency_map:
        return {}

    # Normalize to 1.0 max value
    max_count: int = max(frequency_map.values())
    for word in frequency_map:
        frequency_map[word] /= max_count

    return frequency_map

def score_sentence(text: str, frequency_map: dict) -> float:
    """
    Score a sentence (or other text snippet) by totalling the "score"
    of each word it contains, returning a single numerical value
    """
    total_score: float = 0.0
    tokenized_text: list = tokenize_text(text)
    
    # Build score, handle KeyError for stopwords by adding 0
    for word in tokenized_text:
        try:
            total_score += frequency_map[word]
        except KeyError:
            total_score += 0

    # Make score proportional to sentence length
    average_score: float = total_score / len(tokenized_text)

    return average_score

def summarizer(text: str, frequencies: dict) -> str:
    """
    Splits text into sentences (using nltk) and scores each sentence
    based on count of words in the frequency_map; scores kept in parallel
    list. Once scored, sentences are added to a final return string if
    they clear a specified score.
    """
    # Remove newline characters and any extra spaces
    text_no_newlines: str = re.sub(r'\n\s*', " ", text)

    # Tokenize the sentences using nltk
    sentences_list = sent_tokenize(text_no_newlines)

    # score sentences in parallel list
    score_list = [score_sentence(sentence, frequencies) for sentence in sentences_list]

    # Debugging
    # for i in range(len(score_list)):
    #     print(f"{sentences_list[i]} = {score_list[i]}")
    
    # Rebuild text with only sentences of higher than median importance
    summarized_text_list: list = []
    median_score: int = statistics.median(score_list)

    for idx in range(len(score_list)):
        if score_list[idx] >= median_score:
            summarized_text_list.append(sentences_list[idx])

    return " ".join(summarized_text_list)

if __name__ == "__main__":
    # Sample text
    sample: str = """
        There is a flower within my heart
        Daisy, Daisy!
        Planted one day by a glancing dart
        Planted by Daisy Bell!

        Whether she loves me or loves me not
        Sometimes it's hard to tell;
        Yet I am longing to share the lot
        Of beautiful Daisy Bell!

        Daisy, Daisy
        Give me your answer, do!
        I'm half crazy
        All for the love of you!
        It won't be a stylish marriage
        I can't afford a carriage
        But you'll look sweet
        Upon the seat
        Of a bicycle built for two.

        We will go tandem as man and wife
        Daisy, Daisy
        Wheeling away down the road of life
        I and my Daisy Bell!
        When the night's dark
        We can both despise
        Policemen and lamps as well;
        There are bright lights in the dazzling eyes
        Of beautiful Daisy Bell!

        Daisy, Daisy
        Give me your answer, do!
        I'm half crazy
        All for the love of you!
        It won't be a stylish marriage
        I can't afford a carriage
        But you'll look sweet
        Upon the seat
        Of a bicycle built for two.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Use extractive summarization to summarize a source text"
    )
    
    parser.add_argument(
        "filepath",
        type = str,
        help = "Path to the source .txt file"
    )
    
    # Accept optional output_file argument with flags, defaults to model.json
    parser.add_argument(
        "-o",
        "--output",
        type = str,
        default = "summary.txt",
        help = "Location of summary output (default to summary.txt)"
    )

    args = parser.parse_args()

    # Read in text, or fall back to sample text
    try:
        with open(args.filepath, "r", encoding="utf-8") as source:
            source_text = source.read()
    except FileNotFoundError:
        print(f"Error: File {args.filepath} could not be read. Defaulting to sample text.")
        source_text = sample

    list_of_words: list = tokenize_text(source_text)

    freq_map: dict = build_frequency_map(list_of_words)

    print(summarizer(sample, freq_map))
