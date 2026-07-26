import unittest

from PyQt5.QtGui import QPalette

from text_editor.tooltip_content import TooltipEntry, render_tooltip


class TooltipContentTest(unittest.TestCase):
    def test_renders_structured_tooltip_and_escapes_values(self):
        entry = TooltipEntry(
            title='FOR <cycle>',
            signature='FOR x = 1 2 DO',
            parameters=(('x', 'Value < 3'),),
            example='FOR x = 1 2 DO',
        )

        rendered = render_tooltip(entry, QPalette())

        self.assertIn('FOR &lt;cycle&gt;', rendered)
        self.assertIn('Value &lt; 3', rendered)
        self.assertIn('<table', rendered)
        self.assertIn('EXAMPLE', rendered)
        self.assertIn('SYNTAX', rendered)
        self.assertIn('font-size:14px', rendered)
        self.assertIn('font-size:16px', rendered)
        self.assertNotIn('FOR x = 1 2 DO', rendered)
        self.assertIn('<span', rendered)

    def test_keeps_legacy_html_compatible(self):
        content = '<b>Legacy tooltip</b>'
        rendered = render_tooltip(content, QPalette())

        self.assertIn(content, rendered)
        self.assertIn('font-size:14px', rendered)


if __name__ == '__main__':
    unittest.main()
