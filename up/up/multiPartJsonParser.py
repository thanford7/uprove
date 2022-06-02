from django.http import QueryDict
import json
from rest_framework import parsers


class MultiPartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        # find the data field and parse it
        if jsonData := result.data.get('data'):
            data = json.loads(jsonData)
        else:
            data = result.data
        return parsers.DataAndFiles(data, result.files)
