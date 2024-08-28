from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from src.views.widgets.button import Button
from src.views.widgets.combo_box import ComboBox
from src.views.widgets.dialog import Dialog
from src.views.widgets.double_spin_box import DoubleSpinBox
from src.views.widgets.heading import Heading1
from src.views.widgets.heading import Heading2
from src.views.widgets.heading import Heading3
from src.views.widgets.heading import Heading4
from src.views.widgets.heading import Heading5
from src.views.widgets.heading import Heading6

from src.views.widgets.label import Label
from src.views.widgets.line_edit import LineEdit
from src.views.widgets.list import List
from src.views.widgets.spin_box import SpinBox
from src.views.widgets.table import Table
from src.views.widgets.textarea import TextArea

QWidgetLike = TypeVar("QWidgetLike", bound=QWidget)


class WidgetsFactory:
    def __init__(self, theme_class):
        self.theme = theme_class

    def label(self, text: str = None, *, parent: QWidgetLike = None) -> Label:
        lb = Label(self.theme.text_primary, parent)
        if text:
            lb.setText(text)
        return lb

    def subtitle(self, text: str = None, *, parent: QWidgetLike = None) -> Label:
        lb = Label(self.theme.text_secondary, parent)
        if text:
            lb.setText(text)
        return lb

    def heading1(self, text: str = None, *, parent: QWidgetLike = None) -> Heading1:
        lb = Heading1(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading2(self, text: str = None, *, parent: QWidgetLike = None) -> Heading2:
        lb = Heading2(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading3(self, text: str = None, *, parent: QWidgetLike = None) -> Heading3:
        lb = Heading3(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading4(self, text: str = None, *, parent: QWidgetLike = None) -> Heading4:
        lb = Heading4(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading5(self, text: str = None, *, parent: QWidgetLike = None) -> Heading5:
        lb = Heading5(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def heading6(self, text: str = None, *, parent: QWidgetLike = None) -> Heading6:
        lb = Heading6(self.theme.text_header, parent)
        if text:
            lb.setText(text)
        return lb

    def combo_box(self, parent: QWidgetLike = None) -> ComboBox:
        return ComboBox(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            third_background_color=self.theme.third_background,
            hover_color=self.theme.hover,
            parent=parent
        )

    def spin_box(self, parent: QWidgetLike = None) -> SpinBox:
        return SpinBox(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            parent=parent
        )

    def double_spin_box(self, parent: QWidgetLike = None) -> DoubleSpinBox:
        return DoubleSpinBox(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            first_background_color=self.theme.first_background,
            second_background_color=self.theme.second_background,
            parent=parent
        )

    def modal(self, parent: QWidgetLike = None) -> Dialog:
        return Dialog(
            third_background=self.theme.third_background,
            second_background=self.theme.second_background,
            hover=self.theme.hover,
            text_header=self.theme.text_header,
            parent=parent
        )

    def button(self, text: str = None, *, parent: QWidgetLike = None) -> Button:
        btn = Button(self.theme.hover, self.theme.text_primary, self.theme.third_background, parent)
        if text:
            btn.setText(text)
        return btn

    def list(self, parent: QWidgetLike = None) -> List:
        return List(
            text_primary_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            selection_color=self.theme.selection,
            parent=parent
        )

    def line_edit(self, parent: QWidgetLike = None) -> LineEdit:
        return LineEdit(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            third_background_color=self.theme.third_background,
            parent=parent
        )

    def textarea(self, parent: QWidgetLike = None) -> TextArea:
        return TextArea(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            third_background_color=self.theme.third_background,
            parent=parent
        )

    def table(self, parent: QWidgetLike = None) -> Table:
        return Table(
            selection_color=self.theme.selection,
            primary_text_color=self.theme.text_primary,
            hover_color=self.theme.hover,
            third_background_color=self.theme.third_background,
            parent=parent
        )