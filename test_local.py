"""
测试脚本 - 验证本地版本是否正常工作
"""

import sys
import os

def test_imports():
    """测试依赖包是否正确安装"""
    print("=" * 60)
    print("测试 1: 检查依赖包")
    print("=" * 60)
    
    required_packages = {
        "mem0": "Mem0 核心库",
        "openai": "OpenAI 客户端",
        "dotenv": "环境变量管理",
        "qdrant_client": "Qdrant 向量数据库"
    }
    
    all_ok = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {description} ({package})")
        except ImportError as e:
            print(f"✗ {description} ({package}) - 未安装")
            all_ok = False
    
    return all_ok


def test_memory_initialization():
    """测试本地记忆初始化"""
    print("\n" + "=" * 60)
    print("测试 2: 本地记忆初始化")
    print("=" * 60)
    
    try:
        from mem0 import Memory
        
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "test_collection",
                    "path": "./test_qdrant_storage",
                }
            }
        }
        
        memory = Memory.from_config(config)
        print("✓ Mem0 本地存储初始化成功")
        print(f"✓ 存储路径: ./test_qdrant_storage")
        
        # 清理测试数据
        import shutil
        if os.path.exists("./test_qdrant_storage"):
            shutil.rmtree("./test_qdrant_storage")
            print("✓ 测试数据已清理")
        
        return True
        
    except Exception as e:
        print(f"✗ Mem0 初始化失败: {e}")
        return False


def test_env_file():
    """检查环境变量文件"""
    print("\n" + "=" * 60)
    print("测试 3: 环境变量配置")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    mem0_key = os.getenv("MEM0_API_KEY")
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✓ OPENAI_API_KEY 已配置")
    else:
        print("⚠️  OPENAI_API_KEY 未配置或使用示例值")
        print("   提示: 本地版本需要 OpenAI API Key")
    
    if mem0_key and mem0_key != "your_mem0_api_key_here":
        print("✓ MEM0_API_KEY 已配置（云服务版使用）")
    else:
        print("ℹ️  MEM0_API_KEY 未配置（本地版不需要）")
    
    return True


def test_qdrant_connection():
    """测试 Qdrant 连接"""
    print("\n" + "=" * 60)
    print("测试 4: Qdrant 服务连接（可选）")
    print("=" * 60)
    
    try:
        from qdrant_client import QdrantClient
        
        # 尝试连接本地 Qdrant 服务
        try:
            client = QdrantClient(host="localhost", port=6333, timeout=2)
            collections = client.get_collections()
            print("✓ Qdrant 服务运行中")
            print(f"✓ 已有 {len(collections.collections)} 个集合")
            return True
        except Exception as e:
            print("ℹ️  Qdrant 服务未运行（使用文件存储模式）")
            print("   提示: 如需更好性能，可运行:")
            print("   docker-compose up -d")
            return True
            
    except Exception as e:
        print(f"✗ Qdrant 客户端测试失败: {e}")
        return False


def test_ollama():
    """测试 Ollama 服务（完全本地版）"""
    print("\n" + "=" * 60)
    print("测试 5: Ollama 本地 LLM（完全本地版）")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        
        try:
            models = client.models.list()
            print("✓ Ollama 服务运行中")
            print(f"✓ 可用模型: {[m.id for m in models.data]}")
            return True
        except Exception as e:
            print("ℹ️  Ollama 服务未运行（完全本地版需要）")
            print("   提示: 安装 Ollama:")
            print("   macOS: brew install ollama")
            print("   Linux: curl -fsSL https://ollama.com/install.sh | sh")
            print("   然后运行: ollama pull llama2")
            return True
            
    except Exception as e:
        print(f"⚠️  Ollama 测试跳过: {e}")
        return True


def main():
    """运行所有测试"""
    print("\n🔍 Mem0 本地部署环境检查\n")
    
    results = []
    
    # 运行测试
    results.append(("依赖包检查", test_imports()))
    results.append(("记忆初始化", test_memory_initialization()))
    results.append(("环境变量", test_env_file()))
    results.append(("Qdrant 服务", test_qdrant_connection()))
    results.append(("Ollama 服务", test_ollama()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {name}")
    
    # 推荐
    print("\n" + "=" * 60)
    print("💡 使用推荐")
    print("=" * 60)
    
    openai_configured = os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here"
    mem0_configured = os.getenv("MEM0_API_KEY") and os.getenv("MEM0_API_KEY") != "your_mem0_api_key_here"
    
    if mem0_configured and openai_configured:
        print("✅ 可以使用: python agent.py (云服务版)")
    
    if openai_configured:
        print("✅ 可以使用: python agent_local.py (本地版)")
    
    # 检查 Ollama
    try:
        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        client.models.list()
        print("✅ 可以使用: python agent_fully_local.py (完全本地版)")
    except:
        if not openai_configured:
            print("\n⚠️  建议:")
            print("1. 配置 OPENAI_API_KEY 使用本地版")
            print("2. 或安装 Ollama 使用完全本地版（无需 API Key）")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 返回状态
    all_critical_passed = results[0][1] and results[1][1]
    return 0 if all_critical_passed else 1


if __name__ == "__main__":
    sys.exit(main())

