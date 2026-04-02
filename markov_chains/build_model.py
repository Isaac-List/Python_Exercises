import markov, argparse

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Build a markov chain text model from a source text"
)

parser.add_argument(
    "source",
    type = str,
    help = "Path to the source .txt file"
)

# Accept optional output_file argument with flags, defaults to model.json
parser.add_argument(
    "-o",
    "--output",
    type = str,
    default = "model.json",
    help = "Location of model's save file (default model.json)"
)

# Accept optional depth argument with flags, defaults to 2
parser.add_argument(
    "-d",
    "--depth",
    type = int,
    default = 2,
    help = "Depth of the model (default 2)"
)

args = parser.parse_args()

# Open File
with open(args.source, "r", encoding = "utf-8") as source:
    text_list = source.readlines()

# Cap text at 100,000 lines for performance
if len(text_list) > 100000:
    text = "".join(text_list[:100000])
else:
    text = "".join(text_list)
print(f"{args.source} successfully read")

# Build Model
print(f"Building model with depth of {args.depth}")
model, cap_starts = markov.build_markov_chain_model(text, args.depth)
markov.save_chain_model(model, cap_starts, args.output)
