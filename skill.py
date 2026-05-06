"""
OpenClaw Skill 封装模块

提供OpenClaw Skill接口，支持通过OpenClaw调用高校人才网搜索功能
"""
from typing import Dict, Any, Optional

from core import SearchService, QueryParser
from utils import logger, clean_old_logs


class GaoxiaorencaiSkill:
    """
    高校人才网搜索Skill
    
    适配OpenClaw Skill规范，提供标准化的搜索接口
    """
    
    # Skill元数据
    name = "gaoxiaorencai_search"
    description = "高校人才网招聘信息实时搜索"
    version = "1.0.0"
    author = "OpenClaw"
    
    def __init__(self):
        self.search_service = SearchService()
        self.query_parser = QueryParser()
    
    def run(self, query: str, **kwargs) -> str:
        """
        Skill主入口
        
        Args:
            query: 用户搜索查询
            **kwargs: 额外参数
                - format: 输出格式 (text|markdown|json|simple)，默认text
                - max_results: 最大返回结果数
                
        Returns:
            str: 搜索结果
        """
        # 清理过期日志
        clean_old_logs()
        
        if not query or not query.strip():
            return self._get_help_message()
        
        query = query.strip()
        logger.info(f"Skill收到查询: {query}")
        
        # 检查是否为帮助请求
        if query in ["help", "帮助", "?", "？"]:
            return self._get_help_message()
        
        # 执行搜索
        try:
            output_format = kwargs.get("format", "text")
            
            if output_format == "simple":
                # 简化格式
                jobs = self.search_service.search_jobs(query)
                criteria = self.query_parser.parse(query)
                criteria_desc = self.query_parser.format_criteria(criteria)
                from core import ResultFormatter
                formatter = ResultFormatter()
                return formatter.format_simple(jobs, criteria_desc)
            
            elif output_format == "markdown":
                # Markdown格式
                jobs = self.search_service.search_jobs(query)
                criteria = self.query_parser.parse(query)
                criteria_desc = self.query_parser.format_criteria(criteria)
                from core import ResultFormatter
                formatter = ResultFormatter()
                return formatter.format_markdown(jobs, criteria_desc)
            
            else:
                # 默认文本格式
                return self.search_service.search(query)
                
        except Exception as e:
            logger.exception("Skill执行异常")
            return f"搜索失败：{str(e)}\n\n请稍后重试或联系技术支持。"
    
    def _get_help_message(self) -> str:
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
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        获取Skill元数据
        
        Returns:
            Dict[str, Any]: 元数据字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "parameters": {
                "query": {
                    "type": "string",
                    "description": "搜索查询字符串",
                    "required": True,
                },
                "format": {
                    "type": "string",
                    "description": "输出格式",
                    "enum": ["text", "markdown", "json", "simple"],
                    "default": "text",
                },
            },
        }


# Skill实例
_skill_instance: Optional[GaoxiaorencaiSkill] = None


def get_skill() -> GaoxiaorencaiSkill:
    """
    获取Skill单例
    
    Returns:
        GaoxiaorencaiSkill: Skill实例
    """
    global _skill_instance
    if _skill_instance is None:
        _skill_instance = GaoxiaorencaiSkill()
    return _skill_instance


# OpenClaw Skill标准接口
def run(query: str, **kwargs) -> str:
    """
    OpenClaw Skill标准运行接口
    
    Args:
        query: 用户查询
        **kwargs: 额外参数
        
    Returns:
        str: 搜索结果
    """
    skill = get_skill()
    return skill.run(query, **kwargs)


def help() -> str:
    """
    获取帮助信息
    
    Returns:
        str: 帮助文本
    """
    skill = get_skill()
    return skill._get_help_message()


def metadata() -> Dict[str, Any]:
    """
    获取Skill元数据
    
    Returns:
        Dict[str, Any]: 元数据字典
    """
    skill = get_skill()
    return skill.get_metadata()
