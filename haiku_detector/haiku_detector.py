import syllables, re

def detect_haiku(candidate: str) -> str:
	"""Detect and format haiku from text"""
	# Clean text
	cleaned_text: str = re.sub(r'[^\w\s]', '', candidate)

	# Make list of words
	words: list = cleaned_text.split()

	# Make list of syllable counts for each word
	counts = []
	for word in words:
		counts.append(syllables.estimate(word))
	
	# Check Haiku status
	if sum(counts) != 17:
		return "Not a Haiku"

	# Attempt to build Haiku line-by-line
	line_1 = []
	line_2 = []
	line_3 = []
	current_syllable_count: int = 0

	# Iterate through the list of words
	for i, word in enumerate(words):
		current_syllable_count += counts[i]

		if current_syllable_count <= 5:
			line_1.append(word)
		elif current_syllable_count <=12:
			line_2.append(word)
		elif current_syllable_count <=17:
			line_3.append(word)

		# Check to see if this word put a line over-length
		if current_syllable_count > 5 and len(line_2) == 0:
			return "Not a Haiku"
		elif current_syllable_count > 12 and len(line_3) == 0:
			return "Not a Haiku"		

	return f"{' '.join(line_1)}\n{' '.join(line_2)}\n{' '.join(line_3)}"

if __name__ == "__main__":
    print("Examples\n--------")
    print(f"Hello World\n{detect_haiku('Hello World')}")
    print()
    print(f"The cold winter wind blows through the naked branches of the tall oak tree\n{detect_haiku('The cold winter wind blows through the naked branches of the tall oak tree.')}")
	
