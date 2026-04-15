# Text Summarizer

This project produces an "extractive" summary of a text. It does this by
identifying the main words in the text, then scoring each sentence by 
importance based on proportion of main words.

## Requirements and Setup

To run this program, first do `pip install --requirements.txt`. NLTK
requires additional setup to install the required components; do this by
running `python3 nltk_modules.py` once before running the program.

To run the program, simply execute `python3 summarizer.py`.
