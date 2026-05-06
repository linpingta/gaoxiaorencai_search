"""
查询解析器测试
"""
import unittest

from core import QueryParser, SearchCriteria


class TestQueryParser(unittest.TestCase):
    """测试查询解析器"""
    
    def setUp(self):
        self.parser = QueryParser()
    
    def test_parse_location(self):
        """测试地区解析"""
        # 测试完整查询
        criteria = self.parser.parse("北京，硕士，AI方向")
        self.assertEqual(criteria.location, "北京")
        
        criteria = self.parser.parse("上海博士计算机")
        self.assertEqual(criteria.location, "上海")
        
        # 测试模糊匹配
        criteria = self.parser.parse("京，硕士，AI")
        self.assertEqual(criteria.location, "北京")
    
    def test_parse_education(self):
        """测试学历解析"""
        criteria = self.parser.parse("北京，硕士，AI方向")
        self.assertEqual(criteria.education, "硕士")
        
        criteria = self.parser.parse("上海博士")
        self.assertEqual(criteria.education, "博士")
        
        criteria = self.parser.parse("广州本科")
        self.assertEqual(criteria.education, "本科")
    
    def test_parse_time_range(self):
        """测试时效范围解析"""
        criteria = self.parser.parse("北京，硕士，AI方向，近1个月")
        self.assertEqual(criteria.time_range, "近1个月")
        
        criteria = self.parser.parse("上海博士计算机近7天")
        self.assertEqual(criteria.time_range, "近7天")
        
        # 测试默认时效
        criteria = self.parser.parse("北京，硕士，AI")
        self.assertEqual(criteria.time_range, "近1个月")
    
    def test_parse_major(self):
        """测试专业方向解析"""
        criteria = self.parser.parse("北京，硕士，AI方向")
        self.assertEqual(criteria.major, "ai")
        
        criteria = self.parser.parse("上海博士计算机")
        self.assertEqual(criteria.major, "计算机")
        
        criteria = self.parser.parse("广州本科教育")
        self.assertEqual(criteria.major, "教育")
    
    def test_build_keyword(self):
        """测试关键词构建"""
        criteria = self.parser.parse("北京，硕士，AI方向")
        self.assertIn("ai", criteria.keyword.lower())
        
        criteria = self.parser.parse("上海博士计算机教师")
        self.assertIn("计算机", criteria.keyword)
        self.assertIn("教师", criteria.keyword)
    
    def test_validate(self):
        """测试条件验证"""
        # 有效条件
        criteria = SearchCriteria(
            location="北京",
            education="硕士",
            major="AI"
        )
        is_valid, _ = self.parser.validate(criteria)
        self.assertTrue(is_valid)
        
        # 只有地区也有效
        criteria = SearchCriteria(location="北京")
        is_valid, _ = self.parser.validate(criteria)
        self.assertTrue(is_valid)
        
        # 空条件无效
        criteria = SearchCriteria()
        is_valid, _ = self.parser.validate(criteria)
        self.assertFalse(is_valid)
    
    def test_format_criteria(self):
        """测试条件格式化"""
        criteria = SearchCriteria(
            location="北京",
            education="硕士",
            major="AI",
            time_range="近1个月"
        )
        formatted = self.parser.format_criteria(criteria)
        self.assertIn("北京", formatted)
        self.assertIn("硕士", formatted)


if __name__ == "__main__":
    unittest.main()
