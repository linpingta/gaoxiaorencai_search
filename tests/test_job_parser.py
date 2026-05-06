"""
职位解析器测试
"""
import unittest
from datetime import datetime

from parsers import JobParser, JobInfo


class TestJobParser(unittest.TestCase):
    """测试职位解析器"""
    
    def setUp(self):
        self.parser = JobParser()
    
    def test_normalize_date(self):
        """测试日期标准化"""
        # 测试 MM-DD 格式
        result = self.parser._normalize_date("04-29")
        self.assertEqual(result, f"{datetime.now().year}-04-29")
        
        # 测试 YYYY-MM-DD 格式
        result = self.parser._normalize_date("2026-04-29")
        self.assertEqual(result, "2026-04-29")
        
        # 测试特殊格式
        result = self.parser._normalize_date("今天")
        self.assertEqual(result, datetime.now().strftime("%Y-%m-%d"))
        
        result = self.parser._normalize_date("昨天")
        yesterday = datetime.now()
        yesterday = yesterday.replace(day=yesterday.day - 1)
        self.assertEqual(result, yesterday.strftime("%Y-%m-%d"))
    
    def test_filter_by_time_range(self):
        """测试时间范围筛选"""
        jobs = [
            JobInfo(
                title="教师",
                company="A大学",
                company_type="公立",
                location="北京",
                education="硕士",
                major="计算机",
                publish_date=datetime.now().strftime("%Y-%m-%d"),
                salary="面议",
                benefits="",
                url=""
            ),
            JobInfo(
                title="研究员",
                company="B研究所",
                company_type="科研",
                location="上海",
                education="博士",
                major="AI",
                publish_date="2025-01-01",  # 很久以前
                salary="面议",
                benefits="",
                url=""
            ),
        ]
        
        # 筛选近1个月
        filtered = self.parser.filter_by_time_range(jobs, "近1个月")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "教师")
    
    def test_filter_by_major(self):
        """测试专业方向筛选"""
        jobs = [
            JobInfo(
                title="AI工程师",
                company="A大学",
                company_type="公立",
                location="北京",
                education="硕士",
                major="人工智能",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
            JobInfo(
                title="语文教师",
                company="B中学",
                company_type="公立",
                location="北京",
                education="本科",
                major="中文",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
        ]
        
        # 筛选AI相关
        filtered = self.parser.filter_by_major(jobs, "AI")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "AI工程师")
    
    def test_deduplicate_jobs(self):
        """测试职位去重"""
        jobs = [
            JobInfo(
                title="教师",
                company="A大学",
                company_type="公立",
                location="北京",
                education="硕士",
                major="计算机",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
            JobInfo(
                title="教师",  # 重复
                company="A大学",
                company_type="公立",
                location="北京",
                education="硕士",
                major="计算机",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
            JobInfo(
                title="研究员",
                company="B研究所",
                company_type="科研",
                location="上海",
                education="博士",
                major="AI",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
        ]
        
        deduplicated = self.parser.deduplicate_jobs(jobs)
        self.assertEqual(len(deduplicated), 2)
    
    def test_sort_jobs(self):
        """测试职位排序"""
        jobs = [
            JobInfo(
                title="旧职位",
                company="A大学",
                company_type="公立",
                location="北京",
                education="硕士",
                major="计算机",
                publish_date="2026-04-01",
                salary="面议",
                benefits="",
                url=""
            ),
            JobInfo(
                title="新职位",
                company="B大学",
                company_type="公立",
                location="上海",
                education="博士",
                major="AI",
                publish_date="2026-04-29",
                salary="面议",
                benefits="",
                url=""
            ),
        ]
        
        sorted_jobs = self.parser.sort_jobs(jobs)
        self.assertEqual(sorted_jobs[0].title, "新职位")
        self.assertEqual(sorted_jobs[1].title, "旧职位")


if __name__ == "__main__":
    unittest.main()
