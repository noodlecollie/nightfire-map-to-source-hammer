import re
import argparse

# This hellish regex matches the Source engine-compatible section of a Nightfire surface descriptor.
# If this matches a line, we keep the matched contents and discard everything after.
SURFACE_DESC_MATCH = r"""
^						# Beginning of the line

\(\s*					# Open bracket for first plane point
-?[0-9]+(\.[0-9]*)?\s+	# X co-ord
-?[0-9]+(\.[0-9]*)?\s+	# Y co-ord
-?[0-9]+(\.[0-9]*)?		# Z co-ord
\s*\)					# Close bracket

\s+						# Whitespace delimiter

\(\s*					# Open bracket for second plane point
-?[0-9]+(\.[0-9]*)?\s+	# X co-ord
-?[0-9]+(\.[0-9]*)?\s+	# Y co-ord
-?[0-9]+(\.[0-9]*)?		# Z co-ord
\s*\)					# Close bracket

\s+						# Whitespace delimiter

\(\s*					# Open bracket for third plane point
-?[0-9]+(\.[0-9]*)?\s+	# X co-ord
-?[0-9]+(\.[0-9]*)?\s+	# Y co-ord
-?[0-9]+(\.[0-9]*)?		# Z co-ord
\s*\)					# Close bracket

\s+						# Whitespace delimiter

[\w\/]+					# Texture path - word characters plus '/'

\s+						# Whitespace delimiter

\[\s*					# Open bracket for texture U parameters
-?[0-9]+(\.[0-9]*)?\s+	# X co-ordinate
-?[0-9]+(\.[0-9]*)?\s+	# Y co-ordinate
-?[0-9]+(\.[0-9]*)?\s+	# Z co-ordinate
-?[0-9]+(\.[0-9]*)?		# Offset
\s*\]					# Close bracket

\s+						# Whitespace delimiter

\[\s*					# Open bracket for texture V parameters
-?[0-9]+(\.[0-9]*)?\s+	# X co-ordinate
-?[0-9]+(\.[0-9]*)?\s+	# Y co-ordinate
-?[0-9]+(\.[0-9]*)?\s+	# Z co-ordinate
-?[0-9]+(\.[0-9]*)?		# Offset
\s*\]					# Close bracket

\s+						# Whitespace delimiter

-?[0-9]+(\.[0-9]*)?		# Texture rotation

\s+						# Whitespace delimiter

-?[0-9]+(\.[0-9]*)?		# Texture X scale

\s+						# Whitespace delimiter

-?[0-9]+(\.[0-9]*)?		# Texture Y scale
"""

def parseArgs():
	parser = argparse.ArgumentParser(description="Convert a decompiled Nightfire .map file to one that is compatible with the Source engine's Hammer Editor.")

	parser.add_argument("-o", "--output",
						required=True,
						help="Output file to write.")

	parser.add_argument("path",
						help="Input file to convert.")

	return parser.parse_args()

def modify(lines : list):
	lineMatcher = re.compile(SURFACE_DESC_MATCH, re.VERBOSE)
	output = []
	modifiedLines = 0
	skippedLines = 0

	for line in lines:
		if line.startswith('"BRUSHFLAGS" "DETAIL"'):
			skippedLines += 1
			continue

		match = lineMatcher.match(line)

		if not match:
			output.append(line)
			continue

		output.append(match.group(0) + "\n")
		modifiedLines += 1

	print(modifiedLines, "lines modified", skippedLines, "lines skipped.")
	return output

def main():
	args = parseArgs()

	print("Reading:", args.path)
	lines = []

	with open(args.path, "r") as inFile:
		lines = inFile.readlines()

	print("Fixing up surface descriptors...")
	lines = modify(lines)

	print("Writing:", args.output)

	with open(args.output, "w") as outFile:
		outFile.writelines(lines)

	print("Done. It's recommended to import this .map into JACK and re-save as a VMF, because "
		  "the Source engine Hammer is not good at importing old-style .map files.")

if __name__ == "__main__":
	main()
