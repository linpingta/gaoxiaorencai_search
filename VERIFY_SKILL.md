# Skill 配置验证指南

## 当前状态

**项目目录下的Skill**: ✅ 已配置
- 位置: `c:\Users\tchu\PycharmProjects\gaoxiaorencai_search\.trae\skills\gaoxiaorencai_search\`

**用户全局Skill**: ❌ 未配置
- 需要安装到: `%USERPROFILE%\.trae\skills\gaoxiaorencai_search\`

## 安装方法

### 方法一：使用安装脚本（推荐）

1. 打开 PowerShell
2. 进入项目目录:
   ```powershell
   cd c:\Users\tchu\PycharmProjects\gaoxiaorencai_search
   ```
3. 运行安装脚本:
   ```powershell
   .\install_skill.ps1
   ```
4. 按提示完成安装

### 方法二：手动安装

1. **创建目标目录**:
   ```powershell
   mkdir %USERPROFILE%\.trae\skills\gaoxiaorencai_search
   ```

2. **复制文件**:
   将以下文件从项目目录复制到用户目录:
   ```
   从: c:\Users\tchu\PycharmProjects\gaoxiaorencai_search\.trae\skills\gaoxiaorencai_search\
   到: %USERPROFILE%\.trae\skills\gaoxiaorencai_search\
   
   文件列表:
   - SKILL.md
   - skill.json
   - __init__.py
   ```

3. **创建 skills.json**:
   在 `%USERPROFILE%\.trae\` 目录下创建 `skills.json`:
   ```json
   {
     "skills": [
       {
         "name": "gaoxiaorencai_search",
         "path": ".trae/skills/gaoxiaorencai_search",
         "enabled": true,
         "auto_load": true
       }
     ]
   }
   ```

## 验证安装

### 1. 检查文件是否存在

运行以下 PowerShell 命令:
```powershell
# 检查 Skill 目录
Test-Path $env:USERPROFILE\.trae\skills\gaoxiaorencai_search

# 检查关键文件
Test-Path $env:USERPROFILE\.trae\skills\gaoxiaorencai_search\SKILL.md
Test-Path $env:USERPROFILE\.trae\skills\gaoxiaorencai_search\skill.json
Test-Path $env:USERPROFILE\.trae\skills\gaoxiaorencai_search\__init__.py

# 检查配置文件
Test-Path $env:USERPROFILE\.trae\skills.json
```

如果都返回 `True`，说明安装成功。

### 2. 查看 Skill 内容

```powershell
# 查看 SKILL.md
Get-Content $env:USERPROFILE\.trae\skills\gaoxiaorencai_search\SKILL.md -Head 20

# 查看 skills.json
Get-Content $env:USERPROFILE\.trae\skills.json
```

### 3. 在 OpenClaw 中验证

1. **重启 OpenClaw/Trae IDE**
   - 完全关闭并重新打开 Trae IDE

2. **测试 Skill 触发**
   在对话中输入以下任意内容:
   ```
   帮我搜索北京硕士AI方向的招聘信息
   ```
   ```
   查找上海高校的博士后岗位
   ```
   ```
   最近有什么计算机方向的教师职位
   ```

3. **预期结果**
   - OpenClaw 应该自动识别并调用 `gaoxiaorencai_search` Skill
   - 返回格式化的搜索结果

## 故障排除

### Skill 未触发

1. **检查文件路径**:
   ```powershell
   Get-ChildItem $env:USERPROFILE\.trae\skills\gaoxiaorencai_search\
   ```

2. **检查 skills.json 格式**:
   ```powershell
   Get-Content $env:USERPROFILE\.trae\skills.json | ConvertFrom-Json
   ```

3. **验证 SKILL.md 格式**:
   - 确保文件开头有 frontmatter:
     ```yaml
     ---
     name: "gaoxiaorencai_search"
     description: "..."
     ---
     ```

### 导入错误

如果 Skill 触发但报错，检查:
1. Python 依赖是否安装:
   ```bash
   pip install -r requirements.txt
   ```
2. 项目路径是否正确添加到 sys.path

### 网络错误

- 检查是否能访问 https://www.gaoxiaojob.com
- 检查防火墙/代理设置

## 目录结构参考

安装成功后，目录结构应该是:
```
%USERPROFILE%/
└── .trae/
    ├── skills.json                    # Skill 注册配置
    └── skills/
        └── gaoxiaorencai_search/      # Skill 目录
            ├── SKILL.md               # Skill 元数据
            ├── skill.json             # Skill 配置
            └── __init__.py            # Skill 入口
```

## 卸载 Skill

如果需要卸载，删除以下文件/目录:
```powershell
# 删除 Skill 目录
Remove-Item -Path $env:USERPROFILE\.trae\skills\gaoxiaorencai_search -Recurse -Force

# 编辑 skills.json 移除配置
notepad $env:USERPROFILE\.trae\skills.json
```

## 更新 Skill

1. 更新项目代码
2. 重新运行安装脚本:
   ```powershell
   .\install_skill.ps1
   ```
3. 重启 OpenClaw/Trae IDE
