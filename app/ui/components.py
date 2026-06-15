"""
Reusable UI components for the Study Planner App.

Provides common Flet components used throughout the application.
"""

from typing import Callable, Optional

import flet as ft

from app.ui.styles import Colors, FontSizes, Spacing, BorderRadius


def create_header(
    title: str,
    subtitle: Optional[str] = None,
    on_back: Optional[Callable] = None,
) -> ft.Container:
    """
    Create a header component with title and optional back button.
    
    Args:
        title: Header title
        subtitle: Optional subtitle text
        on_back: Optional callback for back button
    
    Returns:
        ft.Container: Header component
    """
    header_content = [
        ft.Text(
            title,
            size=FontSizes.HEADLINE_MEDIUM,
            color=Colors.TEXT_PRIMARY,
            weight="bold",
        )
    ]
    
    if subtitle:
        header_content.append(
            ft.Text(
                subtitle,
                size=FontSizes.BODY_MEDIUM,
                color=Colors.TEXT_SECONDARY,
            )
        )
    
    row_content = []
    if on_back:
        row_content.append(
            ft.IconButton(
                ft.icons.ARROW_BACK,
                on_click=lambda _: on_back(),
            )
        )
    
    row_content.append(
        ft.Column(
            header_content,
            spacing=Spacing.EXTRA_SMALL,
        )
    )
    
    return ft.Container(
        ft.Row(
            row_content,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=Spacing.MEDIUM,
        bgcolor=Colors.SURFACE,
    )


def create_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    variant: str = "contained",
    size: str = "medium",
) -> ft.Control:
    """
    Create a customized button.
    
    Args:
        text: Button text
        on_click: Click handler
        icon: Optional icon name
        variant: Button style ('contained', 'outlined', 'text')
        size: Button size ('small', 'medium', 'large')
    
    Returns:
        ft.Control: Button component
    """
    # Size configuration
    size_config = {
        "small": (80, 32),
        "medium": (120, 44),
        "large": (160, 56),
    }
    width, height = size_config.get(size, (120, 44))
    
    if variant == "contained":
        button = ft.ElevatedButton(
            text,
            icon=icon,
            width=width,
            height=height,
            on_click=on_click,
        )
    elif variant == "outlined":
        button = ft.OutlinedButton(
            text,
            icon=icon,
            width=width,
            height=height,
            on_click=on_click,
        )
    else:  # text variant
        button = ft.TextButton(
            text,
            icon=icon,
            on_click=on_click,
        )
    
    return button


def create_card(
    title: str,
    subtitle: Optional[str] = None,
    content: Optional[ft.Control] = None,
    on_click: Optional[Callable] = None,
    trailing: Optional[ft.Control] = None,
) -> ft.Card:
    """
    Create a styled card component.
    
    Args:
        title: Card title
        subtitle: Optional subtitle
        content: Optional main content
        on_click: Optional click handler
        trailing: Optional trailing widget (icon, badge, etc.)
    
    Returns:
        ft.Card: Card component
    """
    card_content = [
        ft.ListTile(
            title=ft.Text(title, size=FontSizes.TITLE_MEDIUM, weight="bold"),
            subtitle=ft.Text(subtitle, size=FontSizes.BODY_SMALL) if subtitle else None,
            trailing=trailing,
            on_click=on_click,
        )
    ]
    
    if content:
        card_content.append(
            ft.Container(
                content,
                padding=Spacing.MEDIUM,
            )
        )
    
    return ft.Card(
        ft.Column(
            card_content,
            spacing=0,
        ),
        margin=ft.margin.symmetric(vertical=Spacing.SMALL, horizontal=0),
    )


def create_badge(text: str, color: str = Colors.PRIMARY) -> ft.Container:
    """
    Create a badge component.
    
    Args:
        text: Badge text
        color: Badge background color
    
    Returns:
        ft.Container: Badge component
    """
    return ft.Container(
        ft.Text(
            text,
            size=FontSizes.LABEL_SMALL,
            color="white",
        ),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=Spacing.SMALL, vertical=2),
        border_radius=BorderRadius.ROUND,
    )


def create_input_field(
    label: str,
    placeholder: str = "",
    on_change: Optional[Callable] = None,
    multiline: bool = False,
    min_lines: int = 1,
) -> ft.TextField:
    """
    Create a styled input field.
    
    Args:
        label: Input label
        placeholder: Placeholder text
        on_change: Change handler
        multiline: Allow multiple lines
        min_lines: Minimum number of lines
    
    Returns:
        ft.TextField: Input field component
    """
    return ft.TextField(
        label=label,
        hint_text=placeholder,
        on_change=on_change,
        multiline=multiline,
        min_lines=min_lines,
        filled=True,
        border_color=Colors.TEXT_DISABLED,
    )


def create_loading_indicator() -> ft.Column:
    """
    Create a loading spinner.
    
    Returns:
        ft.Column: Loading indicator component
    """
    return ft.Column(
        [
            ft.ProgressRing(),
            ft.Text("Loading...", text_align="center"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=Spacing.MEDIUM,
    )
