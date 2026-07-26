import unittest

from PyQt5.QtGui import QPalette

from text_editor.tooltips.content import TooltipEntry, render_tooltip
from text_editor.tooltips.registry import tooltips


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
        self.assertEqual(rendered.count('<nobr>'), 2)

    def test_keeps_legacy_html_compatible(self):
        content = '<b>Legacy tooltip</b>'
        rendered = render_tooltip(content, QPalette())

        self.assertIn(content, rendered)
        self.assertIn('font-size:14px', rendered)

    def test_renders_requested_minimum_width(self):
        entry = TooltipEntry(title='IF statement', minimum_width=620)
        rendered = render_tooltip(entry, QPalette())

        self.assertIn('<table width="620"', rendered)

    def test_control_flow_aliases_share_their_tooltip(self):
        self.assertIs(tooltips['AND'], tooltips['IF'])
        self.assertIs(tooltips['DO'], tooltips['FOR'])
        self.assertIs(tooltips['ELSE'], tooltips['IF'])
        self.assertIs(tooltips['ENDIF'], tooltips['IF'])
        self.assertIs(tooltips['NEXT'], tooltips['FOR'])
        self.assertIs(tooltips['OR'], tooltips['IF'])
        self.assertIs(tooltips['THEN'], tooltips['IF'])

    def test_renders_control_flow_structure(self):
        rendered = render_tooltip(tooltips['IF'], QPalette())

        self.assertIn('STRUCTURE', rendered)
        self.assertIn('ELSE', rendered)
        self.assertIn('ENDIF', rendered)
        self.assertIn('PROGRAM_BODY', rendered)
        self.assertIn('&nbsp;', rendered)


if __name__ == '__main__':
    unittest.main()
