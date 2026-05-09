---
name: "gaoxiaorencai_search"
description: "Search and retrieve job postings from gaoxiaojob.com (高校人才网). Invoke when user wants to find university/research institute job openings, faculty positions, postdoc opportunities, or when user asks about academic job search in China."
---

# 高校人才网实时搜索 Skill

## Overview

This skill provides real-time search capabilities for job postings on 高校人才网 (gaoxiaojob.com), a leading Chinese academic job platform for universities and research institutions.

## When to Use

- User asks about university faculty positions in China
- User wants to find postdoc opportunities
- User inquires about academic job openings
- User needs to search for research institute positions
- User mentions job search with criteria like location, degree requirements, or field

## Input Format

Users can search using natural language queries with the following components:

```
地区，学历，专业方向，时效范围
```

### Parameters

| Parameter | Description | Examples |
|-----------|-------------|----------|
| 地区 (Location) | City or province | 北京, 上海, 广州, 深圳, 杭州 |
| 学历 (Education) | Degree requirement | 本科, 硕士, 博士, 博士后 |
| 专业方向 (Major) | Field of study | AI, 计算机, 自动化, 教育, 医学 |
| 时效范围 (Time Range) | Publication time | 近7天, 近1个月, 近3个月 |

## Usage Examples

### Basic Search
```
北京，硕士，AI方向，近1个月
```

### Search by Location and Degree
```
上海，博士，近1个月
```

### Search by Field
```
广州，本科，教育类
```

### Flexible Input
```
深圳硕士计算机方向
```

## Output Format

The skill returns structured job information including:

- 职位名称 (Job Title)
- 招聘单位 (Employer)
- 单位类型 (Organization Type)
- 工作地点 (Location)
- 学历要求 (Education Requirement)
- 专业方向 (Field/Major)
- 发布时间 (Publication Date)
- 薪资待遇 (Salary)
- 福利待遇 (Benefits)
- 详情链接 (Detail Link)

## Implementation

This skill uses:
- Real-time web scraping of gaoxiaojob.com
- Multi-condition filtering (location, education, major, time)
- Automatic deduplication and sorting
- Structured data extraction and formatting

## Error Handling

If search fails, the skill will:
1. Retry up to 2 times automatically
2. Return user-friendly error messages
3. Suggest alternative search terms or timing

## Notes

- Default time range is "近1个月" (last 30 days) if not specified
- At least one search condition (location, education, or major) is required
- Results are sorted by publication date (newest first)
- Maximum 50 results returned per search
