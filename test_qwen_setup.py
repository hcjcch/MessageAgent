"""
测试通义千问 + ChromaDB 配置
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_environment():
    """测试环境变量配置"""
    print("=" * 60)
    print("检查环境变量配置")
    print("=" * 60)
    
    # 检查 DEFAULT_LLM_API_KEY
    api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✓ DEFAULT_LLM_API_KEY: {masked_key}")
    else:
        print("✗ DEFAULT_LLM_API_KEY: 未设置")
        print("\n请设置环境变量:")
        print("  export DEFAULT_LLM_API_KEY=your_qwen_api_key")
        print("  或在 .env 文件中添加: DEFAULT_LLM_API_KEY=your_api_key")
        return False
    
    # 检查模型配置
    model = os.getenv("QWEN_MODEL", "qwen-plus")
    print(f"✓ QWEN_MODEL: {model}")
    
    return True


def test_chromadb():
    """测试 ChromaDB 是否可用"""
    print("\n" + "=" * 60)
    print("检查 ChromaDB")
    print("=" * 60)
    
    try:
        import chromadb
        print("✓ ChromaDB 已安装")
        
        # 测试创建客户端
        from chromadb import Client, Settings
        client = Client(Settings(
            is_persistent=False,
            anonymized_telemetry=False
        ))
        print("✓ ChromaDB 客户端初始化成功")
        
        return True
    except ImportError:
        print("✗ ChromaDB 未安装")
        print("  安装: pip install chromadb")
        return False
    except Exception as e:
        print(f"✗ ChromaDB 初始化失败: {e}")
        return False


def test_qwen_connection():
    """测试通义千问连接"""
    print("\n" + "=" * 60)
    print("测试通义千问连接")
    print("=" * 60)
    
    api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if not api_key:
        print("✗ 缺少 DEFAULT_LLM_API_KEY，跳过测试")
        return False
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        model = os.getenv("QWEN_MODEL", "qwen-plus")
        
        print(f"⏳ 测试模型: {model}")
        print("   发送测试消息...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "你好，请回复'测试成功'"}
            ],
            max_tokens=50
        )
        
        reply = response.choices[0].message.content
        print(f"✓ 通义千问响应成功")
        print(f"✓ 回复内容: {reply}")
        
        return True
        
    except Exception as e:
        print(f"✗ 通义千问连接失败: {e}")
        print("\n请检查:")
        print("1. API Key 是否正确")
        print("2. 是否已开通通义千问服务")
        print("3. 账户是否有余额")
        return False


def test_mem0_with_chroma():
    """测试 Mem0 + ChromaDB 集成"""
    print("\n" + "=" * 60)
    print("测试 Mem0 + ChromaDB 集成")
    print("=" * 60)
    
    try:
        from mem0 import Memory
        
        api_key = os.getenv("DEFAULT_LLM_API_KEY")
        
        # 为 Mem0 的 embedder 设置环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "test_collection",
                    "path": "./test_chroma_storage",
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": os.getenv("QWEN_MODEL", "qwen-plus"),
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-v1",
                }
            }
        }
        
        memory = Memory.from_config(config)
        print("✓ Mem0 + ChromaDB 初始化成功")
        
        # 测试添加记忆
        memory.add(
            "测试记忆：我喜欢编程",
            user_id="test_user"
        )
        print("✓ 添加记忆成功")
        
        # 测试搜索记忆
        results = memory.search(
            "编程",
            user_id="test_user",
            limit=1
        )
        print(f"✓ 搜索记忆成功，找到 {len(results)} 条结果")
        
        # 清理测试数据
        import shutil
        if os.path.exists("./test_chroma_storage"):
            shutil.rmtree("./test_chroma_storage")
            print("✓ 测试数据已清理")
        
        return True
        
    except Exception as e:
        print(f"✗ Mem0 + ChromaDB 测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n🔍 通义千问 + ChromaDB 配置检查\n")
    
    results = []
    
    # 运行测试
    results.append(("环境变量", test_environment()))
    results.append(("ChromaDB", test_chromadb()))
    
    # 只有环境变量配置正确才测试连接
    if results[0][1]:
        results.append(("通义千问连接", test_qwen_connection()))
    
    # 只有 ChromaDB 可用才测试集成
    if results[1][1]:
        results.append(("Mem0集成", test_mem0_with_chroma()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    # 给出建议
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！可以开始使用了")
        print("\n运行命令:")
        print("  python agent_local.py")
    else:
        print("⚠️  部分测试未通过，请根据上述提示进行配置")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

