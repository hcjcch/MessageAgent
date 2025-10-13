# 通义千问 + ChromaDB 版本使用说明

## ✅ 已完成的配置

你的 `agent_local.py` 已经完全配置好并测试通过：

1. ✅ **LLM**: 通义千问（Qwen）
2. ✅ **向量存储**: ChromaDB（本地文件）
3. ✅ **API Key**: 使用系统环境变量 `DEFAULT_LLM_API_KEY`
4. ✅ **Embeddings**: 通义千问 text-embedding-v1
5. ✅ **记忆功能**: 完全正常

## 🚀 立即开始使用

```bash
# 进入项目目录
cd /Users/huangchen/Develop/mem0

# 激活虚拟环境
source venv/bin/activate

# 启动 Agent
python agent_local.py
```

就这么简单！因为你已经把 `DEFAULT_LLM_API_KEY` 设置到系统环境变量了。

## 📋 配置总结

### 环境变量

| 变量 | 状态 | 用途 |
|------|------|------|
| `DEFAULT_LLM_API_KEY` | ✅ 已设置 | 通义千问 API Key |
| `QWEN_MODEL` | 可选 | 模型选择（默认 qwen-plus） |

### 架构说明

```
用户输入
   ↓
通义千问 LLM (对话生成)
   ↓
Mem0 (记忆管理)
   ├─ 通义千问 LLM (提取记忆)
   ├─ 通义千问 Embeddings (向量化)
   └─ ChromaDB (本地存储)
   ↓
助手回复
```

### 数据流程

1. **用户发送消息** → Agent 接收
2. **搜索相关记忆** → ChromaDB 查询 (使用通义千问 embeddings)
3. **构建上下文** → 结合记忆和对话历史
4. **生成回复** → 调用通义千问 LLM
5. **保存记忆** → Mem0 提取关键信息 (使用通义千问) → ChromaDB 存储

## 💬 使用示例

### 基本对话

```
>>> python agent_local.py

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

>>> 你好，我叫小明，是一名AI工程师

👤 用户: 你好，我叫小明，是一名AI工程师
✓ 已保存 2 条记忆到本地
🤖 助手: 你好小明！很高兴认识你...

>>> /memories

============================================================
📚 当前用户的所有本地记忆:
============================================================

1. 用户名叫小明
2. 小明是一名AI工程师
...
```

### 可用命令

- **直接输入** - 与 Agent 对话
- `/memories` - 查看所有记忆
- `/clear` - 清空当前会话
- `/exit` - 退出程序

## 🔧 技术细节

### 关键配置代码

```python
# agent_local.py 中的配置

# 1. 设置环境变量让所有组件使用通义千问
os.environ["OPENAI_API_KEY"] = llm_api_key
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 2. 配置 Mem0
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "mem0_local",
            "path": "./chroma_storage",
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "qwen-plus",  # 用于提取记忆
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-v1",  # 通义千问的 embedding
        }
    }
}
```

### 文件结构

```
chroma_storage/          # ChromaDB 数据目录
├── chroma.sqlite3      # 主数据库
└── ...                # 索引文件
```

## 📊 成本估算

使用通义千问的成本（按 1000 次对话）：

- **LLM 调用**: ¥30-50 (qwen-plus)
- **Embeddings**: 很便宜，几乎可忽略
- **存储**: 完全免费（本地存储）
- **总计**: 约 ¥30-50/千次对话

## ⚙️ 高级配置

### 切换模型

```bash
# 临时切换
export QWEN_MODEL=qwen-turbo  # 更快更便宜
# 或
export QWEN_MODEL=qwen-max    # 更强大

# 永久切换
echo 'export QWEN_MODEL=qwen-max' >> ~/.zshrc
source ~/.zshrc
```

### 数据备份

```bash
# 备份记忆数据
cp -r chroma_storage chroma_backup_$(date +%Y%m%d)

# 恢复
cp -r chroma_backup_20241013 chroma_storage
```

### 清理数据

```bash
# 清理所有记忆
rm -rf chroma_storage

# 下次运行会自动重新创建
```

## 🎯 对比其他版本

| 特性 | 云服务版 | 本地版 (你在用) | 完全本地版 |
|------|---------|----------------|-----------|
| LLM | OpenAI | 通义千问 | Ollama |
| 存储 | Mem0 云 | ChromaDB | ChromaDB |
| API Key | 2个 | 1个 | 0个 |
| 费用 | 最高 | 中等 | 免费 |
| 隐私 | 一般 | 好 | 最好 |

## 📚 相关文件

- `agent_local.py` - 主程序
- `test_qwen_setup.py` - 测试脚本
- `QUICK_START_QWEN.md` - 快速入门
- `env_example_qwen.txt` - 环境变量示例

## ❓ 常见问题

### Q: 如何确认使用的是通义千问？

```bash
# 运行测试脚本
python test_qwen_setup.py

# 看到 "✓ 通义千问响应成功" 就对了
```

### Q: 数据存在哪里？

本地 `./chroma_storage` 目录，完全私有。

### Q: 如何升级模型？

```bash
export QWEN_MODEL=qwen-max
python agent_local.py
```

### Q: 可以离线使用吗？

不能完全离线，因为需要调用通义千问 API。如需完全离线，使用 `agent_fully_local.py` + Ollama。

## 🎉 开始使用

现在一切就绪！运行：

```bash
python agent_local.py
```

享受智能对话吧！🚀

---

**配置完成时间**: 2024-10-13  
**版本**: 通义千问 + ChromaDB  
**状态**: ✅ 测试通过

