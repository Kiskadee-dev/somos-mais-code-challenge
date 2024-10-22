import json
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import INDENT_SEPARATORS


class PrettyJSONRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        ret = json.dumps(
            data,
            cls=self.encoder_class,
            indent=4,
            ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict,
            separators=INDENT_SEPARATORS,
        )
        ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

        return ret.encode()
