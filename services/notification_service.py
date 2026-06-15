"""
Notification service for system notifications.
"""

import platform
import subprocess
from typing import Optional

from utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationService:
    """
    Sends system notifications to the user.
    """
    
    @staticmethod
    def send_notification(
        title: str,
        message: str,
        timeout: int = 5000,
    ) -> bool:
        """
        Send a system notification.
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Display timeout in milliseconds
        
        Returns:
            True if notification sent successfully
        """
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                return NotificationService._send_macos_notification(title, message)
            elif system == "Windows":
                return NotificationService._send_windows_notification(title, message)
            elif system == "Linux":
                return NotificationService._send_linux_notification(title, message, timeout)
            else:
                logger.warning(f"Notifications not supported on {system}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return False
    
    @staticmethod
    def _send_macos_notification(title: str, message: str) -> bool:
        """
        Send macOS notification using AppleScript.
        """
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)
            logger.info(f"macOS notification sent: {title}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS notification error: {str(e)}")
            return False
    
    @staticmethod
    def _send_windows_notification(title: str, message: str) -> bool:
        """
        Send Windows notification using PowerShell.
        """
        try:
            powershell_cmd = (
                f'[Windows.UI.Notifications.ToastNotificationManager, '
                f'Windows.UI.Notifications, ContentType = WindowsRuntime] > $null\n'
                f'[Windows.UI.Notifications.ToastNotification, '
                f'Windows.UI.Notifications, ContentType = WindowsRuntime] > $null\n'
                f'[Windows.Data.Xml.Dom.XmlDocument, '
                f'System.Xml.XmlDocument, ContentType = WindowsRuntime] > $null\n'
                f'$APP_ID = "StudyPlanner"\n'
                f'$template = @"\n'
                f'<toast>\n'
                f'  <visual>\n'
                f'    <binding template="ToastText02">\n'
                f'      <text id="1">{title}</text>\n'
                f'      <text id="2">{message}</text>\n'
                f'    </binding>\n'
                f'  </visual>\n'
                f'</toast>\n'
                f'"@\n'
                f'$xml = New-Object Windows.Data.Xml.Dom.XmlDocument\n'
                f'$xml.LoadXml($template)\n'
                f'$toast = New-Object Windows.UI.Notifications.ToastNotification $xml\n'
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)'
            )
            subprocess.run(["powershell", "-Command", powershell_cmd], check=True)
            logger.info(f"Windows notification sent: {title}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Windows notification error: {str(e)}")
            return False
    
    @staticmethod
    def _send_linux_notification(title: str, message: str, timeout: int) -> bool:
        """
        Send Linux notification using notify-send.
        """
        try:
            subprocess.run(
                ["notify-send", "-u", "normal", "-t", str(timeout), title, message],
                check=True,
            )
            logger.info(f"Linux notification sent: {title}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Linux notification error: {str(e)}")
            return False
