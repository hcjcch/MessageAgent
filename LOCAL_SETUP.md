# Mem0 本地部署指南

## 🎯 本地部署的优势

- ✅ **无需 Mem0 云服务 API Key**
- ✅ **数据完全本地存储**，隐私更安全
- ✅ **无网络依赖**（除了 LLM 调用）
- ✅ **免费使用**，无额外费用
- ✅ **可自定义向量数据库和嵌入模型**

## 📋 两种部署方案

### 方案 1: 简化版（推荐新手）

使用 Qdrant 文件存储模式，无需额外服务。

#### 安装步骤

```bash
# 激活虚拟环境
source venv/bin/activate

# 已安装依赖（requirements.txt 已包含 qdrant-client）
# 无需额外安装
```

#### 配置环境变量

创建 `.env` 文件：

```bash
# 只需要 OpenAI API Key，用于对话生成
OPENAI_API_KEY=your_openai_api_key_here

# 不需要 MEM0_API_KEY！
```

#### 运行

```bash
python agent_local.py
```

**特点**：
- 数据存储在 `./qdrant_storage` 目录
- 重启后数据依然保留
- 无需额外服务

---

### 方案 2: 完整版（推荐生产环境）

使用 Docker 运行 Qdrant 服务，性能更好。

#### 1. 启动 Qdrant 服务

使用 Docker：

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

或使用 Docker Compose：

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    restart: unless-stopped
```

启动：

```bash
docker-compose up -d
```

#### 2. 验证 Qdrant 运行

访问 http://localhost:6333/dashboard

#### 3. 运行 Agent

```bash
python agent_local.py
```

**特点**：
- 更好的性能和并发支持
- Web 管理界面
- 适合生产环境

---

## 🚀 完全本地化（高级）

如果想要**完全不依赖外部 API**（包括 OpenAI），可以使用本地 LLM。

### 使用 Ollama（本地 LLM）

#### 1. 安装 Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 https://ollama.com/download 下载安装
```

#### 2. 下载模型

```bash
ollama pull llama2
# 或
ollama pull mistral
```

#### 3. 修改代码

创建 `agent_fully_local.py`，将 OpenAI 客户端替换为 Ollama：

```python
from openai import OpenAI

# 使用 Ollama 的 OpenAI 兼容 API
self.openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不需要真实 key
)
self.model = "llama2"
```

#### 4. 运行

```bash
python agent_fully_local.py
```

这样就**完全本地化**了！

---

## 🔧 使用其他向量数据库

### ChromaDB

```python
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "mem0_local",
            "path": "./chroma_storage",
        }
    }
}
```

安装：
```bash
pip install chromadb
```

### Faiss

```python
config = {
    "vector_store": {
        "provider": "faiss",
        "config": {
            "path": "./faiss_storage",
        }
    }
}
```

安装：
```bash
pip install faiss-cpu
```

---

## 📊 性能对比

| 方案 | 启动速度 | 查询性能 | 存储方式 | 适用场景 |
|------|----------|----------|----------|----------|
| 文件存储 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 本地文件 | 开发/测试 |
| Qdrant 服务 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 数据库 | 生产环境 |
| ChromaDB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 本地文件 | 中小规模 |
| Faiss | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 本地文件 | 大规模数据 |

---

## 🛠️ 常见问题

### Q: 本地版本和云服务版本有什么区别？

**云服务版本**（`agent.py`）:
- 需要 Mem0 API Key
- 数据存储在 Mem0 云端
- 自动管理基础设施
- 按使用量付费

**本地版本**（`agent_local.py`）:
- 不需要 Mem0 API Key
- 数据完全本地存储
- 需要自己管理存储
- 完全免费

### Q: 本地版本的记忆功能一样吗？

是的！功能完全相同，只是存储位置不同。

### Q: 数据存储在哪里？

- Qdrant 文件模式: `./qdrant_storage/`
- ChromaDB: `./chroma_storage/`
- Faiss: `./faiss_storage/`

### Q: 如何备份数据？

直接复制存储目录：

```bash
# 备份
cp -r qdrant_storage qdrant_storage_backup

# 恢复
cp -r qdrant_storage_backup qdrant_storage
```

### Q: 可以同时使用云服务和本地版本吗？

可以！它们是独立的，互不影响：
- `agent.py` - 云服务版本
- `agent_local.py` - 本地版本

### Q: 本地版本需要多少存储空间？

取决于对话量：
- 100 条对话记忆 ≈ 10-50 MB
- 1000 条对话记忆 ≈ 100-500 MB
- 10000 条对话记忆 ≈ 1-5 GB

---

## 📦 推荐配置

### 个人学习/开发
```bash
python agent_local.py  # 文件存储模式
```

### 小型应用
```bash
# 使用 ChromaDB
pip install chromadb
# 修改 config 使用 chroma
```

### 生产环境
```bash
# Docker 运行 Qdrant
docker-compose up -d
python agent_local.py
```

### 完全离线
```bash
# 安装 Ollama
ollama pull llama2
# 使用 agent_fully_local.py
```

---

## 🎓 下一步

1. 尝试运行简化版本
2. 查看数据存储目录
3. 根据需求选择合适的方案
4. 考虑是否需要完全本地化（使用 Ollama）

---

**总结**：本地部署让你完全掌控数据，无需依赖云服务，适合注重隐私和成本的场景！🔒

