import string
from Logger import Logger

class DBTranslator:
    NOT_ALLOWED_ONLY_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}', '|',
                                "~", "^", "[", "/", "]", "?", "@", "<", ">", "=", ";", ":", ",", 
                                '.', '!', '+', '-', '*', '_', "'", '"', ',', '(', ')']
    UPPERCASE_SYMBOLS = set(string.ascii_uppercase)
    OPTIONAL_NOT_ALLOWED_SYMBOLS = set(string.ascii_letters)
    OPTIONAL_NOT_ALLOWED_SYMBOLS.update(NOT_ALLOWED_ONLY_SYMBOLS)
    OPTIONAL_NOT_ALLOWED_SYMBOLS.update({' '})
    print(OPTIONAL_NOT_ALLOWED_SYMBOLS)
    TABLE_IND = 0
    
    def __init__(self, db, import_tables:tuple, export_table_name:str, todo_table_name:str, unaccept_eng_symbols:bool):
        self.db = db
        self.tables_and_fields = {}
        self.language_iddentifers = ['uk', 'ru']
        self.general_fields = []
        self.translations = []
        self.not_filtered_translations = []
        self.todo_translations = []
        self.translations_history = []
        
        """  SETINGS """
        self.export_table_name = export_table_name
        self.todo_table_name = todo_table_name
        self.import_tables = import_tables
        self.unaccept_eng_symbols = unaccept_eng_symbols
        self.num_of_aliasing = 0

    def translate(self):
        self.db.create_or_truncate_translations_table(self.export_table_name, self.todo_table_name)
        self.get_import_tables_and_fields()
        self.find_translations_columns()
        self.create_translations()
        self.filter_translations()

        self.push_data_to_db()
        
    def get_import_tables_and_fields(self):
        """ Get tables and their fields with 'uk' or 'ru' """
        if self.import_tables[0] == 'all':
            self.tables_and_fields = self.db.get_all_tables_and_fields()
        else:
            self.tables_and_fields = self.db.get_tables_and_fields(self.import_tables)
        Logger.log_info(f"Found {len(self.tables_and_fields)} : {' '.join(self.tables_and_fields.keys())}")

    def find_translations_columns(self):
        """
           Delete from all fields 'uk' and 'ru'
           For example self.tables_and_fields = {'table_1': ['name_uk', 'name_ru', 'surname_uk', 'surname_ru'],
                                                 'table_2': ['car_name_uk', 'car_name_ru', 'engine_uk', 'engine_ru']}
           temp (for 'table_1' in line 50) = ['table_1', 'name_', 'surname_']
           in result self.generals_fields = [['table_1', 'name_', 'surname_'], ['table_2', 'car_name_', 'engine_']]
        """
        Logger.log_info("Finding fields pairs")
        for key, fields in self.tables_and_fields.items():
            temp = []
            for field in (fields):
                temp.append(self.delete_language(field))
            temp = list(dict.fromkeys(temp))    
            temp.insert(0, key)
            self.general_fields.append(temp)

    def create_translations(self):
        """ Create request to db to get all column data by field and filter response """

        total_length = 0
        for fields in self.general_fields:
            total_length += len(fields) - 1

        Logger.init_import_bar(total_length)
        for fields in self.general_fields:
            table_name = fields[self.TABLE_IND]
            fields.pop(0)
            for field in fields:
                data = self.db.get_translations_from_table(table_name, field+"uk", field+"ru")
                self.not_filtered_translations += data
                Logger.step_importing_bar()

    def filter_translations(self):
        for translation in self.not_filtered_translations:
            if translation[1] in self.translations_history: 
                continue
            is_accept = False
            formated = self.delete_symbols_from_str(translation[1])
            words = formated.split(" ")
            for word in words:
                if len(word)>=4 and not self.UPPERCASE_SYMBOLS.issuperset(word):
                    is_accept = True
            if is_accept:
                if self.OPTIONAL_NOT_ALLOWED_SYMBOLS.issuperset(translation[1]):
                    self.todo_translations.append(translation)
                else:
                    self.translations.append(translation)
            self.translations_history.append(translation[1])

    def push_data_to_db(self):
        """ push translations to db """
        Logger.log_info("\nPushing data to database")
        self.db.push_translations(self.export_table_name, self.translations)
        self.db.push_translations(self.todo_table_name, self.todo_translations)


    def delete_language(self, string: str):
        result = string
        for language in self.language_iddentifers:
            result = result.replace(language, "")
        return result

    def delete_symbols_from_str(self, string:str):
        result = string
        for i in self.NOT_ALLOWED_ONLY_SYMBOLS:
            result = result.replace(i, '')
        return result
   


