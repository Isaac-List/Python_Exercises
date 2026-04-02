# Markov Chain Text Generation

A markov chain based text generating module. Inspired by Markovify and healycodes, probably has
issues here or there but I learned some new math and Python techniques making this :)

## Components
 - markov.py: The main module with function definitions for creating a model, loading/saving a model, and generating text from a model.
 - build_model.py: A script to build a model from a source txt file. Takes arguments for input and output locations and model depth. Saves model to JSON.
 - generate_text.py: A script to generate text using a model file. Takes arguments for input model, output location, maximum text length. Saves output to txt file.

## Purpose
I made this to brush up on Python and practice processing text data. It probably could be used as
part of a larger project, but the intention I had was primarily a learning experience.

#### _Note on AI/LLM Use:_

I also used this project as an opportunity to try using an LLM as a code reviewer. I used Google's Gemini
to review code, and it provided a handful of fixes and suggested improvements.
