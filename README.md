# Daily Intel

Daily Intel 已切换到 Gwern.net 风格的 Hakyll 构建系统，并在 WSL 下运行。

## 快速开始

```bash
cd /mnt/c/Users/ROG/.openclaw/workspace/projects/daily-intel/build
GWERN_ANNOTATIONS=0 \
GWERN_EXTERNAL_ANNOTATIONS=0 \
GWERN_WRITE_MISSING_ANNOTATIONS=0 \
GWERN_LINK_ANNOTATIONS=0 \
GWERN_LINK_SIZES=0 \
cabal run hakyll -- watch
```

访问:
- WSL 内部: `http://127.0.0.1:8000/`
- Windows 端: `http://<WSL_IP>:8000/`
  ```bash
  hostname -I | awk '{print $1}'
  ```

## 主页与模板

- 首页内容使用 `gwen-net-index模版.md` 作为原版索引模板，并覆盖到 `index.md`。
- 模板文件使用 `static/template/default.html` (已移除 SSI 依赖，改为由 Hakyll 注入 `static/include/*.html` 片段)。
- 如果访问 `/` 出现目录列表，执行:
  ```bash
  GWERN_ANNOTATIONS=0 GWERN_EXTERNAL_ANNOTATIONS=0 GWERN_WRITE_MISSING_ANNOTATIONS=0 GWERN_LINK_ANNOTATIONS=0 GWERN_LINK_SIZES=0 \
  cabal run hakyll -- build index.md
  ```

## 内容同步

已将 `/home/mako/wiki` 的内容同步到 `daily-intel`（排除 `.git/`, `build/`, `_cache/`, `_site/`, `dist-newstyle/`），用于快速迁移文章与页面。

## 代理与本地访问

如果本地访问被代理拦截:
```bash
curl --noproxy '*' -I http://127.0.0.1:8000/
```
或在 WSL 中设置:
```bash
export NO_PROXY=localhost,127.0.0.1,::1
```
