"""
UI screens for the Study Planner App.

Defines main screens and navigation.
"""

from typing import Optional

import flet as ft

from app.ui.components import (
    create_header,
    create_button,
    create_card,
    create_badge,
)
from app.ui.styles import Colors, FontSizes, Spacing
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_home_screen(page: ft.Page) -> ft.Column:
    """
    Create the home screen.
    
    Args:
        page: Flet page object
    
    Returns:
        ft.Column: Home screen component
    """
    def on_schedule_click():
        logger.info("Schedule button clicked")
        page.snack_bar = ft.SnackBar(ft.Text("📅 일정 관리 기능 준비 중..."))
        page.snack_bar.open = True
        page.update()
    
    def on_ai_feedback_click():
        logger.info("AI Feedback button clicked")
        page.snack_bar = ft.SnackBar(ft.Text("🤖 AI 분석 기능 준비 중..."))
        page.snack_bar.open = True
        page.update()
    
    def on_account_click():
        logger.info("Account button clicked")
        page.snack_bar = ft.SnackBar(ft.Text("👤 계정 관리 준비 중..."))
        page.snack_bar.open = True
        page.update()
    
    # Header
    header = create_header(
        "📚 Study Planner",
        "오늘의 일정을 확인하세요",
    )
    
    # Quick stats
    stats_row = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Text("3", size=FontSizes.HEADLINE_LARGE, weight="bold", color=Colors.PRIMARY),
                        ft.Text("오늘의 과제", size=FontSizes.BODY_SMALL, color=Colors.TEXT_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=Colors.BACKGROUND,
                border_radius=8,
                padding=Spacing.MEDIUM,
                expand=True,
            ),
            ft.Container(
                ft.Column(
                    [
                        ft.Text("2", size=FontSizes.HEADLINE_LARGE, weight="bold", color=Colors.SECONDARY),
                        ft.Text("완료됨", size=FontSizes.BODY_SMALL, color=Colors.TEXT_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=Colors.BACKGROUND,
                border_radius=8,
                padding=Spacing.MEDIUM,
                expand=True,
            ),
            ft.Container(
                ft.Column(
                    [
                        ft.Text("1", size=FontSizes.HEADLINE_LARGE, weight="bold", color=Colors.ACCENT),
                        ft.Text("진행중", size=FontSizes.BODY_SMALL, color=Colors.TEXT_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=Colors.BACKGROUND,
                border_radius=8,
                padding=Spacing.MEDIUM,
                expand=True,
            ),
        ],
        spacing=Spacing.SMALL,
    )
    
    # Main action buttons
    action_buttons = ft.Column(
        [
            ft.Row(
                [
                    create_button(
                        "📅 일정 관리",
                        on_click=lambda _: on_schedule_click(),
                        size="large",
                    ),
                    create_button(
                        "🤖 AI 분석",
                        on_click=lambda _: on_ai_feedback_click(),
                        size="large",
                    ),
                ],
                spacing=Spacing.SMALL,
            ),
            ft.Row(
                [
                    create_button(
                        "👤 계정",
                        on_click=lambda _: on_account_click(),
                        size="large",
                    ),
                    ft.Container(expand=True),
                ],
                spacing=Spacing.SMALL,
            ),
        ],
        spacing=Spacing.SMALL,
    )
    
    # Recent schedules section
    recent_schedules = ft.Column(
        [
            ft.Text("📋 최근 일정", size=FontSizes.TITLE_MEDIUM, weight="bold"),
            create_card(
                title="수행평가 준비",
                subtitle="내일 10:00 | 높은 우선도",
                trailing=create_badge("HIGH", Colors.PRIORITY_HIGH),
            ),
            create_card(
                title="영어 단어 암기",
                subtitle="3일 뒤",
                trailing=create_badge("MEDIUM", Colors.PRIORITY_MEDIUM),
            ),
        ],
        spacing=Spacing.SMALL,
    )
    
    # Main container
    return ft.Column(
        [
            header,
            ft.Container(
                ft.Column(
                    [
                        ft.Text("오늘의 요약", size=FontSizes.TITLE_LARGE, weight="bold"),
                        stats_row,
                        ft.Divider(),
                        action_buttons,
                        ft.Divider(),
                        recent_schedules,
                    ],
                    spacing=Spacing.MEDIUM,
                ),
                padding=Spacing.MEDIUM,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
