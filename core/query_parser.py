"""
查询解析模块 - 解析用户输入的筛选条件
"""
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from config import (
    LOCATION_MAPPING,
    EDUCATION_MAPPING,
    TIME_RANGE_CONFIG,
    MAJOR_KEYWORDS,
)
from utils import logger


@dataclass
class SearchCriteria:
    """搜索条件数据类"""
    location: str = ""  # 地区
    education: str = ""  # 学历
    major: str = ""  # 专业方向
    time_range: str = "近1个月"  # 时效范围
    keyword: str = ""  # 综合关键词
    
    def is_valid(self) -> bool:
        """检查是否包含必要的搜索条件"""
        return bool(self.location or self.education or self.major or self.keyword)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "location": self.location,
            "education": self.education,
            "major": self.major,
            "time_range": self.time_range,
            "keyword": self.keyword,
        }


class QueryParser:
    """
    查询条件解析器
    
    负责解析用户输入的自然语言查询，提取结构化搜索条件
    """
    
    def __init__(self):
        self.location_keywords = set(LOCATION_MAPPING.keys())
        self.education_keywords = set(EDUCATION_MAPPING.keys())
        self.time_range_keywords = set(TIME_RANGE_CONFIG.keys())
        self.major_keywords = set(MAJOR_KEYWORDS.keys())
    
    def parse(self, query: str) -> SearchCriteria:
        """
        解析用户查询
        
        Args:
            query: 用户输入的查询字符串
            
        Returns:
            SearchCriteria: 解析后的搜索条件
        """
        if not query or not query.strip():
            return SearchCriteria()
        
        query = query.strip()
        logger.info(f"解析查询: {query}")
        
        criteria = SearchCriteria()
        
        # 解析地区
        criteria.location = self._extract_location(query)
        
        # 解析学历
        criteria.education = self._extract_education(query)
        
        # 解析时效范围
        criteria.time_range = self._extract_time_range(query)
        
        # 解析专业方向
        criteria.major = self._extract_major(query)
        
        # 构建综合关键词
        criteria.keyword = self._build_keyword(criteria, query)
        
        logger.info(f"解析结果: {criteria.to_dict()}")
        return criteria
    
    def _extract_location(self, query: str) -> str:
        """
        提取地区信息
        
        Args:
            query: 查询字符串
            
        Returns:
            str: 地区名称
        """
        # 直接匹配地区关键词
        for location in self.location_keywords:
            if location in query:
                return location
        
        # 模糊匹配（如"京"对应"北京"）
        fuzzy_mapping = {
            "京": "北京",
            "沪": "上海",
            "穗": "广州",
            "鹏城": "深圳",
            "杭": "杭州",
            "宁": "南京",
            "汉": "武汉",
            "蓉": "成都",
            "渝": "重庆",
            "津": "天津",
        }
        
        for fuzzy, location in fuzzy_mapping.items():
            if fuzzy in query:
                return location
        
        return ""
    
    def _extract_education(self, query: str) -> str:
        """
        提取学历要求
        
        Args:
            query: 查询字符串
            
        Returns:
            str: 学历要求
        """
        # 按学历层次从高到低匹配
        education_priority = ["博士", "博士后", "硕士", "研究生", "本科", "学士"]
        
        for edu in education_priority:
            if edu in query:
                return edu
        
        return ""
    
    def _extract_time_range(self, query: str) -> str:
        """
        提取时效范围
        
        Args:
            query: 查询字符串
            
        Returns:
            str: 时效范围描述
        """
        for time_range in self.time_range_keywords:
            if time_range in query:
                return time_range
        
        # 默认返回近1个月
        return "近1个月"
    
    def _extract_major(self, query: str) -> str:
        """
        提取专业方向
        
        Args:
            query: 查询字符串
            
        Returns:
            str: 专业方向
        """
        # 匹配专业关键词
        for major in self.major_keywords:
            if major in query.lower():
                return major
        
        # 匹配扩展关键词
        for major, keywords in MAJOR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query:
                    return major
        
        return ""
    
    def _build_keyword(self, criteria: SearchCriteria, original_query: str) -> str:
        """
        构建搜索关键词
        
        Args:
            criteria: 已解析的条件
            original_query: 原始查询
            
        Returns:
            str: 搜索关键词
        """
        keywords = []
        
        # 添加专业方向作为关键词
        if criteria.major:
            keywords.append(criteria.major)
        
        # 提取查询中可能包含的职位类型关键词
        job_types = ["教师", "教授", "副教授", "讲师", "博士后", "研究员", "工程师", "辅导员"]
        for job_type in job_types:
            if job_type in original_query:
                keywords.append(job_type)
                break
        
        # 如果关键词为空，使用原始查询（去除已知条件）
        if not keywords:
            # 移除已解析的条件
            remaining = original_query
            for condition in [criteria.location, criteria.education, criteria.time_range]:
                if condition:
                    remaining = remaining.replace(condition, "")
            
            remaining = remaining.strip("，,、 ")
            if remaining:
                keywords.append(remaining)
        
        return " ".join(keywords) if keywords else original_query
    
    def validate(self, criteria: SearchCriteria) -> tuple[bool, str]:
        """
        验证搜索条件
        
        Args:
            criteria: 搜索条件
            
        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        if not criteria.is_valid():
            return False, "请至少提供地区、学历或专业方向中的一个搜索条件"
        
        if not criteria.location:
            logger.warning("未指定地区，将搜索全国范围")
        
        if not criteria.education:
            logger.warning("未指定学历要求")
        
        if not criteria.major:
            logger.warning("未指定专业方向")
        
        return True, ""
    
    def format_criteria(self, criteria: SearchCriteria) -> str:
        """
        格式化搜索条件为可读字符串
        
        Args:
            criteria: 搜索条件
            
        Returns:
            str: 格式化的条件描述
        """
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
