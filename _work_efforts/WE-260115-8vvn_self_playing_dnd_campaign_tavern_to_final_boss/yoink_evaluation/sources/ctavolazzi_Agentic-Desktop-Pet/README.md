<h1 align="center">🤖 Agentic-Desktop-Pet</h1>

<p align="center">
  <img src="./docs/peticon.png" height="200px" alt="Agentic-Desktop-Pet">
</p>

<p align="center">
  <a href="./README_EN.md">English</a> | 简体中文
</p>

---

## 👋 介绍

🚀 🚀 🚀 下一代 Agentic 桌宠 = LLM + 记忆 + 情感 + RPG + Claude Code
> [!Caution]
> development is still in progress, there are many bugs, please be patient 

## ✨ 特性

- 🧠 记忆系统：使用 [Cognee](https://docs.cognee.ai/) 
    - **知识图谱记忆**: 将对话组织成语义图谱
    - **长期记忆**: 跨会话持久存储
    - **语义搜索**: 向量和图谱搜索进行记忆检索
    - **记忆丰富化**: 自动提取实体和关系
- 🛠️ 个人助手能力：实现类似 Claude Code 的功能,参考   [learn-agent](https://github.com/jihe520/learn-agent) 
    - **文件操作**: 读取、创建、编辑本地文件
    - **代码执行**: 运行代码和脚本
    - **任务管理**: 创建和管理待办事项
    - **系统集成**: 执行系统命令和自动化任务
- mod 系统：轻松添加和切换不同桌宠主题
- 💕 动态情感系统
    - **情感状态**: 开心、悲伤、兴奋、无聊等基础情感
    - **时间衰减**: 情感随时间自然衰减
    - **互动增强**: 与用户交互增强情感连接
    - **行为影响**: 情感状态影响 Agent 的回复风格和行为
-  ⚔️ RPG 属性系统
    - **基础属性**: 智力、魅力、敏捷、体力等
    - **经验等级**: 通过对话和任务获得经验升级
    - **技能系统**: 解锁和升级各种能力
    - **好感度**: 与用户的情感纽带等级

<img src="/docs/example.png" width="300">

---

## 🏗️ 架构

```
Agentic-Desktop-Pet/
├── backend/                    # Python FastAPI 后端
│   ├── learn_agent/           # Agent 核心模块
│   │   ├── agent/             # Agent 实现
│   │   │   ├── agent.py       # 主 Agent 类
│   │   │   └── memory.py      # 记忆管理
│   │   ├── memory/            # 记忆系统 (Cognee)
│   │   │   └── cognee_manager.py
│   │   ├── emotion/           # 情感系统
│   │   │   └── emotion_engine.py
│   │   ├── rpg/               # RPG 属性系统
│   │   │   └── character.py
│   │   ├── llm/               # LLM 接口
│   │   └── tool/              # 工具集
│   │       ├── file_tool.py
│   │       ├── code_tool.py
│   │       └── todo_tool.py
│   ├── main.py                # FastAPI 服务入口
│   └── pyproject.toml
│
├── godot/                     # Godot 4.x 前端
│   ├── scenes/               # 场景文件
│   ├── scripts/              # GDScript 脚本
│   ├── themes/               # 桌宠主题
│   └── project.godot
│
├── docs/                     # 文档
└── CLAUDE.md                # Claude Code 指导
```

---

## 🚀 快速开始

### 前置要求

- **Python 3.13+**
- **Godot 4.3+**
- **LLM API** (OpenAI / DeepSeek / Claude 等)

### 安装后端

```bash
cd backend
uv sync
# 配置环境变量
cp .env.example .env
# 编辑 .env 添加 API Key
```

### 启动服务

```bash
# 启动后端服务
uv run main.py
# 服务运行在 http://localhost:8000
```

### 运行前端

1. 打开 Godot 4.3+
2. 导入 `godot/` 文件夹
3. 点击运行按钮（或按 F5）

> [!Caution]
> 将主题文件`.pck`都需要放在和`.exe`的同级目录的`themes/*.pck`下面

---

## 📖 使用指南

### ⌨️ 快捷键
鼠标右键 角色区域弹出对话框
当焦点在角色窗口上，按 ESC 关闭软件

### 文件操作
```
"帮我读取 main.py 文件"
"创建一个新文件 hello.txt"
"帮我编辑 config.json"
```

### 任务管理
```
"创建一个待办：买牛奶"
"列出我的待办事项"
"标记第一个待办为完成"
```

### 查看状态
```
"你现在感觉怎么样？"
"你有多少经验值？"
"显示你的属性"
```

---

## 🛣️ 开发路线图

详见 [TODO.md](./TODO.md)


## 🐶 开发自己的桌宠
[Wiki 教程](https://github.com/jihe520/Agentic-Desktop-Pet/wiki)


## 🤝 贡献

项目目前处于开发阶段（我有时间就会更新），还存在许多 Bug，我正着手修复。 欢迎任何贡献，即使细微。 添加角色素材等等

---

## ©️ 许可证

你可以使用项目中的任何代码片段，但不能直接将完整项目打包用于商业项目。 同时，需要注意项目中使用到的一些资产的版权信息。


## 🙏 致谢

- [Godot Engine](https://godotengine.org/) - 游戏引擎
- [godot-click-through-transparent-window](https://github.com/atadenizoktay/godot-click-through-transparent-window) - 透明窗口
- [Cognee](https://docs.cognee.ai/) - 知识图谱记忆系统
- [tech-dungeon-roguelite](https://trevor-pupkin.itch.io/tech-dungeon-roguelite) - 角色资产
- [tiny-swords](https://pixelfrog-assets.itch.io/tiny-swords) - 角色资产
- [dino-characters](https://arks.itch.io/dino-characters) - 角色资产
- [VPet](https://github.com/LorisYounger/VPet) - 角色资产
