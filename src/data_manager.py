"""
数据管理模块

负责笔记和应用设置的持久化存储，提供数据加载、保存和访问接口。
"""
import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class DataManager:
    """数据管理器类

    处理应用数据的加载、保存和管理，包括用户笔记和应用设置。
    """

    def __init__(self, notes_file: str, settings_file: str) -> None:
        """初始化数据管理器

        Args:
            notes_file: 笔记数据存储文件路径
            settings_file: 设置数据存储文件路径
        """
        self.notes_path: str = notes_file
        self.settings_path: str = settings_file

        os.makedirs(os.path.dirname(self.notes_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)

        self.notes: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {
            "theme": "light",
            "minimize_to_tray": True,
            "show_lunar": True,
        }

    def load_notes(self) -> None:
        """加载笔记数据"""
        try:
            if os.path.exists(self.notes_path):
                with open(self.notes_path, "r", encoding="utf-8") as f:
                    self.notes = json.load(f)
                logger.info(f"已加载笔记数据: {self.notes_path}")
            else:
                logger.info("笔记文件不存在，使用空数据")
        except json.JSONDecodeError as e:
            logger.error(f"笔记文件格式错误: {e}")
            self.notes = {}
        except Exception as e:
            logger.error(f"加载笔记数据失败: {e}")
            self.notes = {}

    def save_notes(self) -> None:
        """保存笔记数据"""
        try:
            with open(self.notes_path, "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
            logger.debug(f"已保存笔记数据: {self.notes_path}")
        except Exception as e:
            logger.error(f"保存笔记数据失败: {e}")

    def load_settings(self) -> None:
        """加载设置"""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    for key, value in loaded_settings.items():
                        self.settings[key] = value
                logger.info(f"已加载设置: {self.settings_path}")
            else:
                logger.info("设置文件不存在，使用默认设置")
        except json.JSONDecodeError as e:
            logger.error(f"设置文件格式错误: {e}")
            self.settings = {
                "theme": "light",
                "minimize_to_tray": True,
                "show_lunar": True,
            }
        except Exception as e:
            logger.error(f"加载设置失败: {e}")
            self.settings = {
                "theme": "light",
                "minimize_to_tray": True,
                "show_lunar": True,
            }

    def save_settings(self) -> None:
        """保存设置"""
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            logger.debug(f"已保存设置: {self.settings_path}")
        except Exception as e:
            logger.error(f"保存设置失败: {e}")

    def get_note(self, date_str: str) -> tuple[str, bool, bool]:
        """获取指定日期的笔记、加班和出差状态

        Args:
            date_str: 日期字符串 (YYYY-MM-DD)

        Returns:
            (笔记内容, 是否加班, 是否出差) 元组，若无记录则返回 ("", False, False)
        """
        note_data = self.notes.get(date_str)
        if note_data is None:
            return "", False, False
        if isinstance(note_data, str):
            return note_data, False, False
        return (
            note_data.get("content", ""),
            note_data.get("overtime", False),
            note_data.get("business_trip", False),
        )

    def set_note(
        self,
        date_str: str,
        content: str,
        overtime: bool = False,
        business_trip: bool = False
    ) -> None:
        """设置指定日期的笔记、加班和出差状态

        Args:
            date_str: 日期字符串 (YYYY-MM-DD)
            content: 笔记内容
            overtime: 是否加班
            business_trip: 是否出差
        """
        if content.strip() or overtime or business_trip:
            self.notes[date_str] = {
                "content": content,
                "overtime": overtime,
                "business_trip": business_trip,
            }
        elif date_str in self.notes:
            del self.notes[date_str]

    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取设置值

        Args:
            key: 设置键名
            default: 默认值

        Returns:
            设置值，若不存在则返回默认值
        """
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """设置值

        Args:
            key: 设置键名
            value: 设置值
        """
        self.settings[key] = value
