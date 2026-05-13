# 高校人才网实时搜索 Skill 安装脚本
# 使用方法: 右键选择"使用 PowerShell 运行" 或在 PowerShell 中执行: .\install_skill.ps1

# 设置 UTF-8 编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

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
    Write-Host "       Created directory: $env:USERPROFILE\.trae\skills" -ForegroundColor Green
}

Write-Host "[2/4] 复制 Skill 文件..." -ForegroundColor Yellow

# 复制文件
if (Test-Path $targetDir) {
    Remove-Item -Path $targetDir -Recurse -Force
}
Copy-Item -Path $sourceDir -Destination $targetDir -Recurse -Force
Write-Host "       Copied to: $targetDir" -ForegroundColor Green

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
Write-Host "       Updated: $skillsJson" -ForegroundColor Green

Write-Host "[4/4] 验证安装..." -ForegroundColor Yellow

# 验证安装
$skillFiles = @(
    "$targetDir\SKILL.md",
    "$targetDir\skill.json",
    "$targetDir\__init__.py",
    "$targetDir\core.py",
    "$targetDir\parsers.py",
    "$targetDir\utils.py"
)

$allExist = $true
foreach ($file in $skillFiles) {
    if (Test-Path $file) {
        Write-Host "       OK: $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "       Missing: $(Split-Path $file -Leaf)" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host ""

if ($allExist) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Skill Installed Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Location: $targetDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  1. Restart OpenClaw/Trae IDE" -ForegroundColor White
    Write-Host "  2. Try queries like:" -ForegroundColor White
    Write-Host "     - 'Search for Beijing master AI jobs'" -ForegroundColor White
    Write-Host "     - 'Find Shanghai postdoc positions'" -ForegroundColor White
    Write-Host "     - 'Recent computer science teaching jobs'" -ForegroundColor White
    Write-Host ""
    Write-Host "Query format:" -ForegroundColor Yellow
    Write-Host "  Location, Education, Major, Time Range" -ForegroundColor White
    Write-Host "  Example: Beijing, Master, AI, Recent 1 month" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  Installation Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
