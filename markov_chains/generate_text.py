import markov, argparse

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Generate text using a Markov chain from a source file."
)

parser.add_argument(
    "source",
    type = str,
    help = "Path to the source .json file"
)

# Accepet an optional max_length argument with flags, default to 100
parser.add_argument(
    "-l",
    "--length",
    type = int,
    default = 100,
    help = "Maximum length of generated text (default: 100)"
)

# Accept optional output_file argument with flags, defaults to output.txt
parser.add_argument(
    "-o",
    "--output",
    type = str,
    default = "output.txt",
    help = "Location of output text (default output.txt)"
)

args = parser.parse_args()

# Load model
print(f"Loading model from {args.source}")
model, starts = markov.load_chain_model(args.source)

# Generate text and save to file
print(f"Generating text with length of {args.length}")
generated_text = markov.generate_text_from_chain(model, starts, args.length)

# Save generated text to file
print(f"Saving output to {args.output}")
try:
    with open(args.output, "w") as output_file:
        output_file.write(generated_text)
    print(f"Output successfully saved to {args.output}")
except:
    print("Error occured, saving unsuccessful")
