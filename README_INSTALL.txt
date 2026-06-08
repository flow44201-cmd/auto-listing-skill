auto-listing-skill 离线安装说明

推荐安装方式：

1. 关闭 Codex App。
2. 解压 auto-listing-skill-offline.zip。
3. 打开 PowerShell，运行：

   explorer "$env:USERPROFILE\.agents\skills"

4. 如果没有 skills 文件夹，就新建。
5. 把解压出来的 auto-listing-skill 文件夹放进去。
6. 最终结构必须是：

   %USERPROFILE%\.agents\skills\auto-listing-skill\SKILL.md
   %USERPROFILE%\.agents\skills\auto-listing-skill\references\...
   %USERPROFILE%\.agents\skills\auto-listing-skill\agents\openai.yaml

7. 重启 Codex App。
8. 新开对话，输入：

   执行自动上架skill

重要：

- 所有 .md/.yaml 文件都是 UTF-8。
- 如果用 PowerShell 查看文件，必须使用：

  Get-Content -Encoding UTF8

- 如果看到乱码，不要执行任务，先重新安装或用 UTF-8 读取。
- 不要用乱码内容推断目录、产品编号、价格表或上架规则。
