def format(text):
	# Remove unnecessary asterisks from bold text
	text = text.replace('**', '*')

	# Add missing colons to section titles
	text = text.replace('*\r\n', '*:\r\n')
	text = text.replace('*\n', '*:\r\n')

	# Set preformatted blocks of code in JIRA dialect
	text = text.replace('```', '{noformat}')

	# Set preformatting of singular words
	text = text.replace(' `', ' {{')
	text = text.replace('`', '}}')

	return text
