from app.services.parsers.abstract import BaseParser


class ImageParser(BaseParser):
    async def parse(self, file_path):
        # Implement image parsing logic here
        pass


image_parser = ImageParser()
