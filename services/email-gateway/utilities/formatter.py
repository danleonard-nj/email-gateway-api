
import json

from models.formatter import FormatDefault
from pretty_html_table import build_table
from pretty_html_table.pretty_html_table import dict_colors
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


class Formatter:
    def __init__(self):
        self.valid_styles = list(dict_colors.keys())

    def format_json(
        self,
        data,
        style
    ):
        json_style = style or FormatDefault.JSON
        content = json.dumps(
            data, indent=4, sort_keys=True)

        formatter = HtmlFormatter(
            style=json_style,
            noclasses=True)

        json_html = highlight(
            content,
            JsonLexer(),
            formatter)

        return json_html

    def format_table(self, df, style, title='Kube-Tools'):
        email_style = style or FormatDefault.TABLE

        if email_style not in self.valid_styles:
            choices = ', '.join(self.valid_styles)
            raise Exception(
                f"'{email_style}' is not a valid style choice: {choices}")

        table_html = build_table(
            df, email_style)

        return table_html

    def format_email(
        self,
        email_content,
        title=None,
        template='template.html'
    ):
        with open(f'./resources/{template}', 'r') as file:
            content = file.read()

        email_title = title or FormatDefault.TITLE
        email_content = self.replace_field(
            template=content,
            field_name=FormatDefault.CONTENT_KEY,
            content=email_content)

        email = self.replace_field(
            template=email_content,
            field_name=FormatDefault.TITLE_KEY,
            content=email_title)

        return email

    def replace_field(
        self,
        template,
        field_name,
        content
    ):
        segments = template.split(
            field_name)

        return ''.join([
            segments[0],
            content,
            segments[1]
        ])
