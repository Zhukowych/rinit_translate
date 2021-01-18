import argparse

class ArgumentsParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-table_name", type=str, help="Name of exporting translations table")
        self.parser.add_argument("-import_tables", type=str, help="Name of importing translations tables")
        self.parser.add_argument("--all-tables", action="store_true", help="Import data from all tables in database")
        self.parser.add_argument("--unaccept_eng", action="store_true", help="Unaccept translations, which consist only of eng letters and other unacceptable sumbols")
        
    def parse(self) -> dict: 
        args = self.parser.parse_args()
        parsed_args = {}
        try:
            parsed_args['translations_table_name'] = args.table_name
        except:
            raise Exception("You must provide name, to which will export translations")

        if args.all_tables:
            parsed_args["import_tables"] = ['all']
        else:
            parsed_args["import_tables"] = args.import_tables.split(" ")

        if args.unaccept_eng:
            parsed_args['unaccept_eng'] = True
        else:
            parsed_args['unaccept_eng'] = False
            
        return parsed_args
