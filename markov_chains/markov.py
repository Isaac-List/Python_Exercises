"""
Markov chain text generator. Inspired by Markovify and a blog
post on healycodes.com. Reimplemented on my own with some references
to learn the process myself. Probably a bit worse and less flexible
but I learned some new things making this! :)
"""

import re, random, json, ast, argparse

def tokenize_text(text: str) -> list:
    """
    Produce a list of tokens, which are either alphanumeric
    words or punctuation marks (this regex builds a list)
    """
    return re.findall(r'\w+|[^\w\s]', text)

def detokenize(tokens: list) -> str:
    """Join list text and clean up punctuation spacing"""
    initial_result: str = " ".join(tokens)

    # Remove spaces before punctuation marks (word . -> word.)
    final_result: str = re.sub(r'\s+([,.!?:;\'])', r'\1', initial_result)
    return final_result
    
def build_markov_chain_model(source_text: str, depth = 2) -> tuple[dict, list]:
    """
    Build the markov chain model using a cleaned source text
    and the provided depth. If no depth provided, use 2.

    The model is created as chain as dict with keys of word
    tuples the length of depth and values a dictionary of next
    words as keys and count of that occurance as values
    """
    # Create list of words and punctuation marks
    words: list = tokenize_text(source_text)

    # Create model, accounting for index out-of-range
    chain_links: dict = {}
    for i in range(len(words) - depth):
        current_state: tuple[str, ...] = tuple(words[i:i + depth])
        next_word: str = words[i + depth]

        # Create new entry if needed, else increment
        if current_state not in chain_links:
            chain_links[current_state] = {next_word: 1}
        elif next_word not in chain_links[current_state]:
            chain_links[current_state][next_word] = 1
        else:
            chain_links[current_state][next_word] += 1

    # Build a list of tuples which are capitalized to use as "starts"
    # Tuple's first token should be a capitalized word (link[0][0] is
    # the first letter of the first word, link[0] is the first word)
    capitalized_starts: list = [
        link for link in chain_links.keys()
        if link[0][0].isupper() and link[0].isalpha()
    ]

    return chain_links, capitalized_starts

def save_chain_model(chain: dict, starts: list, filename: str) -> None:
    """Save the model to a JSON file"""
    serializable_data: dict = {}
    for key, value in chain.items():
        # Converts tuples to string keys for storage
        serializable_data[str(key)] = value

    # Dictionary "bundle" for model and starting tuples list
    save_to_json: dict = {"model": serializable_data, "starts": starts}

    try:
        with open(filename, 'w') as output_file:
            json.dump(save_to_json, output_file, indent = 4)
        print(f"Chain model saved to {filename}")
    except:
        print(f"Failed to save chain model to {filename}")

def load_chain_model(filename: str) -> tuple[dict, list]:
    """Load a model from a selected filename"""
    with open(filename, 'r') as source_file:
        data = json.load(source_file)

    # Convert string representations of tuples back to tuples
    chain_model: dict = {ast.literal_eval(key): value for key, value in data["model"].items()}

    # Convert list representation of start tuples back into tuples
    starts: list = [tuple(s) for s in data["starts"]]

    return chain_model, starts

def generate_text_from_chain(chain: dict, starts: list, length: int) -> str:
    """
    Generate text using the markov chain model provided.
    Result built as a list of words, returned as a string.
    """
    # Choose starting state from capitalized starts if possible, else
    # choose a random tuple as a starting point
    if starts:
        current_state: tuple[str, ...] = random.choice(starts)
    else:
        current_state: tuple[str, ...] = random.choice(list(chain.keys()))
    previous_state: tuple[str, ...] = current_state
    
    # List to be joined and returned as resulting text
    generated_text: list = list(current_state)

    for i in range(length - len(current_state)):
        # Check to see if current window of words is a state,
        # if it's not use the previous state and choose another word
        # if that doesn't work, choose a random state
        if current_state in chain:
            next_word_options: dict = chain[current_state]
            previous_state = current_state
        else:
            try:
                next_word_options = chain[previous_state]
            except KeyError:
                current_state = random.choice(list(chain.keys()))
                next_word_options = chain[current_state]

        # Choose a word considering counts as weights
        next_word: str = random.choices(
            list(next_word_options.keys()),
            weights = list(next_word_options.values()),
            k = 1
        )[0]

        # Move current state forward one word
        current_state = current_state[1:] + (next_word,)

        # Add word to the generated list
        generated_text.append(next_word)

    # End on a . ? or ! to produce text <= target length
    ending_chars = {".", "?", "!"}

    # Search backwards through generated_text to find last ending_char
    idx = len(generated_text) -1
    trimmed_text = generated_text
    found = False
    while idx >= 0 and not found:
        if generated_text[idx] in ending_chars:
            # Save trimmed text
            trimmed_text = generated_text[:idx + 1]
            found = True
        idx -= 1
    
    return detokenize(trimmed_text)

if __name__ == "__main__":
    # Accept command line arguments
    parser = argparse.ArgumentParser(
        description="Generate text using a Markov chain from a source file."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the source .txt file"
    )

    # Accepet an optional max_length argument with flags, default to 100
    parser.add_argument(
        "-l",
        "--length",
        type = int,
        default = 100,
        help = "Maximum length of generated text (default: 100)"
    )

    # Accept an optional depth argument with flags, defaults to 2
    parser.add_argument(
        "-d",
        "--depth",
        type = int,
        default = 2,
        help = "Set the depth of the markov chain (default: 2)"
    )
    
    args = parser.parse_args()
    
    # Read in text, or fall back to sample text
    try:
        with open(args.filepath, "r", encoding="utf-8") as source:
            text = source.read()
    except FileNotFoundError:
        print(f"Error: File {args.filepath} could not be read. Defaulting to sample text.")
        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque aliquet quis dolor ac elementum.
        Nam commodo pretium lectus posuere luctus. Aenean volutpat volutpat sem, sed malesuada est. In at
        metus sit amet mi volutpat finibus. Aenean ultrices vel libero sed imperdiet. In id nunc mi.
        Phasellus et ligula ac est scelerisque blandit. Sed id est ex. Pellentesque habitant morbi tristique
        senectus et netus et malesuada fames ac turpis egestas. Duis non vestibulum eros, eu pulvinar augue.
        Curabitur at finibus leo, id vulputate lorem. Duis iaculis tempor quam vitae placerat. Aenean non
        quam erat. Curabitur vitae dolor ut felis aliquet ultricies. Suspendisse potenti. Vestibulum sodales
        nibh sit amet luctus luctus.
        """
    print(f"Generating model with depth of {args.depth}")
    model, cap_starts = build_markov_chain_model(text, args.depth)
    print(f"Generating with length = {args.length}")
    generated_text: str = generate_text_from_chain(model, cap_starts, args.length)
    print(generated_text)
