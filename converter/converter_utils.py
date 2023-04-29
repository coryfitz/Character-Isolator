import string
from django.contrib.staticfiles.storage import staticfiles_storage

def get_unique_characters(ur_text):
    text = []
    for char in ur_text:
        if char not in text:
            text.append(char)
    text = str(text)

    #Find unique characters
    unique = []
    for char in text:
        if char not in unique:
            unique.append(char)
    unique = str(unique)

    #Remove punctuation and whitespace
    nopunct_unique = unique.translate(str.maketrans('', '', string.punctuation))
    nodigit_unique = nopunct_unique.translate(str.maketrans('', '', string.digits))
    noletter_unique = nodigit_unique.translate(str.maketrans('', '', string.ascii_letters))
    nochinesepunct_unique = noletter_unique.translate({ord(c): None for c in '。；：！？，、'})
    clean_unique = nochinesepunct_unique.translate({ord(c): None for c in string.whitespace})
    return clean_unique
        
def filter_characters(clean_unique, preference):
    if preference == 'NO':
        file_path = staticfiles_storage.open('converter/filternone.csv')

    elif preference == 'F250':
        file_path = staticfiles_storage.open('converter/filter250.csv')

    elif preference == 'F500':
        file_path = staticfiles_storage.open('converter/filter500.csv')

    elif preference == 'F750':
        file_path = staticfiles_storage.open('converter/filter750.csv')

    else:
        file_path = staticfiles_storage.open('converter/filter1000.csv')

    filter_file = file_path.read().decode("utf-8")

    filter = set([])
    for word in filter_file:
        filter.add(word)

    #Filter out common characters
    filtered = set([])
    for word in clean_unique:
        if word not in filter:
            filtered.add(word)
    return filtered