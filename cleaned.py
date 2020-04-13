import re
def clean_text(text):
	cleaned_text = re.sub('[a-zA-Z]', '', text)
	cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', cleaned_text)
	return cleaned_text
