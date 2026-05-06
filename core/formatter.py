"""
结果格式化模块 - 格式化搜索结果输出
"""
from typing import List

from parsers import JobInfo
from utils import logger


class ResultFormatter:
    """
    结果格式化器
    
    负责将搜索结果格式化为易读的文本格式
    """
    
    def __init__(self):
        self.max_results = 50
    
    def format(
        self,
        jobs: List[JobInfo],
        criteria_desc: str,
        total_found: int = 0
    ) -> str:
        """
        格式化搜索结果
        
        Args:
            jobs: 职位列表
            criteria_desc: 搜索条件描述
            total_found: 总共找到的结果数
            
        Returns:
            str: 格式化的结果文本
        """
        if not jobs:
            return self._format_empty_result(criteria_desc)
        
        lines = []
        
        # 标题
        lines.append(f"【高校人才网-实时搜索结果】（筛选条件：{criteria_desc}）")
        lines.append("")
        
        # 结果统计
        showing = min(len(jobs), self.max_results)
        if total_found > 0:
            lines.append(f"共找到 {total_found} 条招聘信息，显示前 {showing} 条：")
        else:
            lines.append(f"找到 {showing} 条招聘信息：")
        lines.append("")
        
        # 职位列表
        for idx, job in enumerate(jobs[:self.max_results], 1):
            lines.append(self._format_job(job, idx))
            lines.append("")
        
        # 提示信息
        if len(jobs) > self.max_results:
            lines.append(f"... 还有 {len(jobs) - self.max_results} 条结果未显示")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_job(self, job: JobInfo, index: int) -> str:
        """
        格式化单个职位信息
        
        Args:
            job: 职位信息
            index: 序号
            
        Returns:
            str: 格式化的职位文本
        """
        lines = []
        
        # 职位标题
        urgent_tag = "【急聘】" if job.is_urgent else ""
        bianzhi_tag = "【有编制】" if job.has_bianzhi else ""
        lines.append(f"{index}. {urgent_tag}{bianzhi_tag}{job.title}")
        
        # 单位信息
        lines.append(f"   招聘单位：{job.company}（单位类型：{job.company_type}）")
        
        # 基本信息
        if job.location and job.location != "未公开":
            lines.append(f"   工作地点：{job.location}")
        
        if job.education and job.education != "未公开":
            lines.append(f"   学历要求：{job.education}")
        
        if job.major and job.major != "未公开":
            lines.append(f"   专业方向：{job.major}")
        
        if job.recruit_num and job.recruit_num != "未公开":
            lines.append(f"   招聘人数：{job.recruit_num}")
        
        # 时间和薪资
        if job.publish_date:
            lines.append(f"   发布时间：{job.publish_date}")
        
        if job.salary:
            lines.append(f"   薪资待遇：{job.salary}")
        
        # 福利待遇
        if job.benefits and job.benefits != "未公开":
            # 限制福利待遇长度
            benefits = job.benefits[:100] + "..." if len(job.benefits) > 100 else job.benefits
            lines.append(f"   福利待遇：{benefits}")
        
        # 详情链接
        if job.url:
            lines.append(f"   详情链接：{job.url}")
        
        return "\n".join(lines)
    
    def _format_empty_result(self, criteria_desc: str) -> str:
        """
        格式化空结果
        
        Args:
            criteria_desc: 搜索条件描述
            
        Returns:
            str: 空结果提示文本
        """
        lines = [
            f"【高校人才网-实时搜索结果】（筛选条件：{criteria_desc}）",
            "",
            "未找到符合条件的招聘信息，建议：",
            "1. 调整筛选条件（如放宽地区、学历要求）",
            "2. 更换专业方向关键词",
            "3. 扩大时间范围",
            "4. 稍后重试",
        ]
        return "\n".join(lines)
    
    def format_error(self, error_msg: str) -> str:
        """
        格式化错误信息
        
        Args:
            error_msg: 错误信息
            
        Returns:
            str: 格式化的错误文本
        """
        lines = [
            "【高校人才网-实时搜索】",
            "",
            f"搜索失败：{error_msg}",
            "",
            "建议：",
            "1. 检查网络连接",
            "2. 稍后重试",
            "3. 如问题持续，请联系技术支持",
        ]
        return "\n".join(lines)
    
    def format_simple(
        self,
        jobs: List[JobInfo],
        criteria_desc: str
    ) -> str:
        """
        简化格式输出（用于快速预览）
        
        Args:
            jobs: 职位列表
            criteria_desc: 搜索条件描述
            
        Returns:
            str: 简化的结果文本
        """
        if not jobs:
            return f"未找到符合条件的招聘信息（{criteria_desc}）"
        
        lines = [f"【{criteria_desc}】找到 {len(jobs)} 条招聘信息：", ""]
        
        for idx, job in enumerate(jobs[:10], 1):
            urgent = "[急]" if job.is_urgent else ""
            bianzhi = "[编]" if job.has_bianzhi else ""
            lines.append(f"{idx}. {urgent}{bianzhi}{job.title} | {job.company} | {job.location} | {job.publish_date}")
        
        if len(jobs) > 10:
            lines.append(f"... 还有 {len(jobs) - 10} 条")
        
        return "\n".join(lines)
    
    def format_markdown(
        self,
        jobs: List[JobInfo],
        criteria_desc: str
    ) -> str:
        """
        Markdown格式输出
        
        Args:
            jobs: 职位列表
            criteria_desc: 搜索条件描述
            
        Returns:
            str: Markdown格式的结果文本
        """
        if not jobs:
            return f"## 高校人才网搜索结果\n\n**筛选条件：** {criteria_desc}\n\n未找到符合条件的招聘信息。"
        
        lines = [
            "## 高校人才网搜索结果",
            "",
            f"**筛选条件：** {criteria_desc}",
            f"**找到结果：** {len(jobs)} 条",
            "",
        ]
        
        for idx, job in enumerate(jobs[:self.max_results], 1):
            lines.append(f"### {idx}. {job.title}")
            lines.append("")
            lines.append(f"- **招聘单位：** {job.company}")
            lines.append(f"- **单位类型：** {job.company_type}")
            lines.append(f"- **工作地点：** {job.location}")
            lines.append(f"- **学历要求：** {job.education}")
            lines.append(f"- **专业方向：** {job.major}")
            lines.append(f"- **发布时间：** {job.publish_date}")
            lines.append(f"- **薪资待遇：** {job.salary}")
            if job.url:
                lines.append(f"- **详情链接：** [{job.url}]({job.url})")
            lines.append("")
        
        return "\n".join(lines)
    
    def format_json(self, jobs: List[JobInfo]) -> List[dict]:
        """
        JSON格式输出
        
        Args:
            jobs: 职位列表
            
        Returns:
            List[dict]: JSON格式的职位列表
        """
        result = []
        for job in jobs:
            result.append({
                "title": job.title,
                "company": job.company,
                "company_type": job.company_type,
                "location": job.location,
                "education": job.education,
                "major": job.major,
                "publish_date": job.publish_date,
                "salary": job.salary,
                "benefits": job.benefits,
                "url": job.url,
                "recruit_num": job.recruit_num,
                "is_urgent": job.is_urgent,
                "has_bianzhi": job.has_bianzhi,
            })
        return result
