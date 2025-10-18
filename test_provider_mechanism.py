"""
测试为什么 provider 配置为 openai 能调用千问服务
验证 OpenAI 兼容接口机制
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_openai_compatible_interface():
    """测试 OpenAI 兼容接口"""
    print("=" * 60)
    print("🧪 测试 OpenAI 兼容接口机制")
    print("=" * 60)
    
    # 获取千问 API Key
    llm_api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if not llm_api_key:
        print("❌ 错误: 请设置 DEFAULT_LLM_API_KEY 环境变量")
        return
    
    # 设置环境变量
    os.environ["OPENAI_API_KEY"] = llm_api_key
    os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    print(f"🔑 API Key: {llm_api_key[:10]}...")
    print(f"🌐 Base URL: {os.environ['OPENAI_BASE_URL']}")
    
    # 创建 OpenAI 客户端（实际连接到千问）
    client = OpenAI(
        api_key=llm_api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    print("\n🔄 测试文本嵌入...")
    
    try:
        # 测试嵌入功能
        response = client.embeddings.create(
            model="text-embedding-v1",
            input="这是一个测试文本"
        )
        
        embedding = response.data[0].embedding
        print(f"✅ 嵌入成功!")
        print(f"📊 向量维度: {len(embedding)}")
        print(f"📊 向量前5个值: {embedding[:5]}")
        
        # 测试不同文本的嵌入
        test_texts = [
            "我喜欢吃苹果",
            "今天天气很好", 
            "苹果是一种水果"
        ]
        
        print(f"\n🔄 测试多个文本嵌入...")
        for text in test_texts:
            response = client.embeddings.create(
                model="text-embedding-v1",
                input=text
            )
            embedding = response.data[0].embedding
            print(f"✅ '{text}' -> 维度: {len(embedding)}")
        
        print(f"\n🎉 OpenAI 兼容接口测试成功!")
        print(f"💡 这就是为什么 Mem0 的 'openai' provider 能调用千问服务")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_mem0_with_environment_variables():
    """测试 Mem0 如何使用环境变量"""
    print("\n" + "=" * 60)
    print("🧪 测试 Mem0 环境变量机制")
    print("=" * 60)
    
    from mem0 import Memory
    
    # 获取千问 API Key
    llm_api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if not llm_api_key:
        print("❌ 错误: 请设置 DEFAULT_LLM_API_KEY 环境变量")
        return
    
    # 设置环境变量让 Mem0 使用千问
    os.environ["OPENAI_API_KEY"] = llm_api_key
    os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    print(f"🔑 环境变量 OPENAI_API_KEY: {os.environ.get('OPENAI_API_KEY', 'Not Set')[:10]}...")
    print(f"🌐 环境变量 OPENAI_BASE_URL: {os.environ.get('OPENAI_BASE_URL', 'Not Set')}")
    
    # 配置 Mem0
    config = {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "test_env_vars",
                "path": "./test_env_storage",
            }
        },
        "llm": {
            "provider": "openai",  # 使用 openai provider
            "config": {
                "model": "qwen-plus",  # 但指定千问模型
            }
        },
        "embedder": {
            "provider": "openai",  # 使用 openai provider
            "config": {
                "model": "text-embedding-v1",  # 但指定千问嵌入模型
            }
        }
    }
    
    try:
        print(f"\n🔄 初始化 Mem0 Memory...")
        memory = Memory.from_config(config)
        print(f"✅ Memory 初始化成功")
        
        # 测试添加记忆
        print(f"\n🔄 测试添加记忆...")
        result = memory.add(
            "这是一个通过环境变量配置的测试",
            user_id="test_user"
        )
        print(f"✅ 添加记忆成功")
        
        # 测试搜索
        print(f"\n🔄 测试搜索...")
        results = memory.search("测试", user_id="test_user", limit=1)
        print(f"✅ 搜索成功，找到 {len(results.get('results', []))} 个结果")
        
        print(f"\n🎉 Mem0 环境变量机制测试成功!")
        print(f"💡 Mem0 的 'openai' provider 会自动读取环境变量")
        print(f"💡 所以即使配置为 'openai'，实际调用的是千问服务")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    # 测试 OpenAI 兼容接口
    test_openai_compatible_interface()
    
    # 测试 Mem0 环境变量机制
    test_mem0_with_environment_variables()
    
    print("\n" + "=" * 60)
    print("📝 总结:")
    print("1. 千问提供 OpenAI 兼容的 API 接口")
    print("2. Mem0 的 'openai' provider 会读取环境变量")
    print("3. 通过设置 OPENAI_API_KEY 和 OPENAI_BASE_URL 重定向到千问")
    print("4. 所以 'openai' provider 实际上调用的是千问服务")
    print("=" * 60)
