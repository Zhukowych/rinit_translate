from MYSQL import MYSQL
import string
db = MYSQL()
NOT_ALLOWED_ONLY_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}', '|',
                                "~", "^", "[", "/", "]", "?", "@", "<", ">", "=", ";", ":", ",", 
                                '.', '!', '+', '-', '*', '_', "'", '"', ',', '(', ')']

uppercase_symbols = set(string.ascii_uppercase)
all_eng_symbols = set(string.ascii_letters)
all_eng_symbols.update(set(NOT_ALLOWED_ONLY_SYMBOLS))
all_eng_symbols.update({' '})
print(all_eng_symbols)
print(uppercase_symbols)
todo_translations = []
sorted_translations = []


def delete_symbols_from_str(string: str):
    result = string
    for i in NOT_ALLOWED_ONLY_SYMBOLS:
        result = result.replace(i, '')
    return result

def filter():
    translations = db.get_all_translations()
    for translation in translations:
        is_accept = False
        formated = delete_symbols_from_str(translation[1])
        words = formated.split(" ")
        for word in words:
            if len(word)>=4 and not uppercase_symbols.issuperset(word):
                is_accept = True
        if is_accept:
            if all_eng_symbols.issuperset(translation[1]):
                todo_translations.append(translation)
            else:
                sorted_translations.append(translation)

filter()
print(len(sorted_translations))
print(len(todo_translations))
db.push_translations(sorted_translations)
'''r = delete_symbols_from_str("3 (13-2370HL)")
words = r.split(" ")
is_accept = False
print(words)
for word in words:
    if len(word)>=4 and not uppercase_symbols.issuperset(word):
        is_accept = True
print(is_accept)
'''
