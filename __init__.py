"""
高校人才网实时搜索模块

提供高校人才网(gaoxiaojob.com)招聘信息的实时搜索功能
"""

__version__ = "1.0.0"
__author__ = "OpenClaw"

from core import search, SearchService, QueryParser, SearchCriteria
from parsers import JobParser, JobInfo

__all__ = [
    "search",
    "SearchService",
    "QueryParser",
    "SearchCriteria",
    "JobParser",
    "JobInfo",
]
