# LangGraph 1.2.20 配套示例

这些示例与正文一一对应，版本固定在 **LangGraph 1.2.20**。
默认**不需要 API Key**：没有 `DEEPSEEK_API_KEY` 时自动使用 fake model；
设置后才会走真实 DeepSeek。

## 安装

```bash
cd samples
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

## 离线跑一遍

```bash
pytest
```

不访问网络，覆盖：最小图、reducer、路由、Send map-reduce、checkpoint、时间旅行、HITL、工具循环、Store。

## 逐章运行

```bash
python -m lg_samples.s01_hello_graph
python -m lg_samples.s02_state_reducer
python -m lg_samples.s03_router
python -m lg_samples.s04_map_reduce
python -m lg_samples.s05_checkpoint
python -m lg_samples.s06_time_travel
python -m lg_samples.s07_hitl
python -m lg_samples.s11_tool_agent
python -m lg_samples.s13_memory_store
```

## 真实模型

```bash
cp .env.example .env
# 填入 DEEPSEEK_API_KEY
python -m lg_samples.s00_live_smoke
```

`common.get_model()` 会优先使用 `ChatDeepSeek`；没 key 时回退到 fake model。
示例默认不用真实模型，避免一跑测试就烧 token。

## 小服务

```bash
uvicorn lg_samples.s24_kb_service:app --reload
curl -N -X POST localhost:8000/chat \
  -H "content-type: application/json" \
  -d "{\"question\":\"退款政策是什么？\",\"user_id\":\"alice\",\"thread_id\":\"t-1\"}"
```

## 与正文的对应

| 目录 | 章节 |
|---|---|
| `s01_hello_graph` | 01 环境与第一个图 |
| `s02_state_reducer` | 02 State 与 Reducer |
| `s03_router` | 03 条件路由 |
| `s04_map_reduce` | 04 Command/Send 与 map-reduce |
| `s05_checkpoint` | 05 Checkpointer 与 thread_id |
| `s06_time_travel` | 06 时间旅行 |
| `s07_hitl` | 07 interrupt 与 HITL |
| `s11_tool_agent` | 11 LangChain 集成 / ToolNode |
| `s13_memory_store` | 13 记忆与 Store |
| `s24_kb_service` | 24 多轮知识库客服 |

## 说明

- `s11_tool_agent` 用脚本化 fake model 返回 `tool_calls`，所以离线也能验证完整工具循环。
- 真实模型的冒烟测试不在 `pytest` 默认路径里；需要时用 `.env` 手动跑对应脚本。
