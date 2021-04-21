"""
Author: Denyson Grellert
"""

def hasNewLine(last):
	if last in ['.', '!', ';', '\"', '?']:
		return '\n'
	if last == ' ':
		return ' '

	return ''


def textParsed(string):
	text = ""
	numberSP = 0
	last = None

	for i in string:
		if i == '\n':
			text += hasNewLine(last)
			last = i
			continue
		if i == ' ':
			numberSP += 1
			last = i
			continue

		if numberSP >= 1 and last == ' ':
			text += ' '

		text += i
		last = i
		numberSP = 0

	return text