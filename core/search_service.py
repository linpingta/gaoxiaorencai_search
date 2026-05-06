"""
搜索服务模块 - 整合搜索流程的主服务类
"""
from typing import List, Optional

from core import SearchEngine, QueryParser, SearchCriteria, ResultFormatter
from parsers import JobParser, JobInfo
from utils import logger


class SearchService:
    """
    搜索服务类
    
    整合查询解析、搜索执行、结果解析和格式化输出的完整流程
    """
    
    def __init__(self):
        self.search_engine = SearchEngine()
        self.query_parser = QueryParser()
        self.job_parser = JobParser()
        self.formatter = ResultFormatter()
    
    def search(self, query: str) -> str:
        """
        执行搜索并返回格式化结果
        
        Args:
            query: 用户查询字符串
            
        Returns:
            str: 格式化的搜索结果
        """
        try:
            # 1. 解析查询条件
            criteria = self.query_parser.parse(query)
            
            # 验证查询条件
            is_valid, error_msg = self.query_parser.validate(criteria)
            if not is_valid:
                return self.formatter.format_error(error_msg)
            
            criteria_desc = self.query_parser.format_criteria(criteria)
            logger.info(f"开始搜索: {criteria_desc}")
            
            # 2. 执行搜索
            html = self.search_engine.search(
                keyword=criteria.keyword,
                location=criteria.location,
                education=criteria.education,
                page=1
            )
            
            if html is None:
                return self.formatter.format_error(
                    "当前高校人才网访问异常，请稍后重试"
                )
            
            # 3. 解析搜索结果
            jobs = self.job_parser.parse_job_list(html)
            total_found = len(jobs)
            logger.info(f"解析到 {total_found} 个职位")
            
            # 4. 按专业方向筛选
            if criteria.major:
                jobs = self.job_parser.filter_by_major(jobs, criteria.major)
                logger.info(f"专业筛选后剩余 {len(jobs)} 个职位")
            
            # 5. 按时间范围筛选
            jobs = self.job_parser.filter_by_time_range(jobs, criteria.time_range)
            logger.info(f"时间筛选后剩余 {len(jobs)} 个职位")
            
            # 6. 去重
            jobs = self.job_parser.deduplicate_jobs(jobs)
            logger.info(f"去重后剩余 {len(jobs)} 个职位")
            
            # 7. 排序
            jobs = self.job_parser.sort_jobs(jobs)
            
            # 8. 格式化输出
            return self.formatter.format(jobs, criteria_desc, total_found)
            
        except Exception as e:
            logger.exception("搜索过程发生异常")
            return self.formatter.format_error(f"搜索异常: {str(e)}")
    
    def search_jobs(self, query: str) -> List[JobInfo]:
        """
        执行搜索并返回职位对象列表
        
        Args:
            query: 用户查询字符串
            
        Returns:
            List[JobInfo]: 职位信息列表
        """
        try:
            # 解析查询条件
            criteria = self.query_parser.parse(query)
            
            if not criteria.is_valid():
                logger.warning("搜索条件无效")
                return []
            
            # 执行搜索
            html = self.search_engine.search(
                keyword=criteria.keyword,
                location=criteria.location,
                education=criteria.education,
                page=1
            )
            
            if html is None:
                return []
            
            # 解析和筛选
            jobs = self.job_parser.parse_job_list(html)
            
            if criteria.major:
                jobs = self.job_parser.filter_by_major(jobs, criteria.major)
            
            jobs = self.job_parser.filter_by_time_range(jobs, criteria.time_range)
            jobs = self.job_parser.deduplicate_jobs(jobs)
            jobs = self.job_parser.sort_jobs(jobs)
            
            return jobs
            
        except Exception as e:
            logger.exception("搜索过程发生异常")
            return []
    
    def search_with_criteria(self, criteria: SearchCriteria) -> str:
        """
        使用已解析的条件执行搜索
        
        Args:
            criteria: 搜索条件对象
            
        Returns:
            str: 格式化的搜索结果
        """
        try:
            if not criteria.is_valid():
                return self.formatter.format_error("搜索条件无效")
            
            criteria_desc = self.query_parser.format_criteria(criteria)
            logger.info(f"开始搜索: {criteria_desc}")
            
            html = self.search_engine.search(
                keyword=criteria.keyword,
                location=criteria.location,
                education=criteria.education,
                page=1
            )
            
            if html is None:
                return self.formatter.format_error(
                    "当前高校人才网访问异常，请稍后重试"
                )
            
            jobs = self.job_parser.parse_job_list(html)
            total_found = len(jobs)
            
            if criteria.major:
                jobs = self.job_parser.filter_by_major(jobs, criteria.major)
            
            jobs = self.job_parser.filter_by_time_range(jobs, criteria.time_range)
            jobs = self.job_parser.deduplicate_jobs(jobs)
            jobs = self.job_parser.sort_jobs(jobs)
            
            return self.formatter.format(jobs, criteria_desc, total_found)
            
        except Exception as e:
            logger.exception("搜索过程发生异常")
            return self.formatter.format_error(f"搜索异常: {str(e)}")


# 全局搜索服务实例
_search_service: Optional[SearchService] = None


def get_search_service() -> SearchService:
    """
    获取搜索服务单例
    
    Returns:
        SearchService: 搜索服务实例
    """
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service


def search(query: str) -> str:
    """
    便捷搜索函数
    
    Args:
        query: 用户查询字符串
        
    Returns:
        str: 格式化的搜索结果
    """
    service = get_search_service()
    return service.search(query)
