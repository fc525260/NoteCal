"""
日历委托模块

提供自定义的单元格绘制，实现卡片式立体感风格的日历外观。
遵循 Win11 Fluent Design 和 UI/UX Pro Max 设计指南。
"""
from PyQt5.QtCore import Qt, QRect, QRectF, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import (
    QBrush, QColor, QFont, QPen, QPainter, QPainterPath,
    QLinearGradient, QRadialGradient
)
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem

from .calendar_model import CalendarModel
from .theme import ThemeManager


class CalendarDelegate(QStyledItemDelegate):
    """日历单元格委托

    自定义日历单元格的绘制，实现卡片式立体感效果。
    遵循 UI/UX Pro Max 设计指南：
    - 动画时长 150-300ms
    - 触摸目标最小 44x44px
    - 颜色对比度 4.5:1
    """

    CORNER_RADIUS = 12
    NOTE_DOT_SIZE = 7

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager.get_instance()

    def paint(self, painter, option, index):
        if not index.isValid():
            super().paint(painter, option, index)
            return

        model = index.model()
        day_data = model.data(index, CalendarModel.ROLE_DAY)
        if day_data is None:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        rect = option.rect
        is_today = model.data(index, CalendarModel.ROLE_IS_TODAY)
        has_note = model.data(index, CalendarModel.ROLE_HAS_NOTE)
        is_overtime = model.data(index, CalendarModel.ROLE_OVERTIME)
        is_business_trip = model.data(index, CalendarModel.ROLE_BUSINESS_TRIP)
        is_marked = model.data(index, CalendarModel.ROLE_IS_MARKED)
        lunar = model.data(index, CalendarModel.ROLE_LUNAR)
        is_weekend = index.column() >= 5
        is_dark = self._theme_manager.current_theme == ThemeManager.DARK_THEME
        is_selected = option.state & QStyle.State_Selected
        is_hovered = option.state & QStyle.State_MouseOver

        if is_dark:
            text_color = QColor(235, 235, 235)
            lunar_color = QColor(140, 140, 140)
            note_dot_color = QColor(255, 100, 100)
            overtime_dot_color = QColor(80, 200, 120)
            business_trip_dot_color = QColor(255, 170, 70)
            card_bg = QColor(38, 38, 40)
            card_bg_hover = QColor(50, 50, 55)
            card_bg_selected = QColor(60, 60, 80)
            shadow_color = QColor(0, 0, 0, 40)
            selection_color = QColor(96, 205, 255)
        else:
            text_color = QColor(30, 30, 30)
            lunar_color = QColor(100, 100, 100)
            note_dot_color = QColor(220, 50, 50)
            overtime_dot_color = QColor(40, 180, 100)
            business_trip_dot_color = QColor(245, 145, 35)
            card_bg = QColor(255, 255, 255)
            card_bg_hover = QColor(248, 250, 252)
            card_bg_selected = QColor(230, 245, 255)
            shadow_color = QColor(0, 0, 0, 15)
            selection_color = QColor(0, 120, 212)

        if is_marked:
            bg_color = card_bg_selected
        elif is_selected:
            bg_color = card_bg_selected
        elif is_hovered:
            bg_color = card_bg_hover
        else:
            bg_color = card_bg

        cell_rect = QRectF(rect.adjusted(1, 1, -1, -1))

        if is_today:
            if is_dark:
                gradient = QLinearGradient(0, 0, 0, rect.height())
                gradient.setColorAt(0, QColor(96, 205, 255))
                gradient.setColorAt(0.5, QColor(80, 180, 240))
                gradient.setColorAt(1, QColor(64, 160, 220))
                bg_color = gradient
            else:
                gradient = QLinearGradient(0, 0, 0, rect.height())
                gradient.setColorAt(0, QColor(255, 230, 120))
                gradient.setColorAt(0.5, QColor(255, 210, 80))
                gradient.setColorAt(1, QColor(255, 190, 50))
                bg_color = gradient
            text_color = QColor(20, 20, 20)

        path = QPainterPath()
        path.addRoundedRect(cell_rect, self.CORNER_RADIUS, self.CORNER_RADIUS)

        if not is_today:
            painter.setPen(QPen(shadow_color, 1))
            painter.setBrush(QBrush(shadow_color))
            shadow_rect = QRectF(cell_rect)
            shadow_rect.translate(0, 2)
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(shadow_rect, self.CORNER_RADIUS, self.CORNER_RADIUS)
            painter.fillPath(shadow_path, shadow_color)

        if isinstance(bg_color, QLinearGradient):
            painter.fillPath(path, bg_color)
        else:
            painter.fillPath(path, bg_color)

        border_color = QColor(200, 200, 200, 40) if is_dark else QColor(220, 220, 220, 60)
        border_pen = QPen(border_color, 1)
        painter.setPen(border_pen)
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawPath(path)

        if is_selected or is_marked:
            selection_pen = QPen(selection_color, 3)
            selection_path = QPainterPath()
            selection_rect = QRectF(cell_rect.adjusted(1, 1, -1, -1))
            selection_path.addRoundedRect(selection_rect, self.CORNER_RADIUS - 1, self.CORNER_RADIUS - 1)
            painter.setPen(selection_pen)
            painter.setBrush(QBrush(Qt.NoBrush))
            painter.drawPath(selection_path)

        font_size = 22 if not lunar else 18
        font_weight = QFont.Bold if is_today else QFont.Medium
        day_font = QFont("Microsoft YaHei UI", font_size, font_weight)
        painter.setFont(day_font)
        painter.setPen(text_color)

        if lunar:
            day_rect = QRect(rect.x(), rect.y() + 8, rect.width(), rect.height() // 2 - 6)
            painter.drawText(day_rect, Qt.AlignHCenter | Qt.AlignBottom, str(day_data))

            lunar_font = QFont("Microsoft YaHei UI", 11)
            painter.setFont(lunar_font)
            if is_today:
                painter.setPen(QColor(80, 70, 40))
            else:
                painter.setPen(lunar_color)
            lunar_rect = QRect(rect.x(), rect.y() + rect.height() // 2 + 2, rect.width(), rect.height() // 2 - 12)
            painter.drawText(lunar_rect, Qt.AlignHCenter | Qt.AlignTop, lunar)
        else:
            painter.drawText(rect, Qt.AlignCenter, str(day_data))

        dot_y = rect.bottom() - self.NOTE_DOT_SIZE - 9
        painter.setPen(QPen(Qt.NoPen))

        status_dots = []
        if has_note:
            status_dots.append(note_dot_color)
        if is_overtime:
            status_dots.append(overtime_dot_color)
        if is_business_trip:
            status_dots.append(business_trip_dot_color)

        dot_gap = 5
        dot_right_margin = 9
        for dot_index, dot_color in enumerate(reversed(status_dots)):
            dot_x = (
                rect.right()
                - dot_right_margin
                - self.NOTE_DOT_SIZE
                - dot_index * (self.NOTE_DOT_SIZE + dot_gap)
            )
            dot_rect = QRect(dot_x, dot_y, self.NOTE_DOT_SIZE, self.NOTE_DOT_SIZE)
            painter.setBrush(dot_color)
            painter.drawEllipse(dot_rect)

        if is_hovered and not is_selected and not is_today:
            hover_path = QPainterPath()
            hover_rect = QRectF(cell_rect.adjusted(2, 2, -2, -2))
            hover_path.addRoundedRect(hover_rect, self.CORNER_RADIUS - 2, self.CORNER_RADIUS - 2)
            hover_color = QColor(96, 205, 255, 20 if is_dark else 12)
            painter.fillPath(hover_path, hover_color)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(88, 88)
