from dataclasses import dataclass
from html import escape

from PyQt5.QtGui import QColor


TOOLTIP_FONT_SIZE_PX = 14
TOOLTIP_TITLE_SIZE_PX = 16


@dataclass(frozen=True)
class TooltipEntry:
    title: str
    signature: str = ''
    description: str = ''
    parameters: tuple = ()
    values: tuple = ()
    example: str = ''


def render_tooltip(content, palette):
    background = palette.base().color()
    is_dark = background.lightness() < 128
    text_color = QColor('#F2F2F2' if is_dark else '#202124').name()
    muted_color = QColor('#C0C5CE' if is_dark else '#505761').name()
    accent_color = QColor('#72B7FF' if is_dark else '#005A9E').name()

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
            f'<div style="color:{accent_color}; margin-top:7px;">'
            f'<code>{escape(content.signature)}</code></div>'
        )

    if content.parameters:
        rows = ''.join(
            '<tr>'
            f'<td><b>{escape(name)}</b></td>'
            f'<td>{escape(description)}</td>'
            '</tr>'
            for name, description in content.parameters
        )
        parts.append(
            '<table cellspacing="5" style="margin-top:6px;">'
            f'{rows}</table>'
        )

    if content.values:
        rows = ''.join(
            '<tr>'
            f'<td><b>{escape(str(value))}</b></td>'
            f'<td>{escape(description)}</td>'
            '</tr>'
            for value, description in content.values
        )
        parts.append(
            '<table cellspacing="6" style="margin-top:6px;">'
            f'{rows}</table>'
        )

    if content.example:
        parts.append(
            f'<div style="color:{muted_color}; margin-top:7px;">Example</div>'
            f'<div><code>{escape(content.example)}</code></div>'
        )

    parts.append('</div>')
    return ''.join(parts)
