# 部署说明

站点是纯静态、零构建的，发布物是 `langgraph-learn/` 目录。

## 本地预览

```powershell
python -m http.server 8080
```

然后访问 <http://localhost:8080/langgraph-learn/>。

也可以直接双击 `langgraph-learn/index.html`；站内链接与搜索在 `file://` 下可用。

## GitHub Pages

仓库已包含 `.github/workflows/deploy-pages.yml`：

1. 在仓库 Settings → Pages → Source 选择 **GitHub Actions**。
2. 在 Actions 里手动运行 **Deploy site**（当前工作流只在手动触发）。
3. 工作流会重建搜索索引、跑 `check-site`，然后发布 `langgraph-learn/`。

## Vercel / Netlify

- Build command：留空
- Publish directory：`langgraph-learn`
- Node 版本：20（仅用于构建搜索索引；如果平台不跑构建，直接发布目录也可以）

## 自建服务器

把 `langgraph-learn/` 作为站点根目录即可。Nginx 示例：

```nginx
server {
  listen 80;
  root /var/www/langgraph-learn;
  index index.html;

  location / {
    try_files $uri $uri/ /404.html;
  }
}
```

如果部署在子路径（例如 `/langgraph/`），把 `langgraph-learn/` 放到该子目录即可；站内链接是相对路径，不需要改配置。
