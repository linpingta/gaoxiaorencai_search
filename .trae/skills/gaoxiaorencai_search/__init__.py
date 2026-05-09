"""
高校人才网实时搜索 Skill - OpenClaw Skill Entry Point

Usage:
    from gaoxiaorencai_search import search
    result = search("北京，硕士，AI方向，近1个月")
"""

import sys
import os

# Add parent directory to path to import modules
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import from project modules
from core import search, SearchService, QueryParser, SearchCriteria
from parsers import JobParser, JobInfo

__version__ = "1.0.0"
__author__ = "OpenClaw"

# Export main functions
__all__ = [
    "search",
    "SearchService", 
    "QueryParser",
    "SearchCriteria",
    "JobParser",
    "JobInfo",
]


def run(query: str, **kwargs) -> str:
    """
    OpenClaw Skill standard run interface
    
    Args:
        query: Search query string (e.g., "北京，硕士，AI方向，近1个月")
        **kwargs: Additional parameters
            - format: Output format (text|markdown|json|simple), default is text
            
    Returns:
        str: Formatted search results
    """
    from core import ResultFormatter
    
    service = SearchService()
    
    output_format = kwargs.get("format", "text")
    
    if output_format == "simple":
        jobs = service.search_jobs(query)
        criteria = QueryParser().parse(query)
        criteria_desc = QueryParser().format_criteria(criteria)
        formatter = ResultFormatter()
        return formatter.format_simple(jobs, criteria_desc)
    
    elif output_format == "markdown":
        jobs = service.search_jobs(query)
        criteria = QueryParser().parse(query)
        criteria_desc = QueryParser().format_criteria(criteria)
        formatter = ResultFormatter()
        return formatter.format_markdown(jobs, criteria_desc)
    
    else:
        return service.search(query)


def help() -> str:
    """
    Get help information
    
    Returns:
        str: Help text
    """
    return """
【高校人才网实时搜索 Skill】

功能：实时搜索高校人才网(gaoxiaojob.com)最新招聘信息

使用方法：
  输入格式：地区，学历，专业方向，时效范围
  
示例：
  北京，硕士，AI方向，近1个月
  上海，博士，计算机，近7天
  广州，本科，教育类，近3个月
  深圳，硕士，近1个月

参数说明：
  地区：北京、上海、广州、深圳、杭州等
  学历：本科、硕士、博士、博士后
  专业方向：AI、计算机、自动化、教育等
  时效范围：近7天、近1个月、近3个月、近半年

注意事项：
  1. 地区、学历、专业方向至少提供一个
  2. 时效范围默认为近1个月
  3. 多个条件用逗号或空格分隔
  4. 搜索耗时约3-5秒，请耐心等待

其他命令：
  help / 帮助 - 显示此帮助信息
""".strip()


def metadata() -> dict:
    """
    Get skill metadata
    
    Returns:
        dict: Metadata dictionary
    """
    return {
        "name": "gaoxiaorencai_search",
        "description": "Search and retrieve job postings from gaoxiaojob.com (高校人才网)",
        "version": "1.0.0",
        "author": "OpenClaw",
        "parameters": {
            "query": {
                "type": "string",
                "description": "Search query string",
                "required": True,
            },
            "format": {
                "type": "string",
                "description": "Output format",
                "enum": ["text", "markdown", "json", "simple"],
                "default": "text",
            },
        },
    }
