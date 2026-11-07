# LangGraph 1.2.20 学习站 · 仓库入口

这是学习站的源码仓库。站点本体在 [`langgraph-learn/`](langgraph-learn/)，可以直接当静态网站部署。

**内容状态**：第 00–27 章 + 00A 图执行实验室 + 附录 A–E，共 34 个内容页，对应站点版本 v1.2.0。

- **本地看站**：双击 [`langgraph-learn/index.html`](langgraph-learn/index.html)，或在仓库根执行 `python -m http.server 8080` 后访问 <http://localhost:8080/langgraph-learn/>
- **配套示例**：[`samples/`](samples/) 是按章节编号的可运行 Python 工程，默认用 fake model，设置 `DEEPSEEK_API_KEY` 后走真实模型
- **部署**：见 [DEPLOY.md](DEPLOY.md)（GitHub Pages / Vercel / Netlify / 自建服务器）
- **更新记录**：见 [CHANGELOG.md](CHANGELOG.md)
- **自检**：`node tools/check-site.cjs` 与 `node tools/check-sources.cjs`

## 目录结构

```
langgraph-learn/           站点本体（发布时把这个目录作为站点根）
├── index.html             首页（学习进度、章节入口、更新记录）
├── 404.html               站内 404（自包含样式，任意深度可用）
├── robots.txt
├── chapters/              第 00–18 章 + 00A 图执行实验室
├── appendix/              附录 A–E（全部可读）
└── assets/                base.css / site.js / nav.js / search-index.js / flow-demo.* / favicon.svg

tools/                     零依赖 Node 脚本
├── check-site.cjs         静态检查（链接、锚点、nav 一致性、meta、发布物）
├── check-sources.cjs      校验每处 file:line 能否在 1.2.20 源码里定位，并检查路径大小写
└── build-search-index.cjs 从各页正文生成全文搜索索引

langgraph-1.2.20/          上游源码副本（仅本地核对出处用，不入库）
```

## 内容约定

- 全部内容对应 **LangGraph 1.2.20**，示例默认使用 **DeepSeek**。
- 页面上的每个默认值、抛错点、参数名都尽量带 `file:line` 出处标签。
- 站点零构建、不联网、不依赖 CDN，`file://` 直接打开即可阅读。
- 章节清单一律改 `langgraph-learn/assets/nav.js`；正文改动后重跑 `node tools/build-search-index.cjs`。
- 与 `agentscope-py-guide`、`springai-guide`、`langchain4j-guide` 保持同一套「先跑通、再拆解、再练习」结构。

## 拉取上游源码（本地核对出处）

推荐直接用 tag：

```powershell
git clone --depth 1 --branch 1.2.20 https://github.com/langchain-ai/langgraph.git langgraph-1.2.20
```

`langgraph-1.2.20/` 已在 `.gitignore` 中忽略，不要把整份源码提交进本站仓库。

## 来源与许可

教程基于 [langgraph](https://github.com/langchain-ai/langgraph) 1.2.20 的源码与官方文档整理，引用部分遵循上游 MIT 许可。
