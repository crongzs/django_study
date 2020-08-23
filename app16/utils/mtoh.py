import markdown


class ToHtml(object):
    def __init__(self, mdText):
        self.mdText = mdText

    def __to_html(self):
        html = markdown.markdown(self.mdText, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        return html

    def to_html(self):
        return self.__to_html()
