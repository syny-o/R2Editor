from dataclasses import dataclass
from html import escape
import re

from PyQt5.QtGui import QColor


TOOLTIP_FONT_SIZE_PX = 14
TOOLTIP_TITLE_SIZE_PX = 16
SIGNATURE_TOKEN_PATTERN = re.compile(
    r'<>|==|[=(),"]|[A-Za-z_]\w*|\d+(?:\.\d+)?|\s+|.'
)
KEYWORDS = frozenset({
    'AND',
    'DO',
    'ELSE',
    'ENDIF',
    'FOR',
    'IF',
    'NEXT',
    'OR',
    'THEN',
})
PLACEHOLDER_PREFIXES = (
    'max_',
    'min_',
    'number_',
    'object_',
    'operator',
    'sample_',
    'tolerance',
    'total_',
    'value',
    'variable',
)


@dataclass(frozen=True)
class TooltipEntry:
    title: str
    signature: str = ''
    description: str = ''
    parameters: tuple = ()
    values: tuple = ()
    example: str = ''


def _section_label(text, muted_color):
    return (
        f'<div style="color:{muted_color}; font-size:11px; '
        f'margin-top:8px;">{escape(text.upper())}</div>'
    )


def _highlight_signature(signature, colors):
    rendered = []
    command_seen = False

    for match in SIGNATURE_TOKEN_PATTERN.finditer(signature):
        token = match.group()
        escaped_token = escape(token)
        normalized = token.lower()

        if token.isspace():
            rendered.append(escaped_token)
        elif token in KEYWORDS:
            rendered.append(
                f'<span style="color:{colors["keyword"]};">'
                f'<b>{escaped_token}</b></span>'
            )
        elif token in {'=', '==', '<>', '(', ')', ',', '"'}:
            rendered.append(
                f'<span style="color:{colors["punctuation"]};">'
                f'<b>{escaped_token}</b></span>'
            )
        elif token.replace('.', '', 1).isdigit():
            rendered.append(
                f'<span style="color:{colors["number"]};">'
                f'{escaped_token}</span>'
            )
        elif (
            token.isupper()
            or normalized.startswith(PLACEHOLDER_PREFIXES)
        ):
            rendered.append(
                f'<span style="color:{colors["parameter"]};">'
                f'{escaped_token}</span>'
            )
        elif not command_seen:
            command_seen = True
            rendered.append(
                f'<span style="color:{colors["command"]};">'
                f'<b>{escaped_token}</b></span>'
            )
        else:
            rendered.append(escaped_token)

    return ''.join(rendered)


def render_tooltip(content, palette):
    background = palette.base().color()
    is_dark = background.lightness() < 128
    text_color = QColor('#F2F2F2' if is_dark else '#202124').name()
    muted_color = QColor('#C0C5CE' if is_dark else '#505761').name()
    accent_color = QColor('#72B7FF' if is_dark else '#005A9E').name()
    syntax_colors = {
        'command': QColor('#D2A8FF' if is_dark else '#6F42C1').name(),
        'keyword': QColor('#FF7AB2' if is_dark else '#AF125A').name(),
        'parameter': QColor('#79C0FF' if is_dark else '#005CC5').name(),
        'punctuation': QColor('#FFA657' if is_dark else '#B54708').name(),
        'number': QColor('#7EE787' if is_dark else '#1A7F37').name(),
    }

    if isinstance(content, str):
        return (
            f'<div style="color:{text_color}; '
            f'font-size:{TOOLTIP_FONT_SIZE_PX}px;">'
            f'{content}</div>'
        )

    parts = [
        (
            f'<div style="color:{text_color}; '
            f'font-size:{TOOLTIP_FONT_SIZE_PX}px;">'
            f'<b style="font-size:{TOOLTIP_TITLE_SIZE_PX}px;">'
            f'{escape(content.title)}</b>'
        )
    ]

    if content.description:
        parts.append(
            f'<div style="color:{muted_color}; margin-top:4px;">'
            f'{escape(content.description)}</div>'
        )

    if content.signature:
        parts.append(
            _section_label('Syntax', muted_color)
        )
        parts.append(
            f'<div style="color:{text_color}; margin-top:3px; '
            f'padding:4px;"><code>'
            f'{_highlight_signature(content.signature, syntax_colors)}'
            f'</code></div>'
        )

    if content.parameters:
        parts.append(_section_label('Parameters', muted_color))
        rows = ''.join(
            '<tr>'
            f'<td style="color:{accent_color};"><b>{escape(name)}</b></td>'
            f'<td>{escape(description)}</td>'
            '</tr>'
            for name, description in content.parameters
        )
        parts.append(
            '<table cellspacing="6" style="margin-top:2px;">'
            f'{rows}</table>'
        )

    if content.values:
        parts.append(_section_label('Values', muted_color))
        rows = ''.join(
            '<tr>'
            f'<td style="color:{syntax_colors["number"]};">'
            f'<b>{escape(str(value))}</b></td>'
            f'<td>{escape(description)}</td>'
            '</tr>'
            for value, description in content.values
        )
        parts.append(
            '<table cellspacing="6" style="margin-top:2px;">'
            f'{rows}</table>'
        )

    if content.example:
        parts.append(_section_label('Example', muted_color))
        parts.append(
            f'<div style="color:{text_color}; margin-top:3px; '
            f'padding:4px;"><code>'
            f'{_highlight_signature(content.example, syntax_colors)}'
            f'</code></div>'
        )

    parts.append('</div>')
    return ''.join(parts)
