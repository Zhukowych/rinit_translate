import string
from Logger import Logger

class DBTranslator:
    NOT_ALLOWED_ONLY_SYMBOLS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}', '|',
                                "~", "^", "[", "/", "]", "?", "@", "<", ">", "=", ";", ":", ",", 
                                '.', '!'}
    OPTIONAL_NOT_ALLOWED_SYMBOLS = set(string.ascii_letters)

    def __init__(self, db, import_tables:tuple, export_table_name:bool, unaccept_eng_symbols:bool):
        self.db = db
        self.tables_and_fields = {}
        self.language_iddentifers = ['uk', 'ru']
        self.field_pairs = []
        self.translations_dictonary = {}
        self.translations_tables = []
        self.export_table_name = export_table_name
        self.import_tables = import_tables
        self.unaccept_eng_symbols = unaccept_eng_symbols
        self.num_of_aliasing = 0

    def translate(self):
        self.db.create_or_truncate_translations_table(self.export_table_name)
        self.get_import_tables_and_fields()
        self.delete_all_tables_fields_without_language_iddentifers()
        self.create_field_pairs()
        self.create_translations_dictonary()
        self.push_data_to_db()
        
    def get_import_tables_and_fields(self):
        if self.import_tables[0] == 'all':
            self.tables_and_fields = self.db.get_all_tables_and_fields()
        else:
            self.tables_and_fields = self.db.get_tables_and_fields(self.import_tables)
        Logger.log_info(f"Found {len(self.tables_and_fields)} : {' '.join(self.tables_and_fields.keys())}")

    def create_translations_dictonary(self):
        Logger.init_import_bar(len(self.field_pairs))
        for pair in self.field_pairs:
            self.add_translations_list_to_dictonary(self.db.get_translations_pairs(pair[0], pair[1], pair[2]), import_translations_table=pair[0])
            Logger.step_importing_bar()
            
    def create_field_pairs(self):
        Logger.log_info("Finding fields pairs")
        for key, fields in self.tables_and_fields.items():
            for field in range(len(fields)):
                for second_field in range(field+1, len(fields)):
                    if self.rm_lng_id(fields[field]) == self.rm_lng_id(fields[second_field]):
                        self.field_pairs.append(self.get_pair_of_fields(key, fields[field], fields[second_field]))
                        fields.remove(fields[second_field])
                        fields.remove(fields[field])
                        break
                
    
    def delete_all_tables_fields_without_language_iddentifers(self):
        Logger.log_info("Filtering fields")
        for key, fields in self.tables_and_fields.items():
            for field in list(fields):
                if not self.whether_language_in_str(field):
                    self.tables_and_fields[key].remove(field)
    
    def whether_language_in_str(self, string: str):
        whether_is = False
        for language in self.language_iddentifers:
            if language in string:
                whether_is = True
        return whether_is

    def rm_lng_id(self, string: str) -> str:
        """Removes language iddentiffers from param string"""
        result = string
        for language in self.language_iddentifers:
            result = result.replace(language, "")
        return result

    def get_pair_of_fields(self, table, field, second_field):
        if self.language_iddentifers[0] in field:
            return [table, field, second_field]
        else:
            return [table, second_field, field]
    
    def add_translations_list_to_dictonary(self, translations_list: tuple, import_translations_table:str):
        for translation in translations_list:
            if translation[0] in self.translations_dictonary:
                self.num_of_aliasing+=1
            if self.whether_translation_is_unacceptable(translation):
                self.translations_dictonary[translation[0]] =  translation[1]
                self.translations_tables.append(import_translations_table)
    
    def whether_translation_is_unacceptable(self, translation: tuple) -> bool:
        if self.whether_translation_is_superset(translation):
            return False
        else:
            return True

    def whether_translation_is_superset(self, translation):
        not_allowed_symbols_set = self.NOT_ALLOWED_ONLY_SYMBOLS
        if self.unaccept_eng_symbols:
            not_allowed_symbols_set.update(self.OPTIONAL_NOT_ALLOWED_SYMBOLS)
        if not_allowed_symbols_set.issuperset(translation[0]) or not_allowed_symbols_set.issuperset(translation[1]):
            return True
        else:
            return False

    def push_data_to_db(self):
        Logger.log_info("\nPushing data to database")
        data_to_push = list(self.translations_dictonary.items())
        self.merge_translations_and_tables(data_to_push)
        self.db.push_translations(data_to_push)

    def merge_translations_and_tables(self, translations):
        for i, table in zip(range(len(translations)), self.translations_tables):
            translations[i] = list(translations[i])
            translations[i].insert(0, table)
