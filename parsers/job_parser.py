"""
职位解析模块 - 解析HTML提取职位信息
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup

from config import MAJOR_KEYWORDS, TIME_RANGE_CONFIG
from utils import logger


@dataclass
class JobInfo:
    """职位信息数据类"""
    title: str  # 职位名称
    company: str  # 招聘单位
    company_type: str  # 单位类型
    location: str  # 工作地点
    education: str  # 学历要求
    major: str  # 专业方向
    publish_date: str  # 发布时间 (YYYY-MM-DD)
    salary: str  # 薪资
    benefits: str  # 福利待遇
    url: str  # 详情链接
    job_type: str = ""  # 职位类型
    recruit_num: str = ""  # 招聘人数
    is_urgent: bool = False  # 是否急聘
    has_bianzhi: bool = False  # 是否有编制


class JobParser:
    """
    职位信息解析器
    
    负责解析搜索结果页面HTML，提取职位信息
    """
    
    def __init__(self):
        self.current_year = datetime.now().year
    
    def parse_job_list(self, html: str) -> List[JobInfo]:
        """
        解析职位列表页面
        
        Args:
            html: 页面HTML内容
            
        Returns:
            List[JobInfo]: 职位信息列表
        """
        if not html:
            return []
        
        soup = BeautifulSoup(html, "lxml")
        jobs = []
        
        # 尝试多种选择器定位职位列表项
        selectors = [
            ".job-list .job-item",
            ".position-list .position-item",
            ".list-item",
            ".job-box",
            ".position-box",
            ".recruit-list-item",
            ".search-item",
        ]
        
        job_items = []
        for selector in selectors:
            job_items = soup.select(selector)
            if job_items:
                logger.debug(f"使用选择器 '{selector}' 找到 {len(job_items)} 个职位")
                break
        
        # 如果没找到，尝试更通用的方式
        if not job_items:
            # 查找包含职位链接的div
            job_items = soup.find_all("div", class_=lambda x: x and ("job" in x.lower() or "position" in x.lower()))
        
        for item in job_items:
            try:
                job = self._parse_job_item(item)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"解析职位项失败: {e}")
                continue
        
        logger.info(f"成功解析 {len(jobs)} 个职位")
        return jobs
    
    def _parse_job_item(self, item: BeautifulSoup) -> Optional[JobInfo]:
        """
        解析单个职位项
        
        Args:
            item: 职位项HTML元素
            
        Returns:
            Optional[JobInfo]: 职位信息对象
        """
        try:
            # 提取职位名称
            title = self._extract_text(item, [
                ".job-title", ".position-title", ".title",
                "h3", "h4", ".name", "a"
            ])
            
            if not title:
                return None
            
            # 提取单位名称
            company = self._extract_text(item, [
                ".company-name", ".enterprise", ".org-name",
                ".company", ".unit"
            ])
            
            # 提取工作地点
            location = self._extract_text(item, [
                ".location", ".workplace", ".city",
                ".address", ".place"
            ])
            
            # 提取学历要求
            education = self._extract_text(item, [
                ".education", ".degree", ".edu-require",
                ".qualification"
            ])
            
            # 提取发布时间
            publish_date = self._extract_text(item, [
                ".publish-date", ".date", ".time",
                ".post-time", ".release-date"
            ])
            publish_date = self._normalize_date(publish_date)
            
            # 提取薪资
            salary = self._extract_text(item, [
                ".salary", ".wage", ".pay",
                ".compensation", ".money"
            ])
            
            # 提取详情链接
            url = self._extract_url(item)
            
            # 提取单位类型
            company_type = self._extract_text(item, [
                ".company-type", ".org-type", ".unit-type",
                ".nature"
            ])
            
            # 提取专业要求
            major = self._extract_text(item, [
                ".major", ".specialty", ".profession",
                ".subject", ".field"
            ])
            
            # 提取福利待遇
            benefits = self._extract_text(item, [
                ".benefits", ".welfare", ".perks",
                ".treatment"
            ])
            
            # 提取招聘人数
            recruit_num = self._extract_text(item, [
                ".recruit-num", ".headcount", ".number",
                ".count"
            ])
            
            # 判断是否急聘
            is_urgent = bool(item.find(class_=lambda x: x and "urgent" in x.lower())) or \
                       "急聘" in item.get_text()
            
            # 判断是否有编制
            has_bianzhi = "编制" in item.get_text() or \
                         "事业编" in item.get_text()
            
            return JobInfo(
                title=title.strip(),
                company=company.strip() if company else "未公开",
                company_type=company_type.strip() if company_type else "未公开",
                location=location.strip() if location else "未公开",
                education=education.strip() if education else "未公开",
                major=major.strip() if major else "未公开",
                publish_date=publish_date,
                salary=salary.strip() if salary else "面议",
                benefits=benefits.strip() if benefits else "未公开",
                url=url,
                recruit_num=recruit_num.strip() if recruit_num else "未公开",
                is_urgent=is_urgent,
                has_bianzhi=has_bianzhi
            )
            
        except Exception as e:
            logger.warning(f"解析职位项异常: {e}")
            return None
    
    def _extract_text(self, item: BeautifulSoup, selectors: List[str]) -> str:
        """
        使用多个选择器尝试提取文本
        
        Args:
            item: HTML元素
            selectors: CSS选择器列表
            
        Returns:
            str: 提取的文本
        """
        for selector in selectors:
            elem = item.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_url(self, item: BeautifulSoup) -> str:
        """
        提取详情链接
        
        Args:
            item: HTML元素
            
        Returns:
            str: 链接URL
        """
        # 尝试多种方式提取链接
        link_elem = item.find("a", href=True)
        if link_elem:
            href = link_elem["href"]
            if href.startswith("http"):
                return href
            elif href.startswith("/"):
                return f"https://www.gaoxiaojob.com{href}"
            else:
                return f"https://www.gaoxiaojob.com/{href}"
        return ""
    
    def _normalize_date(self, date_str: str) -> str:
        """
        标准化日期格式
        
        Args:
            date_str: 原始日期字符串
            
        Returns:
            str: YYYY-MM-DD格式的日期
        """
        if not date_str:
            return ""
        
        date_str = date_str.strip()
        
        # 匹配 "MM-DD发布" 格式
        match = re.match(r"(\d{1,2})-(\d{1,2})", date_str)
        if match:
            month, day = match.groups()
            return f"{self.current_year}-{int(month):02d}-{int(day):02d}"
        
        # 匹配 "YYYY-MM-DD" 格式
        match = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # 匹配 "今天"、"昨天"、"前天"
        today = datetime.now()
        if "今天" in date_str:
            return today.strftime("%Y-%m-%d")
        elif "昨天" in date_str:
            yesterday = today - timedelta(days=1)
            return yesterday.strftime("%Y-%m-%d")
        elif "前天" in date_str:
            before_yesterday = today - timedelta(days=2)
            return before_yesterday.strftime("%Y-%m-%d")
        
        return date_str
    
    def filter_by_time_range(
        self,
        jobs: List[JobInfo],
        time_range: str
    ) -> List[JobInfo]:
        """
        按时间范围筛选职位
        
        Args:
            jobs: 职位列表
            time_range: 时间范围描述（如"近1个月"）
            
        Returns:
            List[JobInfo]: 筛选后的职位列表
        """
        if not time_range or time_range not in TIME_RANGE_CONFIG:
            return jobs
        
        days = TIME_RANGE_CONFIG[time_range]
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered_jobs = []
        for job in jobs:
            try:
                if job.publish_date:
                    job_date = datetime.strptime(job.publish_date, "%Y-%m-%d")
                    if job_date >= cutoff_date:
                        filtered_jobs.append(job)
                else:
                    # 如果没有日期，默认保留
                    filtered_jobs.append(job)
            except ValueError:
                # 日期解析失败，默认保留
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def filter_by_major(
        self,
        jobs: List[JobInfo],
        major_keyword: str
    ) -> List[JobInfo]:
        """
        按专业方向筛选职位
        
        Args:
            jobs: 职位列表
            major_keyword: 专业方向关键词
            
        Returns:
            List[JobInfo]: 筛选后的职位列表
        """
        if not major_keyword:
            return jobs
        
        # 获取相关关键词列表
        related_keywords = [major_keyword]
        for key, keywords in MAJOR_KEYWORDS.items():
            if major_keyword.lower() in key or key in major_keyword.lower():
                related_keywords.extend(keywords)
        
        # 去重
        related_keywords = list(set(related_keywords))
        
        filtered_jobs = []
        for job in jobs:
            text_to_search = f"{job.title} {job.major} {job.company}".lower()
            for keyword in related_keywords:
                if keyword.lower() in text_to_search:
                    filtered_jobs.append(job)
                    break
        
        return filtered_jobs
    
    def deduplicate_jobs(self, jobs: List[JobInfo]) -> List[JobInfo]:
        """
        去重职位列表
        
        Args:
            jobs: 职位列表
            
        Returns:
            List[JobInfo]: 去重后的职位列表
        """
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # 使用"职位名称+单位+地点"作为唯一标识
            key = f"{job.title}_{job.company}_{job.location}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def sort_jobs(self, jobs: List[JobInfo]) -> List[JobInfo]:
        """
        排序职位列表（按发布时间倒序）
        
        Args:
            jobs: 职位列表
            
        Returns:
            List[JobInfo]: 排序后的职位列表
        """
        def sort_key(job: JobInfo):
            try:
                if job.publish_date:
                    return datetime.strptime(job.publish_date, "%Y-%m-%d")
            except ValueError:
                pass
            return datetime.min
        
        return sorted(jobs, key=sort_key, reverse=True)
