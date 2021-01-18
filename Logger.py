from progress.bar import Bar


class Logger:

    def __init__(self):
        self.data_import_bar = None

    @classmethod
    def log_info(self, message):
        print('green')

    @classmethod
    def init_import_bar(self, num_of_tables: int):
        self.data_import_bar = Bar("Impoting data", max=num_of_tables)

    @classmethod
    def step_importing_bar(self):
        self.data_import_bar.next()
