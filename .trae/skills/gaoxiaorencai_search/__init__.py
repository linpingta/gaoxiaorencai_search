"""
高校人才网实时搜索 Skill - OpenClaw Skill

一个自包含的 OpenClaw Skill，用于实时搜索高校人才网(gaoxiaojob.com)的招聘信息。
无需外部依赖，可直接在 OpenClaw 中运行。

Usage:
    import gaoxiaorencai_search
    result = gaoxiaorencai_search.run("北京，硕士，AI方向，近1个月")
    print(result)
"""

__version__ = "1.0.0"
__author__ = "OpenClaw"

# 导入所有模块（确保 Skill 自包含）
from . import utils
from . import parsers
from . import core

# 导出主要接口
from .core import search, SearchService, QueryParser, SearchCriteria, ResultFormatter
from .parsers import JobParser, JobInfo

__all__ = [
    "search",
    "run",
    "help",
    "metadata",
    "SearchService",
    "QueryParser",
    "SearchCriteria",
    "ResultFormatter",
    "JobParser",
    "JobInfo",
]


def run(query: str, **kwargs) -> str:
    """
    OpenClaw Skill 标准运行接口
    
    Args:
        query: 搜索查询字符串，格式：地区，学历，专业方向，时效范围
               例如："北京，硕士，AI方向，近1个月"
        **kwargs: 额外参数
            - format: 输出格式 (text|simple)，默认 text
            
    Returns:
        str: 格式化的搜索结果
    """
    if not query or not query.strip():
        return help()
    
    query = query.strip()
    
    # 检查帮助请求
    if query.lower() in ["help", "帮助", "?", "？"]:
        return help()
    
    try:
        service = SearchService()
        output_format = kwargs.get("format", "text")
        
        if output_format == "simple":
            # 简化格式
            criteria = QueryParser().parse(query)
            criteria_desc = QueryParser().format_criteria(criteria)
            
            # 这里需要获取 jobs 列表
            html = service.engine.search(
                keyword=criteria.keyword,
                location=criteria.location,
                education=criteria.education
            )
            
            if html is None:
                return "搜索失败：无法访问高校人才网"
            
            jobs = service.job_parser.parse_job_list(html)
            if criteria.major:
                jobs = service.job_parser.filter_by_major(jobs, criteria.major)
            jobs = service.job_parser.filter_by_time_range(jobs, criteria.time_range)
            jobs = service.job_parser.deduplicate_jobs(jobs)
            jobs = service.job_parser.sort_jobs(jobs)
            
            # 简化输出
            if not jobs:
                return f"未找到符合条件的招聘信息（{criteria_desc}）"
            
            lines = [f"【{criteria_desc}】找到 {len(jobs)} 条招聘信息：", ""]
            for idx, job in enumerate(jobs[:10], 1):
                urgent = "[急]" if job.is_urgent else ""
                bianzhi = "[编]" if job.has_bianzhi else ""
                lines.append(f"{idx}. {urgent}{bianzhi}{job.title} | {job.company} | {job.location}")
            
            if len(jobs) > 10:
                lines.append(f"... 还有 {len(jobs) - 10} 条")
            
            return "\n".join(lines)
        
        else:
            # 完整格式
            return service.search(query)
            
    except Exception as e:
        return f"搜索失败：{str(e)}\n\n请检查网络连接或稍后重试。"


def help() -> str:
    """
    获取帮助信息
    
    Returns:
        str: 帮助文本
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
    获取 Skill 元数据
    
    Returns:
        dict: 元数据字典
    """
    return {
        "name": "gaoxiaorencai_search",
        "description": "Search and retrieve job postings from gaoxiaojob.com (高校人才网). Invoke when user wants to find university/research institute job openings, faculty positions, postdoc opportunities, or when user asks about academic job search in China.",
        "version": "1.0.0",
        "author": "OpenClaw",
        "parameters": {
            "query": {
                "type": "string",
                "description": "Search query string (e.g., '北京，硕士，AI方向，近1个月')",
                "required": True,
            },
            "format": {
                "type": "string",
                "description": "Output format",
                "enum": ["text", "simple"],
                "default": "text",
            },
        },
    }
