# 高校人才网实时搜索 Skill 安装脚本
# 使用方法: 右键选择"使用 PowerShell 运行" 或在 PowerShell 中执行: .\install_skill.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  高校人才网实时搜索 Skill 安装程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 定义路径
$sourceDir = "$PSScriptRoot\.trae\skills\gaoxiaorencai_search"
$targetDir = "$env:USERPROFILE\.trae\skills\gaoxiaorencai_search"
$skillsJson = "$env:USERPROFILE\.trae\skills.json"

# 检查源目录是否存在
if (-not (Test-Path $sourceDir)) {
    Write-Error "源目录不存在: $sourceDir"
    exit 1
}

Write-Host "[1/4] 检查目标目录..." -ForegroundColor Yellow

# 创建目标目录
if (-not (Test-Path "$env:USERPROFILE\.trae\skills")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.trae\skills" -Force | Out-Null
    Write-Host "       已创建目录: $env:USERPROFILE\.trae\skills" -ForegroundColor Green
}

Write-Host "[2/4] 复制 Skill 文件..." -ForegroundColor Yellow

# 复制文件
if (Test-Path $targetDir) {
    Remove-Item -Path $targetDir -Recurse -Force
}
Copy-Item -Path $sourceDir -Destination $targetDir -Recurse -Force
Write-Host "       已复制到: $targetDir" -ForegroundColor Green

Write-Host "[3/4] 配置 skills.json..." -ForegroundColor Yellow

# 创建或更新 skills.json
$skillConfig = @{
    skills = @(
        @{
            name = "gaoxiaorencai_search"
            path = ".trae/skills/gaoxiaorencai_search"
            enabled = $true
            auto_load = $true
        }
    )
}

$jsonContent = $skillConfig | ConvertTo-Json -Depth 10
Set-Content -Path $skillsJson -Value $jsonContent -Encoding UTF8
Write-Host "       已更新: $skillsJson" -ForegroundColor Green

Write-Host "[4/4] 验证安装..." -ForegroundColor Yellow

# 验证安装
$skillFiles = @(
    "$targetDir\SKILL.md",
    "$targetDir\skill.json",
    "$targetDir\__init__.py"
)

$allExist = $true
foreach ($file in $skillFiles) {
    if (Test-Path $file) {
        Write-Host "       ✓ $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "       ✗ $(Split-Path $file -Leaf) 缺失" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host ""

if ($allExist) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Skill 安装成功!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "安装位置: $targetDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "使用方法:" -ForegroundColor Yellow
    Write-Host "  1. 重启 OpenClaw/Trae IDE" -ForegroundColor White
    Write-Host "  2. 在对话中输入类似以下查询:" -ForegroundColor White
    Write-Host "     - '帮我搜索北京硕士AI方向的招聘信息'" -ForegroundColor White
    Write-Host "     - '查找上海高校的博士后岗位'" -ForegroundColor White
    Write-Host "     - '最近有什么计算机方向的教师职位'" -ForegroundColor White
    Write-Host ""
    Write-Host "查询语法:" -ForegroundColor Yellow
    Write-Host "  地区，学历，专业方向，时效范围" -ForegroundColor White
    Write-Host "  例如: 北京，硕士，AI方向，近1个月" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  安装失败，请检查错误信息" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
