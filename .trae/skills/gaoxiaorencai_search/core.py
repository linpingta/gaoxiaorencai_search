"""
核心模块 - 搜索引擎和查询解析
"""
import time
import random
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

import requests

from utils import logger, LOCATION_MAPPING, EDUCATION_MAPPING, TIME_RANGE_CONFIG, MAJOR_KEYWORDS, SEARCH_CONFIG
from parsers import JobParser, JobInfo


@dataclass
class SearchCriteria:
    """搜索条件"""
    location: str = ""
    education: str = ""
    major: str = ""
    time_range: str = "近1个月"
    keyword: str = ""
    
    def is_valid(self) -> bool:
        return bool(self.location or self.education or self.major or self.keyword)


class QueryParser:
    """查询解析器"""
    
    def parse(self, query: str) -> SearchCriteria:
        """解析用户查询"""
        if not query:
            return SearchCriteria()
        
        query = query.strip()
        criteria = SearchCriteria()
        
        criteria.location = self._extract_location(query)
        criteria.education = self._extract_education(query)
        criteria.time_range = self._extract_time_range(query)
        criteria.major = self._extract_major(query)
        criteria.keyword = self._build_keyword(criteria, query)
        
        return criteria
    
    def _extract_location(self, query: str) -> str:
        """提取地区"""
        for location in LOCATION_MAPPING.keys():
            if location in query:
                return location
        
        # 模糊匹配
        fuzzy = {"京": "北京", "沪": "上海", "穗": "广州", "鹏城": "深圳", "杭": "杭州"}
        for k, v in fuzzy.items():
            if k in query:
                return v
        return ""
    
    def _extract_education(self, query: str) -> str:
        """提取学历"""
        priority = ["博士", "博士后", "硕士", "研究生", "本科", "学士"]
        for edu in priority:
            if edu in query:
                return edu
        return ""
    
    def _extract_time_range(self, query: str) -> str:
        """提取时效范围"""
        for tr in TIME_RANGE_CONFIG.keys():
            if tr in query:
                return tr
        return "近1个月"
    
    def _extract_major(self, query: str) -> str:
        """提取专业方向"""
        for major in MAJOR_KEYWORDS.keys():
            if major in query.lower():
                return major
        
        for major, keywords in MAJOR_KEYWORDS.items():
            for kw in keywords:
                if kw in query:
                    return major
        return ""
    
    def _build_keyword(self, criteria: SearchCriteria, original: str) -> str:
        """构建搜索关键词"""
        keywords = []
        if criteria.major:
            keywords.append(criteria.major)
        
        job_types = ["教师", "教授", "博士后", "研究员", "工程师", "辅导员"]
        for jt in job_types:
            if jt in original:
                keywords.append(jt)
                break
        
        if not keywords:
            remaining = original
            for cond in [criteria.location, criteria.education, criteria.time_range]:
                if cond:
                    remaining = remaining.replace(cond, "")
            remaining = remaining.strip("，,、 ")
            if remaining:
                keywords.append(remaining)
        
        return " ".join(keywords) if keywords else original
    
    def format_criteria(self, criteria: SearchCriteria) -> str:
        """格式化条件描述"""
        parts = []
        if criteria.location:
            parts.append(criteria.location)
        if criteria.education:
            parts.append(criteria.education)
        if criteria.major:
            parts.append(criteria.major)
        if criteria.time_range:
            parts.append(criteria.time_range)
        return "，".join(parts) if parts else "全部"


class SearchEngine:
    """搜索引擎 - 使用API获取数据"""
    
    BASE_URL = "https://www.gaoxiaojob.com"
    API_ENDPOINT = "/job/home-list"
    
    def __init__(self):
        self.session = requests.Session()
        self.timeout = SEARCH_CONFIG["timeout"]
        self.max_retries = SEARCH_CONFIG["max_retries"]
        self.retry_delay = SEARCH_CONFIG["retry_delay"]
        self._last_request_time = 0
        self._initialized = False
        
        # 设置请求头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.gaoxiaojob.com",
            "Referer": "https://www.gaoxiaojob.com/job",
            "X-Requested-With": "XMLHttpRequest",
        })
    
    def _init_session(self):
        """初始化session，访问首页获取cookie"""
        if self._initialized:
            return True
        
        try:
            logger.info("初始化session，访问首页...")
            resp = self.session.get(f"{self.BASE_URL}/job", timeout=self.timeout)
            if resp.status_code == 200:
                self._initialized = True
                logger.info(f"Session初始化成功，cookies: {self.session.cookies.get_dict()}")
                return True
            else:
                logger.warning(f"首页访问失败: {resp.status_code}")
                return False
        except Exception as e:
            logger.error(f"初始化session失败: {e}")
            return False
    
    def _wait_rate_limit(self):
        """等待请求间隔"""
        min_interval = SEARCH_CONFIG["request_delay"]
        elapsed = time.time() - self._last_request_time
        if elapsed < min_interval:
            sleep_time = min_interval - elapsed + random.uniform(0.5, 1.5)
            logger.info(f"等待 {sleep_time:.1f} 秒...")
            time.sleep(sleep_time)
        self._last_request_time = time.time()
    
    def search(self, keyword: str = "", location: str = "", education: str = "", page: int = 1, page_size: int = 50) -> Optional[Dict[str, Any]]:
        """执行搜索，返回JSON数据"""
        self._wait_rate_limit()
        
        # 确保session已初始化
        if not self._init_session():
            logger.error("Session初始化失败")
            return None
        
        # 构建请求参数
        params = {
            "page": page,
            "pageSize": page_size,
        }
        
        if keyword:
            params["keyword"] = keyword
        
        if location and location in LOCATION_MAPPING:
            params["workplace"] = LOCATION_MAPPING[location]
        
        if education and education in EDUCATION_MAPPING:
            params["education"] = EDUCATION_MAPPING[education]
        
        url = f"{self.BASE_URL}{self.API_ENDPOINT}"
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"搜索API: {url}, 参数: {params}")
                response = self.session.post(url, data=params, timeout=self.timeout)
                response.raise_for_status()
                
                # 解析JSON响应
                data = response.json()
                
                # 检查响应状态
                if data.get("result") == 1:
                    logger.info(f"搜索成功，获取到数据")
                    return data.get("data", {})
                else:
                    logger.warning(f"API返回错误: {data.get('msg', '未知错误')}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
                    else:
                        return None
                
            except requests.exceptions.Timeout:
                logger.warning(f"超时，重试 {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
            except ValueError as e:
                logger.error(f"JSON解析失败: {e}")
                return None
        
        return None


class ResultFormatter:
    """结果格式化器"""
    
    def format(self, jobs: List[JobInfo], criteria_desc: str, total: int = 0) -> str:
        """格式化结果"""
        if not jobs:
            return self._format_empty(criteria_desc)
        
        lines = [
            f"【高校人才网-实时搜索结果】（筛选条件：{criteria_desc}）",
            "",
            f"共找到 {total or len(jobs)} 条招聘信息，显示前 {len(jobs)} 条：",
            "",
        ]
        
        for idx, job in enumerate(jobs[:50], 1):
            lines.append(self._format_job(job, idx))
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_job(self, job: JobInfo, idx: int) -> str:
        """格式化单个职位"""
        lines = []
        
        urgent = "【急聘】" if job.is_urgent else ""
        bianzhi = "【有编制】" if job.has_bianzhi else ""
        lines.append(f"{idx}. {urgent}{bianzhi}{job.title}")
        lines.append(f"   招聘单位：{job.company}（{job.company_type}）")
        
        if job.location != "未公开":
            lines.append(f"   工作地点：{job.location}")
        if job.education != "未公开":
            lines.append(f"   学历要求：{job.education}")
        if job.major != "未公开":
            lines.append(f"   专业方向：{job.major}")
        if job.recruit_num != "未公开":
            lines.append(f"   招聘人数：{job.recruit_num}")
        if job.publish_date:
            lines.append(f"   发布时间：{job.publish_date}")
        if job.salary:
            lines.append(f"   薪资待遇：{job.salary}")
        if job.benefits != "未公开":
            benefits = job.benefits[:80] + "..." if len(job.benefits) > 80 else job.benefits
            lines.append(f"   福利待遇：{benefits}")
        if job.url:
            lines.append(f"   详情链接：{job.url}")
        
        return "\n".join(lines)
    
    def _format_empty(self, criteria_desc: str, is_access_error: bool = False) -> str:
        """格式化空结果"""
        if is_access_error:
            return f"""【高校人才网-实时搜索结果】（筛选条件：{criteria_desc}）

暂时无法访问高校人才网，可能原因：
1. 网站访问频率限制，请稍后重试
2. 网络连接问题

建议：
1. 等待几分钟后重试
2. 直接访问官网查看：https://www.gaoxiaojob.com
3. 调整搜索条件后重试"""

        return f"""【高校人才网-实时搜索结果】（筛选条件：{criteria_desc}）

未找到符合条件的招聘信息，建议：
1. 调整筛选条件（如放宽地区、学历要求）
2. 更换专业方向关键词
3. 扩大时间范围
4. 稍后重试"""


def search(query: str) -> str:
    """便捷搜索函数"""
    service = SearchService()
    return service.search(query)


class SearchService:
    """搜索服务"""
    
    def __init__(self):
        self.engine = SearchEngine()
        self.parser = QueryParser()
        self.job_parser = JobParser()
        self.formatter = ResultFormatter()
    
    def search_jobs(self, query: str) -> list:
        """执行搜索并返回职位列表"""
        criteria = self.parser.parse(query)
        if not criteria.is_valid():
            return []
        
        # 调用API获取数据
        data = self.engine.search(
            keyword=criteria.keyword,
            location=criteria.location,
            education=criteria.education,
            page_size=50
        )
        
        if data is None:
            return []
        
        # 解析职位列表
        jobs = self.job_parser.parse_api_response(data)
        
        # 应用筛选条件
        if criteria.major:
            jobs = self.job_parser.filter_by_major(jobs, criteria.major)
        jobs = self.job_parser.filter_by_time_range(jobs, criteria.time_range)
        jobs = self.job_parser.deduplicate_jobs(jobs)
        jobs = self.job_parser.sort_jobs(jobs)
        
        return jobs
    
    def search(self, query: str) -> str:
        """执行搜索"""
        try:
            criteria = self.parser.parse(query)
            if not criteria.is_valid():
                return "请至少提供地区、学历或专业方向中的一个搜索条件"
            
            criteria_desc = self.parser.format_criteria(criteria)
            logger.info(f"搜索: {criteria_desc}")
            
            # 调用API
            data = self.engine.search(
                keyword=criteria.keyword,
                location=criteria.location,
                education=criteria.education,
                page_size=50
            )
            
            if data is None:
                # 访问失败，返回友好的错误提示
                return self.formatter._format_empty(criteria_desc, is_access_error=True)
            
            # 解析职位列表
            jobs = self.job_parser.parse_api_response(data)
            total = len(jobs)
            
            # 应用筛选条件
            if criteria.major:
                jobs = self.job_parser.filter_by_major(jobs, criteria.major)
            jobs = self.job_parser.filter_by_time_range(jobs, criteria.time_range)
            jobs = self.job_parser.deduplicate_jobs(jobs)
            jobs = self.job_parser.sort_jobs(jobs)
            
            if not jobs:
                return self.formatter._format_empty(criteria_desc, is_access_error=False)
            
            return self.formatter.format(jobs, criteria_desc, total)
            
        except Exception as e:
            logger.exception("搜索异常")
            return f"搜索失败: {str(e)}\n\n建议直接访问官网查看：https://www.gaoxiaojob.com"
