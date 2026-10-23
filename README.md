# 中医知识图谱项目 · 学生同步文件

本仓库保存完整课程资料。代码、数据和小文件保留原有目录；6 个超过 100 MiB 的模型权重和安装包保存在 [Releases 下载区](https://github.com/1314Sunlight520/ChineseMedicine/releases/tag/student-files-v1)。

## 下载全部文件（推荐 Windows）

1. 点击 **Code → Download ZIP**，解压。
2. 在解压后的文件夹中打开 PowerShell，运行：

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\download-large-files.ps1
   ```

脚本会将模型和安装包下载到原来的目录，并校验 SHA-256。大文件约 3.75 GiB，请预留足够空间。也可以进入 Releases 手动下载附件，并根据 `FILES.sha256.json` 的 `path` 放回对应位置。

`FILES.sha256.json` 列出分享资料的文件清单、大小和 SHA-256。示例中硬编码的 API Key 已替换为占位符，Python 编译缓存已排除；本地原文件未改动。API Key 和数据库连接凭据需要自行配置。

仓库公开可读；没有写入权限的访问者不能修改本仓库。下载后可以修改自己的本地副本。
