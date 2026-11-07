/* 00A LangGraph 图执行实验室：L1 最小 → L2 条件边/工具 → L3 可恢复（零依赖） */
(function () {
  "use strict";

  var root = document.getElementById("fd");
  if (!root) return;

  var NODES = {
    "input": {
        "name": "Input",
        "title": "invoke 输入",
        "input": "初始 state，例如 {\"messages\": [...]}",
        "output": "交给 START",
        "next": "START",
        "link": "01-setup.html",
        "linkText": "01 第一个图"
    },
    "start": {
        "name": "START",
        "title": "虚拟入口",
        "input": "初始 state",
        "output": "找到第一条边",
        "next": "Agent",
        "link": "01-setup.html",
        "linkText": "01 第一个图"
    },
    "agent": {
        "name": "Agent",
        "title": "节点：读 state，返回 partial",
        "input": "当前 state",
        "output": "{\"messages\": [...]} 等局部更新",
        "next": "Route",
        "link": "02-state-reducer.html",
        "linkText": "02 State 与 Reducer"
    },
    "route": {
        "name": "Route",
        "title": "条件边",
        "input": "节点返回后的 state",
        "output": "下一个节点名或 END",
        "next": "END",
        "link": "03-nodes-edges.html",
        "linkText": "03 条件路由"
    },
    "end": {
        "name": "END",
        "title": "虚拟出口",
        "input": "最终 state",
        "output": "执行器收尾",
        "next": "Result",
        "link": "01-setup.html",
        "linkText": "01 第一个图"
    },
    "result": {
        "name": "Result",
        "title": "返回最终 state",
        "input": "合并后的 state",
        "output": "调用方拿到 dict",
        "next": "—",
        "link": "01-setup.html",
        "linkText": "01 第一个图"
    },
    "checkpointer": {
        "name": "Checkpointer",
        "title": "写入 checkpoint",
        "input": "每个 superstep 后的 state",
        "output": "按 thread_id 存一份快照",
        "next": "Agent",
        "link": "05-checkpointer.html",
        "linkText": "05 Checkpointer",
        "addedAt": 2
    },
    "tool": {
        "name": "ToolNode",
        "title": "执行工具",
        "input": "AIMessage.tool_calls",
        "output": "ToolMessage 写回 messages",
        "next": "Agent",
        "link": "11-langchain-integration.html",
        "linkText": "11 LangChain 集成",
        "addedAt": 2
    },
    "toolroute": {
        "name": "ToolRoute",
        "title": "工具条件边",
        "input": "AIMessage.tool_calls",
        "output": "有调用去 ToolNode，没有去 END",
        "next": "ToolNode",
        "link": "11-langchain-integration.html",
        "linkText": "11 LangChain 集成",
        "addedAt": 2
    },
    "subgraph": {
        "name": "Subgraph",
        "title": "子图",
        "input": "父图映射进来的 state",
        "output": "子图最终 state",
        "next": "Agent",
        "link": "09-subgraph.html",
        "linkText": "09 子图",
        "addedAt": 2
    },
    "stream": {
        "name": "Stream",
        "title": "事件流",
        "input": "执行器的 step 输出",
        "output": "values / updates / messages 等事件",
        "next": "Result",
        "link": "08-streaming.html",
        "linkText": "08 流式",
        "addedAt": 2
    },
    "api": {
        "name": "API",
        "title": "HTTP / SSE 入口",
        "input": "请求体与 thread_id",
        "output": "调用 graph.invoke / stream",
        "next": "Auth",
        "link": "16-deployment.html",
        "linkText": "16 部署",
        "addedAt": 3
    },
    "auth": {
        "name": "Auth",
        "title": "鉴权与租户",
        "input": "请求头",
        "output": "可信的 user_id / tenant_id",
        "next": "Input",
        "link": "16-deployment.html",
        "linkText": "16 部署",
        "addedAt": 3
    },
    "store": {
        "name": "Store",
        "title": "长期记忆",
        "input": "namespace + key",
        "output": "跨 thread 的用户偏好",
        "next": "Agent",
        "link": "13-memory.html",
        "linkText": "13 记忆",
        "addedAt": 3
    },
    "retry": {
        "name": "Retry",
        "title": "节点重试",
        "input": "失败节点",
        "output": "退避后重试或抛出",
        "next": "Agent",
        "link": "10-retry-cache.html",
        "linkText": "10 重试与缓存",
        "addedAt": 3
    },
    "interrupt": {
        "name": "Interrupt",
        "title": "暂停等人",
        "input": "需要确认的动作",
        "output": "Command(resume=...) 后继续",
        "next": "Agent",
        "link": "07-hitl.html",
        "linkText": "07 HITL",
        "addedAt": 3
    },
    "postgres": {
        "name": "Postgres",
        "title": "持久化后端",
        "input": "checkpoint / store 写入",
        "output": "多副本共享状态",
        "next": "Checkpointer",
        "link": "16-deployment.html",
        "linkText": "16 部署",
        "addedAt": 3
    },
    "observe": {
        "name": "Observe",
        "title": "追踪与指标",
        "input": "图与节点事件",
        "output": "trace / token / 延迟",
        "next": "Result",
        "link": "15-testing-observability.html",
        "linkText": "15 测试与观测",
        "addedAt": 3
    },
    "deploy": {
        "name": "Deploy",
        "title": "发布",
        "input": "镜像与配置",
        "output": "可水平扩展的服务",
        "next": "—",
        "link": "16-deployment.html",
        "linkText": "16 部署",
        "addedAt": 3
    }
};

  var LEVELS = {
    "minimal": {
        "label": "MINIMAL GRAPH",
        "level": "L1",
        "blurb": "L1 只有 6 个观察点：输入进入 START，Agent 读 state 并返回 partial state，条件边决定去 END，最后返回合并后的 state。",
        "ids": [
            "input",
            "start",
            "agent",
            "route",
            "end",
            "result"
        ]
    },
    "control": {
        "label": "CONTROL FLOW",
        "level": "L2",
        "blurb": "L2 在 L1 上新增 5 个节点：Checkpointer、ToolNode、ToolRoute、Subgraph、Stream。重点是工具循环与 checkpoint 写入。",
        "ids": [
            "input",
            "checkpointer",
            "start",
            "agent",
            "route",
            "toolroute",
            "tool",
            "subgraph",
            "stream",
            "end",
            "result"
        ]
    },
    "durable": {
        "label": "DURABLE GRAPH",
        "level": "L3",
        "blurb": "L3 再加 8 个外围节点：API、Auth、Store、Retry、Interrupt、Postgres、Observe、Deploy。Interrupt 把执行停在 checkpoint，恢复不是从头跑。",
        "ids": [
            "api",
            "auth",
            "input",
            "store",
            "retry",
            "checkpointer",
            "start",
            "agent",
            "route",
            "toolroute",
            "tool",
            "interrupt",
            "subgraph",
            "stream",
            "postgres",
            "observe",
            "end",
            "result",
            "deploy"
        ]
    }
};

  var modeButtons = root.querySelectorAll(".fd-mode");
  var rail = document.getElementById("fd-rail");
  var blurb = document.getElementById("fd-blurb");
  var stepEl = document.getElementById("fd-step");
  var titleEl = document.getElementById("fd-title");
  var inputEl = document.getElementById("fd-input");
  var outputEl = document.getElementById("fd-output");
  var nextEl = document.getElementById("fd-next-node");
  var linkEl = document.getElementById("fd-link");
  var counterEl = document.getElementById("fd-counter");
  var labelEl = document.getElementById("fd-scenario-label");
  var levelEl = document.getElementById("fd-level");
  var jsonEl = document.getElementById("fd-json");
  var eventsEl = document.getElementById("fd-events");
  var packetEl = document.getElementById("fd-packet");
  var barEl = document.getElementById("fd-bar");
  var railWrap = root.querySelector(".fd-rail-wrap");
  var current = "minimal";
  var index = 0;
  var timer = null;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function nodes() {
    return LEVELS[current].ids.map(function (id) {
      return NODES[id];
    });
  }

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function stopPlay() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    playBtn.setAttribute("aria-pressed", "false");
    playBtn.textContent = "▶ 播放";
  }

  function paintRail() {
    rail.innerHTML = "";
    nodes().forEach(function (n, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "fd-node";
      b.dataset.i = String(i);
      var badge = n.addedAt
        ? '<span class="fd-badge l' + n.addedAt + '">+L' + n.addedAt + "</span>"
        : "";
      b.innerHTML =
        '<span class="fd-idx">' +
        pad2(i + 1) +
        "</span>" +
        badge +
        '<span class="fd-name">' +
        n.name +
        '</span><span class="fd-out">' +
        n.output +
        "</span>";
      b.addEventListener("click", function () {
        stopPlay();
        select(i);
      });
      rail.appendChild(b);
    });
  }

  function positionPacket() {
    var active = rail.querySelector(".fd-node.active");
    if (!active || !railWrap) {
      packetEl.classList.remove("on");
      return;
    }
    var wr = railWrap.getBoundingClientRect();
    var ar = active.getBoundingClientRect();
    packetEl.style.left = ar.left - wr.left + ar.width / 2 - 4 + "px";
    packetEl.classList.add("on");
  }

  function paintEvents() {
    if (!eventsEl) return;
    eventsEl.innerHTML = "";
    var from = Math.max(0, index - 6);
    nodes()
      .slice(from, index + 1)
      .forEach(function (n) {
        var chip = document.createElement("span");
        chip.className = "fd-event";
        chip.textContent = n.name;
        eventsEl.appendChild(chip);
      });
  }

  function select(i) {
    index = Math.max(0, Math.min(nodes().length - 1, i));
    var list = rail.querySelectorAll(".fd-node");
    for (var k = 0; k < list.length; k++) {
      list[k].classList.toggle("active", k === index);
      list[k].classList.toggle("done", k < index);
      if (k === index) list[k].setAttribute("aria-current", "step");
      else list[k].removeAttribute("aria-current");
    }
    var n = nodes()[index];
    var len = nodes().length;
    stepEl.textContent = "步骤 " + (index + 1) + " / " + len;
    counterEl.textContent = pad2(index + 1) + " / " + pad2(len);
    barEl.style.width = ((index + 1) / len) * 100 + "%";
    titleEl.textContent = n.title;
    inputEl.textContent = n.input;
    outputEl.textContent = n.output;
    nextEl.textContent = n.next;
    jsonEl.textContent = JSON.stringify(
      {
        step: index + 1,
        node: n.name,
        addedAt: n.addedAt || 1,
        input: n.input,
        output: n.output,
        next: n.next,
      },
      null,
      2
    );
    paintEvents();
    linkEl.innerHTML = '对应章节：<a href="' + n.link + '">' + n.linkText + "</a>";
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === len - 1;
    var active = list[index];
    if (active) {
      var left = active.offsetLeft - (rail.clientWidth - active.offsetWidth) / 2;
      if (rail.scrollWidth > rail.clientWidth + 4) {
        rail.scrollTo({
          left: Math.max(0, left),
          behavior: reduce ? "auto" : "smooth",
        });
      }
    }
    requestAnimationFrame(positionPacket);
  }

  function renderScenario(key) {
    stopPlay();
    current = key;
    index = 0;
    modeButtons.forEach(function (b) {
      b.setAttribute(
        "aria-pressed",
        b.dataset.scenario === key ? "true" : "false"
      );
    });
    blurb.textContent = LEVELS[key].blurb;
    labelEl.textContent = LEVELS[key].label;
    levelEl.textContent = LEVELS[key].level;
    eventsEl.innerHTML = "";
    jsonEl.textContent = "";
    paintRail();
    select(0);
  }

  var prevBtn = document.getElementById("fd-prev");
  var nextBtn = document.getElementById("fd-next");
  var playBtn = document.getElementById("fd-play");
  var resetBtn = document.getElementById("fd-reset");

  prevBtn.addEventListener("click", function () {
    stopPlay();
    select(index - 1);
  });
  nextBtn.addEventListener("click", function () {
    stopPlay();
    select(index + 1);
  });
  resetBtn.addEventListener("click", function () {
    stopPlay();
    select(0);
  });
  playBtn.addEventListener("click", function () {
    if (timer) {
      stopPlay();
      return;
    }
    if (index >= nodes().length - 1) select(0);
    playBtn.setAttribute("aria-pressed", "true");
    playBtn.textContent = "❚❚ 暂停";
    timer = setInterval(function () {
      if (index >= nodes().length - 1) {
        stopPlay();
        return;
      }
      select(index + 1);
    }, 1400);
  });

  modeButtons.forEach(function (b) {
    b.addEventListener("click", function () {
      renderScenario(b.dataset.scenario);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (!root.contains(document.activeElement)) return;
    if (e.key === "ArrowRight") {
      e.preventDefault();
      stopPlay();
      select(index + 1);
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      stopPlay();
      select(index - 1);
    }
  });

  rail.addEventListener("scroll", positionPacket, { passive: true });
  window.addEventListener("resize", positionPacket);

  var requested = new URLSearchParams(location.search).get("scenario");
  renderScenario(LEVELS[requested] ? requested : "minimal");
})();
