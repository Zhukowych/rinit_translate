import mysql.connector

class MYSQL:
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "absurdH5+PRO"
    DB_NAME = "td"
    AUTH_PLUGIN = "mysql_native_password"
    
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
            charset = "utf8", 
            collation="utf8_general_ci",
            use_unicode = True,
            auth_plugin=self.AUTH_PLUGIN
        )
        self.connection.set_charset_collation('utf8', 'utf8_general_ci')
        self.cursor = self.connection.cursor(buffered=True)
        self.cursor.execute("SET NAMES UTF8")
    
    def create_or_truncate_translations_table(self, translation_table_name: str):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS %s (
                                `table` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
                                `uk` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
                                `ru` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL, 
                                KEY `table` (`table`),
                                KEY `uk` (`uk`), 
                                KEY `ru` (`ru`) 
                            ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci""" % translation_table_name)
        self.cursor.execute("TRUNCATE TABLE %s" % translation_table_name)


    def get_all_tables_and_fields(self) -> dict:
        self.cursor.execute("SHOW TABLES")
        result = {}
        table_names = self.cursor.fetchall()
        for (table_name, ) in table_names:
            name = table_name.decode()
            result[name] = self.get_table_fields(name)
        return result

    def get_tables_and_fields(self, tables_names: tuple) -> dict:
        result = {}
        for table_name in tables_names:
            result[table_name] = self.get_table_fields(table_name)
        return result

    def get_table_fields(self, table_name: str) -> list:
        self.cursor.execute("show columns from %s" % table_name)
        return [column[0] for column in self.cursor.fetchall()]

    def get_translations_pairs(self, table_name, uk_translation, ru_translation) -> list:
        self.cursor.execute("SELECT DISTINCT %(uk_translation)s, %(ru_translation)s FROM %(table_name)s WHERE %(uk_translation)s!=''" %
                            {'uk_translation': uk_translation,
                             'ru_translation':ru_translation,
                             'table_name':table_name})
        return self.cursor.fetchall()
    
    def push_translations(self, translations):
        self.cursor.executemany("INSERT into translations VALUES (%s, %s, %s)", translations)
        self.connection.commit()
