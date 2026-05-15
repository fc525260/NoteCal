"""
农历工具模块

提供公历和农历之间的转换功能，依赖外部 lunarcalendar 库。
"""
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class LunarUtils:
    """农历工具类

    提供农历日期转换功能，封装了 lunarcalendar 库的接口。
    """

    LUNAR_MONTHS = [
        "", "正月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "十一月", "腊月"
    ]

    LUNAR_DAYS = [
        "", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
    ]

    def __init__(self) -> None:
        """初始化农历工具"""
        self.lunar_available: bool = self._check_lunar_library()
        self.converter: Any = None
        self.Solar: Any = None
        self.Lunar: Any = None

        if self.lunar_available:
            try:
                from lunarcalendar import Converter, Solar, Lunar
                self.converter = Converter()
                self.Solar = Solar
                self.Lunar = Lunar
                logger.debug("农历库初始化成功")
            except ImportError as e:
                logger.warning(f"农历库导入失败: {e}")
                self.lunar_available = False
            except Exception as e:
                logger.warning(f"农历库初始化异常: {e}")
                self.lunar_available = False

    def _check_lunar_library(self) -> bool:
        """检查农历库是否可用

        Returns:
            如果 lunarcalendar 库已安装则返回 True，否则返回 False
        """
        try:
            import lunarcalendar
            return True
        except ImportError:
            logger.warning(
                "lunarcalendar 库未安装，农历功能不可用。"
                "请运行 'pip install lunarcalendar' 安装农历库"
            )
            return False

    def is_available(self) -> bool:
        """检查农历功能是否可用

        Returns:
            如果农历功能可用则返回 True，否则返回 False
        """
        return self.lunar_available

    def get_lunar_date(self, year: int, month: int, day: int) -> Optional[str]:
        """获取指定公历日期对应的农历日期

        Args:
            year: 公历年
            month: 公历月
            day: 公历日

        Returns:
            农历日期字符串，格式为 "X月X日"，若转换失败返回 None
        """
        if not self.lunar_available:
            return None

        try:
            solar_date = self.Solar(year, month, day)
            lunar_date = self.converter.Solar2Lunar(solar_date)

            lunar_month = lunar_date.month
            lunar_day = lunar_date.day

            if 1 <= lunar_month <= 12:
                month_name = self.LUNAR_MONTHS[lunar_month]
            else:
                month_name = f"{lunar_month}月"

            if 1 <= lunar_day <= 30:
                day_name = self.LUNAR_DAYS[lunar_day]
            else:
                day_name = f"{lunar_day}日"

            if lunar_date.isleap:
                lunar_str = f"闰{month_name}{day_name}"
            else:
                lunar_str = f"{month_name}{day_name}"

            return lunar_str

        except Exception as e:
            logger.error(f"农历转换失败: {e}")
            return None