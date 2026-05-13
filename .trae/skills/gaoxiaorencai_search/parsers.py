"""
解析模块 - HTML解析和数据提取
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from bs4 import BeautifulSoup

from utils import logger, normalize_date, MAJOR_KEYWORDS, TIME_RANGE_CONFIG


@dataclass
class JobInfo:
    """职位信息数据类"""
    title: str = ""
    company: str = ""
    company_type: str = ""
    location: str = ""
    education: str = ""
    major: str = ""
    publish_date: str = ""
    salary: str = ""
    benefits: str = ""
    url: str = ""
    recruit_num: str = ""
    is_urgent: bool = False
    has_bianzhi: bool = False


class JobParser:
    """职位信息解析器"""
    
    def parse_job_list(self, html: str) -> List[JobInfo]:
        """解析职位列表页面"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        # 尝试多种选择器
        selectors = [
            ".job-list .job-item",
            ".position-list .position-item",
            ".list-item",
            ".job-box",
            ".search-item",
        ]
        
        job_items = []
        for selector in selectors:
            job_items = soup.select(selector)
            if job_items:
                logger.info(f"找到 {len(job_items)} 个职位项")
                break
        
        # 如果没找到，尝试通用方式
        if not job_items:
            job_items = soup.find_all("div", class_=lambda x: x and ("job" in x.lower() if x else False))
        
        for item in job_items:
            try:
                job = self._parse_job_item(item)
                if job and job.title:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"解析职位项失败: {e}")
                continue
        
        logger.info(f"成功解析 {len(jobs)} 个职位")
        return jobs
    
    def _parse_job_item(self, item) -> Optional[JobInfo]:
        """解析单个职位项"""
        try:
            # 提取职位名称
            title = self._extract_text(item, [".job-title", ".title", "h3", "h4", "a"])
            if not title:
                return None
            
            # 提取其他字段
            company = self._extract_text(item, [".company", ".enterprise", ".org-name"])
            location = self._extract_text(item, [".location", ".workplace", ".city"])
            education = self._extract_text(item, [".education", ".degree"])
            publish_date = self._extract_text(item, [".date", ".time", ".publish-date"])
            salary = self._extract_text(item, [".salary", ".wage", ".pay"])
            company_type = self._extract_text(item, [".company-type", ".org-type"])
            major = self._extract_text(item, [".major", ".specialty"])
            benefits = self._extract_text(item, [".benefits", ".welfare"])
            recruit_num = self._extract_text(item, [".recruit-num", ".headcount"])
            
            # 提取链接
            url = self._extract_url(item)
            
            # 判断标签
            is_urgent = "急聘" in item.get_text() or bool(item.find(class_=lambda x: x and "urgent" in x.lower() if x else False))
            has_bianzhi = "编制" in item.get_text() or "事业编" in item.get_text()
            
            return JobInfo(
                title=title.strip(),
                company=company.strip() if company else "未公开",
                company_type=company_type.strip() if company_type else "未公开",
                location=location.strip() if location else "未公开",
                education=education.strip() if education else "未公开",
                major=major.strip() if major else "未公开",
                publish_date=normalize_date(publish_date),
                salary=salary.strip() if salary else "面议",
                benefits=benefits.strip() if benefits else "未公开",
                url=url,
                recruit_num=recruit_num.strip() if recruit_num else "未公开",
                is_urgent=is_urgent,
                has_bianzhi=has_bianzhi
            )
        except Exception as e:
            logger.warning(f"解析异常: {e}")
            return None
    
    def _extract_text(self, item, selectors: List[str]) -> str:
        """使用多个选择器提取文本"""
        for selector in selectors:
            elem = item.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_url(self, item) -> str:
        """提取详情链接"""
        link = item.find("a", href=True)
        if link:
            href = link["href"]
            if href.startswith("http"):
                return href
            elif href.startswith("/"):
                return f"https://www.gaoxiaojob.com{href}"
            else:
                return f"https://www.gaoxiaojob.com/{href}"
        return ""
    
    def filter_by_time_range(self, jobs: List[JobInfo], time_range: str) -> List[JobInfo]:
        """按时间范围筛选"""
        if not time_range or time_range not in TIME_RANGE_CONFIG:
            return jobs
        
        days = TIME_RANGE_CONFIG[time_range]
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered = []
        for job in jobs:
            try:
                if job.publish_date:
                    job_date = datetime.strptime(job.publish_date, "%Y-%m-%d")
                    if job_date >= cutoff_date:
                        filtered.append(job)
                else:
                    filtered.append(job)
            except ValueError:
                filtered.append(job)
        
        return filtered
    
    def filter_by_major(self, jobs: List[JobInfo], major_keyword: str) -> List[JobInfo]:
        """按专业方向筛选"""
        if not major_keyword:
            return jobs
        
        related_keywords = [major_keyword]
        for key, keywords in MAJOR_KEYWORDS.items():
            if major_keyword.lower() in key or key in major_keyword.lower():
                related_keywords.extend(keywords)
        
        related_keywords = list(set(related_keywords))
        
        filtered = []
        for job in jobs:
            text = f"{job.title} {job.major} {job.company}".lower()
            for keyword in related_keywords:
                if keyword.lower() in text:
                    filtered.append(job)
                    break
        
        return filtered
    
    def deduplicate_jobs(self, jobs: List[JobInfo]) -> List[JobInfo]:
        """去重职位"""
        seen = set()
        unique = []
        for job in jobs:
            key = f"{job.title}_{job.company}_{job.location}"
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique
    
    def sort_jobs(self, jobs: List[JobInfo]) -> List[JobInfo]:
        """按发布时间排序"""
        def sort_key(job):
            try:
                if job.publish_date:
                    return datetime.strptime(job.publish_date, "%Y-%m-%d")
            except ValueError:
                pass
            return datetime.min
        return sorted(jobs, key=sort_key, reverse=True)
