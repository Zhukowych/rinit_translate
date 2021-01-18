from DBTranslator import DBTranslator
from MYSQL import MYSQL
from ArgumentsParser import ArgumentsParser

if __name__ == "__main__":
    parser = ArgumentsParser()
    parse_data = parser.parse()
    db_translator = DBTranslator(MYSQL(), export_table_name=parse_data['translations_table_name'], import_tables=parse_data['import_tables'], unaccept_eng_symbols=parse_data['unaccept_eng'])
    db_translator.translate()
   
