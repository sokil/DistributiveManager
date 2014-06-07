from math import ceil

class Paginator:

    def __init__(self, cursor=None):
        self.cursor = cursor
        self.page_cursor = None
        self.page = 1
        self.page_length = 20

        self.total_length = None

    def set_cursor(self, cursor):
        self.cursor = cursor
        return self

    def set_page(self, page):
        if page:
            try:
                page = int(page)
            except ValueError:
                page = 1

        if not page:
            page = 1

        self.page = page
        self.page_cursor = None

        return self

    def get_page(self):
        return self.page

    def set_page_length(self, length):
        length = int(length)
        if length:
            self.page_length = length

        self.page_cursor = None

        return self

    def get_total_length(self):
        if not self.total_length:
            self.total_length = self.cursor.count()

        return self.total_length

    def get_total_pages(self):
        return int(ceil(self.get_total_length() / self.page_length))

    def __iter__(self):
        return self

    def __next__(self):
        self.next()

    def next(self):
        if not self.page_cursor:
            self.page_cursor = self.cursor.limit(self.page_length).skip(self.page_length * (self.page - 1))

        return self.page_cursor.next()