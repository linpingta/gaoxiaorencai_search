"""
核心搜索模块 - 负责构造请求和获取搜索结果
"""
import time
import random
from typing import Optional, Dict, Any
from urllib.parse import urlencode, urljoin

import requests
from fake_useragent import UserAgent

from config import (
    JOB_LIST_URL,
    SEARCH_CONFIG,
    DEFAULT_HEADERS,
    LOCATION_MAPPING,
    EDUCATION_MAPPING,
)
from utils import logger


class SearchEngine:
    """
    高校人才网搜索引擎
    
    负责构造搜索请求、发送HTTP请求、获取搜索结果页面
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.timeout = SEARCH_CONFIG["timeout"]
        self.max_retries = SEARCH_CONFIG["max_retries"]
        self.retry_delay = SEARCH_CONFIG["retry_delay"]
        self._last_request_time = 0
        
    def _get_headers(self) -> Dict[str, str]:
        """
        获取随机User-Agent的请求头
        
        Returns:
            Dict[str, str]: 请求头字典
        """
        headers = DEFAULT_HEADERS.copy()
        headers["User-Agent"] = self.ua.random
        return headers
    
    def _wait_for_rate_limit(self):
        """
        等待请求间隔，避免请求过于频繁
        """
        min_interval = SEARCH_CONFIG["request_delay"]
        elapsed = time.time() - self._last_request_time
        if elapsed < min_interval:
            sleep_time = min_interval - elapsed + random.uniform(0.5, 1.5)
            time.sleep(sleep_time)
        self._last_request_time = time.time()
    
    def _make_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        retries: int = 0
    ) -> Optional[str]:
        """
        发送HTTP请求并返回响应内容
        
        Args:
            url: 请求URL
            params: URL参数
            retries: 当前重试次数
            
        Returns:
            Optional[str]: 响应HTML内容，失败返回None
        """
        self._wait_for_rate_limit()
        
        headers = self._get_headers()
        
        try:
            logger.debug(f"发送请求: {url}, 参数: {params}")
            
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            response.raise_for_status()
            
            # 检查是否需要验证码
            if "验证码" in response.text or "captcha" in response.text.lower():
                logger.warning("检测到验证码，需要人工验证")
                return None
            
            logger.debug(f"请求成功，响应长度: {len(response.text)}")
            return response.text
            
        except requests.exceptions.Timeout:
            logger.warning(f"请求超时: {url}")
            if retries < self.max_retries:
                time.sleep(self.retry_delay)
                return self._make_request(url, params, retries + 1)
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            if retries < self.max_retries:
                time.sleep(self.retry_delay)
                return self._make_request(url, params, retries + 1)
            return None
    
    def search(
        self,
        keyword: str,
        location: Optional[str] = None,
        education: Optional[str] = None,
        page: int = 1
    ) -> Optional[str]:
        """
        执行职位搜索
        
        Args:
            keyword: 搜索关键词（专业方向/职位名称）
            location: 地区
            education: 学历要求
            page: 页码
            
        Returns:
            Optional[str]: 搜索结果页面HTML
        """
        # 构造搜索参数
        params = {
            "keyword": keyword,
            "page": page,
        }
        
        # 添加地区参数
        if location:
            location_code = self._parse_location(location)
            if location_code:
                params["workplace"] = location_code
        
        # 添加学历参数
        if education:
            edu_code = self._parse_education(education)
            if edu_code:
                params["degree"] = edu_code
        
        # 发送搜索请求
        html = self._make_request(JOB_LIST_URL, params)
        return html
    
    def _parse_location(self, location: str) -> Optional[str]:
        """
        解析地区名称，返回地区代码
        
        Args:
            location: 地区名称
            
        Returns:
            Optional[str]: 地区代码
        """
        # 直接匹配
        if location in LOCATION_MAPPING:
            return LOCATION_MAPPING[location]
        
        # 模糊匹配
        for loc_name, loc_code in LOCATION_MAPPING.items():
            if loc_name in location or location in loc_name:
                return loc_code
        
        # 返回原始值，让服务器处理
        return location
    
    def _parse_education(self, education: str) -> Optional[str]:
        """
        解析学历要求，返回学历代码
        
        Args:
            education: 学历名称
            
        Returns:
            Optional[str]: 学历代码
        """
        # 标准化学历名称
        edu_normalized = education.lower().replace("学位", "").strip()
        
        # 直接匹配
        if edu_normalized in EDUCATION_MAPPING:
            return EDUCATION_MAPPING[edu_normalized]
        
        # 模糊匹配
        for edu_name, edu_code in EDUCATION_MAPPING.items():
            if edu_name in edu_normalized or edu_normalized in edu_name:
                return edu_code
        
        return None
    
    def search_announcement(
        self,
        keyword: str,
        page: int = 1
    ) -> Optional[str]:
        """
        搜索招聘公告
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            Optional[str]: 搜索结果页面HTML
        """
        url = f"{JOB_LIST_URL}/announcement"
        params = {
            "keyword": keyword,
            "page": page,
        }
        
        return self._make_request(url, params)
