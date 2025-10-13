# 基于 Mem0 的多轮对话 Agent

这是一个使用 [Mem0](https://mem0.ai) 构建的智能对话 Agent，支持长期记忆和上下文理解。Agent 能够记住用户的偏好、历史对话内容，并在后续对话中提供更个性化的服务。

## 功能特点

- ✨ **长期记忆**: 使用 Mem0 存储和检索对话历史
- 🧠 **智能上下文**: 自动从历史记忆中提取相关信息
- 👤 **多用户支持**: 为不同用户维护独立的记忆空间
- 💬 **自然对话**: 基于 OpenAI GPT 模型的自然语言理解
- 📚 **记忆管理**: 查看和管理存储的记忆
- 🔒 **本地部署**: 支持完全本地部署，无需云服务 API Key

## 版本说明

本项目提供**三个版本**，根据你的需求选择：

| 版本 | 文件 | API Key 需求 | 特点 |
|------|------|-------------|------|
| **云服务版** | `agent.py` | Mem0 + OpenAI | 推荐快速开始 |
| **本地版** | `agent_local.py` | 仅 OpenAI | 数据本地存储 |
| **完全本地版** | `agent_fully_local.py` | 无需任何 Key | 完全私有化 |

详细的本地部署指南请查看 [LOCAL_SETUP.md](LOCAL_SETUP.md)

## 项目结构

```
mem0/
├── venv/                      # Python 虚拟环境
├── agent.py                   # 云服务版（需要 Mem0 API Key）
├── agent_local.py             # 本地版（仅需 OpenAI API Key）
├── agent_fully_local.py       # 完全本地版（使用 Ollama）
├── example.py                 # 使用示例
├── requirements.txt           # Python 依赖包
├── requirements_local.txt     # 本地版依赖
├── docker-compose.yml         # Docker 配置（可选）
├── LOCAL_SETUP.md            # 本地部署详细指南
├── quickstart.md             # 快速入门
├── .env                      # 环境变量配置（需要创建）
└── README.md                 # 项目说明
```

## 快速开始

### 方式一：云服务版（推荐快速体验）

1. **激活虚拟环境**
```bash
source venv/bin/activate
```

2. **创建 `.env` 文件**
```bash
MEM0_API_KEY=your_mem0_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

3. **运行**
```bash
python agent.py
```

### 方式二：本地版（推荐日常使用）

1. **激活虚拟环境**
```bash
source venv/bin/activate
```

2. **创建 `.env` 文件**（只需 OpenAI Key）
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

3. **运行**
```bash
python agent_local.py
```

数据将存储在本地 `./qdrant_storage` 目录。

### 方式三：完全本地版（推荐隐私优先）

1. **安装 Ollama**
```bash
# macOS
brew install ollama

# 或访问 https://ollama.com/download
```

2. **下载模型**
```bash
ollama pull llama2
```

3. **运行**
```bash
python agent_fully_local.py
```

**无需任何 API Key！完全本地运行！**

详细说明请查看：
- [LOCAL_SETUP.md](LOCAL_SETUP.md) - 本地部署详细指南
- [COMPARISON.md](COMPARISON.md) - 三个版本详细对比

## 环境测试

运行测试脚本检查环境配置：

```bash
python test_local.py
```

这将检查：
- 依赖包是否安装
- 本地存储是否正常
- 环境变量是否配置
- 可选服务状态（Qdrant、Ollama）

## 使用方法

### 运行 Agent

```bash
python agent.py
```

### 可用命令

在对话界面中，你可以使用以下命令：

- **直接输入消息**: 与 Agent 进行对话
- `/memories`: 查看当前用户的所有记忆
- `/clear`: 清空当前会话历史（不清除 Mem0 中的记忆）
- `/quit` 或 `/exit`: 退出程序

### 使用示例

```
欢迎使用基于 Mem0 的多轮对话 Agent
============================================================
请输入用户ID (直接回车使用 'default_user'): alice
✓ Agent 已初始化 (用户ID: alice)

可用命令:
  - 直接输入消息进行对话
  - /memories - 查看所有记忆
  - /clear - 清空当前会话历史
  - /quit 或 /exit - 退出程序

>>> 你好！我叫 Alice，我喜欢喝咖啡和阅读科幻小说。

👤 用户: 你好！我叫 Alice，我喜欢喝咖啡和阅读科幻小说。
✓ 已保存 2 条记忆
🤖 助手: 很高兴认识你，Alice！咖啡和科幻小说都是很棒的爱好...

>>> 你能推荐一些适合我的书吗？

👤 用户: 你能推荐一些适合我的书吗？
✓ 已保存 2 条记忆
🤖 助手: 当然可以！既然你喜欢科幻小说，我可以推荐一些经典作品...

>>> /memories

============================================================
📚 当前用户的所有记忆:
============================================================

1. 用户名叫 Alice
2. Alice 喜欢喝咖啡
3. Alice 喜欢阅读科幻小说
...
```

## 核心功能说明

### ConversationalAgent 类

主要的 Agent 类，提供以下功能：

#### 初始化
```python
agent = ConversationalAgent(user_id="alice")
```

#### 对话
```python
response = agent.chat("你好，今天天气怎么样？")
```

#### 记忆管理
```python
# 添加记忆
agent.add_to_memory([
    {"role": "user", "content": "我喜欢喝咖啡"},
    {"role": "assistant", "content": "好的，我记住了"}
])

# 搜索记忆
memories = agent.search_memory("咖啡", limit=5)

# 获取所有记忆
all_memories = agent.get_all_memories()
```

## 工作原理

1. **用户输入**: 用户发送消息
2. **记忆检索**: Agent 从 Mem0 中搜索相关的历史信息
3. **上下文构建**: 将相关记忆和对话历史组合成上下文
4. **生成回复**: 使用 OpenAI API 基于上下文生成回复
5. **保存记忆**: 将当前对话保存到 Mem0 中

## 扩展开发

### 集成到你的应用

```python
from agent import ConversationalAgent

# 创建 Agent 实例
agent = ConversationalAgent(user_id="your_user_id")

# 进行对话
response = agent.chat("你好")
print(response)

# 查看用户记忆
memories = agent.get_all_memories()
for memory in memories:
    print(memory.get("memory"))
```

### 自定义系统提示

修改 `agent.py` 中的 `system_prompt` 变量来定制 Agent 的行为：

```python
system_prompt = """你是一个专业的客户服务助手。
你可以记住客户的历史订单和偏好，提供个性化的服务。"""
```

## 注意事项

1. **API 密钥安全**: 不要将 `.env` 文件提交到版本控制系统
2. **成本控制**: OpenAI API 和 Mem0 API 可能会产生费用，请注意使用量
3. **记忆管理**: Mem0 会自动提取对话中的关键信息作为记忆
4. **隐私保护**: 请遵守相关隐私法规，妥善处理用户数据

## 相关资源

- [Mem0 官方文档](https://docs.mem0.ai/)
- [Mem0 快速入门](https://docs.mem0.ai/quickstart)
- [OpenAI API 文档](https://platform.openai.com/docs)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

Made with ❤️ using Mem0

