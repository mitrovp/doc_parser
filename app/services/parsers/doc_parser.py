from app.services.parsers.abstract import BaseParser


class DocParser(BaseParser):
    async def parse(self, file_path):
        # Implement DOC parsing logic here
        pass


doc_parser = DocParser()

