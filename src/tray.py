"""
System tray interface for Canvus-Local-LLM.

This module handles the Windows system tray icon and menu.
"""

from infi.systray import SysTrayIcon
from typing import Callable, Optional
import webbrowser
import os
from PIL import Image

class CanvusTray:
    """Manages the system tray icon and menu."""
    
    def __init__(self, on_restart: Callable, on_settings_change: Callable[[str, str], None], get_status: Optional[Callable[[], str]] = None):
        """Initialize the tray icon."""
        self.on_restart = on_restart
        self.on_settings_change = on_settings_change
        self.get_status = get_status or (lambda: "Idle")
        self.tray_icon: Optional[SysTrayIcon] = None
        self.icon_state = "default"  # can be 'default', 'connected', 'processing', 'error'
        self.icon_paths = {
            "default": "assets/icon.ico",
            "connected": "assets/icon_connected.ico",
            "processing": "assets/icon_processing.ico",
            "error": "assets/icon_error.ico"
        }
        self.tooltip = "Canvus-Local-LLM"
    
    def start_tray(self) -> None:
        """Start the system tray icon with hierarchical menu."""
        settings_menu = (
            ("Set Server Address", None, lambda s: self._handle_setting('server', 'Enter server URL:')),
            ("Set API Key", None, lambda s: self._handle_setting('api_key', 'Enter API Key:')),
            ("Set Username", None, lambda s: self._handle_setting('username', 'Enter Username:')),
            ("Set Password", None, lambda s: self._handle_setting('password', 'Enter Password:')),
            ("Select Model", None, lambda s: self._handle_setting('model', 'Enter Model Name:')),
        )
        menu_options = (
            ("Restart", None, self._handle_restart),
            ("Settings", settings_menu),
            ("Show Status", None, self._show_status),
            ("Exit", None, self._handle_exit),
        )
        self.tray_icon = SysTrayIcon(
            self.icon_paths[self.icon_state],
            self.tooltip,
            menu_options,
            on_quit=self._handle_exit,
        )
        self.tray_icon.start()
    
    def set_icon_state(self, state: str) -> None:
        """Set the tray icon state (default, connected, processing, error)."""
        if state in self.icon_paths:
            self.icon_state = state
            if self.tray_icon:
                self.tray_icon.icon = self.icon_paths[state]
    
    def set_tooltip(self, text: str) -> None:
        """Set the tray icon tooltip."""
        self.tooltip = text
        if self.tray_icon:
            self.tray_icon.hover_text = text
    
    def _handle_restart(self, systray: SysTrayIcon) -> None:
        """Handle restart menu item."""
        self.on_restart()
    
    def _handle_setting(self, key: str, prompt: str) -> None:
        """Handle setting changes (console-based for now)."""
        value = input(prompt)
        self.on_settings_change(key, value)
    
    def _show_status(self, systray: SysTrayIcon) -> None:
        """Show current status in a console dialog (for now)."""
        status = self.get_status()
        print(f"Current Status: {status}")
    
    def _handle_exit(self, systray: SysTrayIcon) -> None:
        """Handle exit menu item."""
        if self.tray_icon:
            self.tray_icon.shutdown()
        os._exit(0) 