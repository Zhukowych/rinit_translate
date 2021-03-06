import mysql.connector

class MYSQL:
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "absurdH5+PRO"
    DB_NAME = "td"
    AUTH_PLUGIN = "mysql_native_password"
    CHUNK_SIZE = 1000
    
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
        self.translations_table_name = None
    
    def create_or_truncate_translations_table(self, translation_table_name: str, todo_table_name: str):
        self.translations_table_name = translation_table_name
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS %s (
                                `table` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
                                `uk` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
                                `ru` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL, 
                                KEY `table` (`table`),
                                KEY `uk` (`uk`), 
                                KEY `ru` (`ru`) 
                            ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci""" % translation_table_name)
        self.cursor.execute("TRUNCATE TABLE %s" % translation_table_name)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS %s (
                        `table` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
                        `uk` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
                        `ru` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL, 
                        KEY `table` (`table`),
                        KEY `uk` (`uk`), 
                        KEY `ru` (`ru`) 
                    ) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci""" % todo_table_name)
        self.cursor.execute("TRUNCATE TABLE %s" % todo_table_name)

    def get_all_translations(self):
        self.cursor.execute("SELECT * FROM translations")
        return self.cursor.fetchall()


    def get_all_tables_and_fields(self) -> dict:
        self.cursor.execute("SHOW TABLES")
        result = {}
        table_names = self.cursor.fetchall()
        for (table_name, ) in table_names:
            try:
                name = table_name.decode()
            except Exception:
                name = table_name
            result[name] = self.get_table_fields(name)
        del result[self.translations_table_name]
        return result

    def get_tables_and_fields(self, tables_names: tuple) -> dict:
        result = {}
        for table_name in tables_names:
            result[table_name] = self.get_table_fields(table_name)
        return result

    def get_table_fields(self, table_name: str) -> list:
        self.cursor.execute(f"show columns from {table_name} WHERE field LIKE '%uk' OR field LIKE '%ru'")
        return [column[0] for column in self.cursor.fetchall()]

    def get_translations_from_table(self, table_name, uk_translation, ru_translation) -> list:
        self.cursor.execute("SELECT '%(table_name)s' as tablename, %(uk_translation)s, %(ru_translation)s FROM %(table_name)s WHERE %(uk_translation)s!='' GROUP BY %(uk_translation)s, %(ru_translation)s" %
                            {'uk_translation': uk_translation,
                             'ru_translation':ru_translation,
                             'table_name':table_name})
        return self.cursor.fetchall()

    def chunk(self, data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
    
    def push_translations(self, table_name, translations):
        chunked_translations = self.chunk(translations, self.CHUNK_SIZE)
        for chunk in chunked_translations:
            self.cursor.executemany(f"INSERT into {table_name} VALUES (%s, %s, %s)", chunk)
            self.connection.commit()
