def format(text):
	return text.replace('**', '*').replace('*\r\n', '*:\r\n').replace('*\n', '*:\r\n').replace('```', '{noformat}')
