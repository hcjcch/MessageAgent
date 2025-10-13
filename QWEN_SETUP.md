# 通义千问 + ChromaDB 配置指南

本指南将帮助你配置使用**通义千问（Qwen）** 作为 LLM 和 **ChromaDB** 作为本地向量存储的 Agent。

## 🎯 优势

- ✅ **国内 LLM**：通义千问是阿里云的大语言模型，国内访问更快更稳定
- ✅ **价格优势**：相比 OpenAI 更实惠
- ✅ **中文优化**：对中文理解更好
- ✅ **本地存储**：ChromaDB 轻量级，易于部署
- ✅ **完全本地**：数据不上传到云端

## 📋 第一步：获取通义千问 API Key

### 1. 访问 DashScope 控制台

打开浏览器访问：https://dashscope.aliyun.com/

### 2. 注册/登录阿里云账号

如果没有账号，需要先注册阿里云账号。

### 3. 开通 DashScope 服务

- 进入控制台后，找到「模型广场」
- 选择「通义千问」系列模型
- 开通服务（有免费额度）

### 4. 获取 API Key

- 在控制台右上角，点击「API-KEY 管理」
- 创建新的 API Key
- **复制并保存** API Key（只显示一次）

### 5. 充值（可选）

免费额度用完后，可以充值继续使用。通义千问的价格比 OpenAI 便宜很多。

## 📋 第二步：安装 ChromaDB

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装 ChromaDB
pip install chromadb
```

或者使用项目提供的依赖文件：

```bash
pip install -r requirements_local.txt
```

## 📋 第三步：配置环境变量

### 方法 1：使用模板文件

```bash
# 复制模板
cp .env.qwen .env

# 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

### 方法 2：手动创建

创建 `.env` 文件并添加以下内容：

```bash
# 通义千问 API Key（必需）
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# 模型选择（可选，默认 qwen-plus）
QWEN_MODEL=qwen-plus
```

### 可用的通义千问模型

| 模型 | 特点 | 价格 | 推荐场景 |
|------|------|------|---------|
| `qwen-turbo` | 速度快 | 💰 最便宜 | 日常对话、简单任务 |
| `qwen-plus` | 平衡 | 💰💰 适中 | **推荐默认** |
| `qwen-max` | 能力强 | 💰💰💰 较贵 | 复杂任务、高质量输出 |
| `qwen-long` | 长文本 | 💰💰 适中 | 长文档处理 |

## 📋 第四步：运行 Agent

```bash
python agent_local.py
```

### 首次运行会看到：

```
============================================================
欢迎使用基于 Mem0 的多轮对话 Agent（本地版本）
✓ 使用通义千问 LLM
✓ 使用 ChromaDB 本地存储
✓ 无需 Mem0 云服务 API Key
============================================================

请输入用户ID (直接回车使用 'default_user'): 

✓ 使用 ChromaDB 向量数据库（本地文件存储）
✓ 数据存储路径: ./chroma_storage
✓ 使用通义千问模型: qwen-plus
✓ 本地 Agent 已初始化 (用户ID: default_user)
✓ 使用通义千问 + ChromaDB 本地存储
```

## 🎮 使用示例

```
>>> 你好！我叫小明，是一名软件工程师，喜欢用 Python 开发。

👤 用户: 你好！我叫小明，是一名软件工程师，喜欢用 Python 开发。
✓ 已保存 2 条记忆到本地
🤖 助手: 你好小明！很高兴认识你。作为一名 Python 开发工程师，你一定经常使用各种 Python 库和框架...

>>> 你还记得我的名字和职业吗？

👤 用户: 你还记得我的名字和职业吗？
🤖 助手: 当然记得！你叫小明，是一名软件工程师，而且喜欢用 Python 进行开发...

>>> /memories

============================================================
📚 当前用户的所有本地记忆:
============================================================

1. 用户名叫小明
2. 小明是一名软件工程师
3. 小明喜欢用 Python 开发
...
```

## 📂 数据存储位置

所有对话记忆存储在本地：

```
./chroma_storage/
├── chroma.sqlite3        # ChromaDB 数据库文件
└── ...其他索引文件
```

### 备份数据

```bash
# 备份
cp -r chroma_storage chroma_storage_backup_$(date +%Y%m%d)

# 恢复
cp -r chroma_storage_backup_20241013 chroma_storage
```

## 💰 成本对比

### 通义千问 vs OpenAI（按 1000 次对话估算）

| 项目 | 通义千问 (qwen-plus) | OpenAI (gpt-4) |
|------|---------------------|----------------|
| LLM 费用 | ¥30-50 | ¥150-300 |
| 存储费用 | ¥0（本地） | ¥0（本地） |
| **总计** | **¥30-50** | **¥150-300** |

使用通义千问可以**节省 70-80% 的成本**！

## ⚡ 性能优化

### 1. 选择合适的模型

```bash
# 日常对话 - 速度优先
QWEN_MODEL=qwen-turbo

# 平衡使用 - 推荐
QWEN_MODEL=qwen-plus

# 高质量输出 - 质量优先
QWEN_MODEL=qwen-max
```

### 2. ChromaDB 优化

ChromaDB 会自动优化，无需特别配置。如果数据量很大（>10万条记忆），建议定期清理：

```python
# 在 Python 中
agent.memory.delete_all(user_id="user_id")
```

## 🔧 常见问题

### Q: 通义千问 API Key 在哪里获取？

A: 访问 https://dashscope.aliyun.com/ -> 登录 -> API-KEY 管理

### Q: ChromaDB 需要额外服务吗？

A: 不需要！ChromaDB 是嵌入式数据库，直接使用本地文件存储。

### Q: 数据存储在哪里？

A: `./chroma_storage` 目录，可以随时备份或删除。

### Q: 通义千问支持哪些语言？

A: 中文和英文都支持，中文效果更好。

### Q: 如何切换模型？

A: 修改 `.env` 文件中的 `QWEN_MODEL` 参数。

### Q: 通义千问有免费额度吗？

A: 有！新用户有免费额度，具体查看 DashScope 控制台。

### Q: 响应速度怎么样？

A: 通义千问在国内访问速度很快，通常 1-3 秒响应。

### Q: 可以离线使用吗？

A: 不完全离线。记忆存储是本地的，但需要联网调用通义千问 API。如需完全离线，使用 `agent_fully_local.py`（配合 Ollama）。

## 🎓 下一步

1. **优化提示词**：修改 `system_prompt` 定制 Agent 行为
2. **集成到应用**：将 Agent 集成到你的应用中
3. **添加功能**：扩展工具调用、文件处理等功能
4. **监控成本**：在 DashScope 控制台查看 API 调用量

## 📚 相关资源

- [通义千问官方文档](https://help.aliyun.com/zh/dashscope/)
- [DashScope 控制台](https://dashscope.aliyun.com/)
- [ChromaDB 文档](https://docs.trychroma.com/)
- [API 价格](https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-thousand-questions-metering-and-billing)

---

**祝你使用愉快！🎉**

如有问题，欢迎提 Issue 或查看项目文档。

