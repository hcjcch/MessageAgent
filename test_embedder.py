"""
测试 Mem0 embedder 模型
验证文本嵌入功能是否正常工作
"""

import os
from mem0 import Memory
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_embedder():
    """测试 embedder 模型"""
    print("=" * 60)
    print("🧪 测试 Mem0 Embedder 模型")
    print("=" * 60)
    
    # 获取 API Key
    llm_api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if not llm_api_key:
        print("❌ 错误: 请设置 DEFAULT_LLM_API_KEY 环境变量")
        return
    
    # 设置环境变量让 Mem0 使用千问
    os.environ["OPENAI_API_KEY"] = llm_api_key
    os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # 配置 Mem0
    config = {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "test_embedder",
                "path": "./test_embedder_storage",
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
    
    try:
        # 初始化 Memory
        print("🔄 初始化 Mem0 Memory...")
        memory = Memory.from_config(config)
        print("✅ Memory 初始化成功")
        
        # 测试文本
        test_texts = [
            "我喜欢吃苹果",
            "今天天气很好",
            "我在学习人工智能",
            "苹果是一种水果",
            "人工智能很有趣"
        ]
        
        print(f"\n📝 测试文本数量: {len(test_texts)}")
        print("测试文本:")
        for i, text in enumerate(test_texts, 1):
            print(f"  {i}. {text}")
        
        # 添加文本到记忆
        print(f"\n🔄 添加文本到记忆...")
        for i, text in enumerate(test_texts):
            try:
                result = memory.add(
                    text, 
                    user_id="test_user",
                    metadata={"test_id": i, "category": "test"}
                )
                print(f"✅ 添加成功: {text[:20]}...")
            except Exception as e:
                print(f"❌ 添加失败: {text[:20]}... - {e}")
        
        # 测试搜索功能
        print(f"\n🔍 测试搜索功能...")
        search_queries = [
            "水果",
            "天气",
            "学习",
            "苹果"
        ]
        
        for query in search_queries:
            print(f"\n🔍 搜索: '{query}'")
            try:
                results = memory.search(
                    query, 
                    user_id="test_user",
                    limit=3
                )
                
                if isinstance(results, dict) and 'results' in results:
                    results = results['results']
                
                if results:
                    print(f"✅ 找到 {len(results)} 个相关结果:")
                    for j, result in enumerate(results, 1):
                        memory_text = result.get("memory", "")
                        score = result.get("score", 0)
                        print(f"  {j}. {memory_text} (相似度: {score:.3f})")
                else:
                    print("❌ 未找到相关结果")
                    
            except Exception as e:
                print(f"❌ 搜索失败: {e}")
        
        # 测试获取所有记忆
        print(f"\n📚 获取所有记忆...")
        try:
            all_memories = memory.get_all(user_id="test_user")
            if isinstance(all_memories, dict) and 'results' in all_memories:
                all_memories = all_memories['results']
            
            print(f"✅ 总共找到 {len(all_memories)} 条记忆:")
            for i, memory_item in enumerate(all_memories, 1):
                memory_text = memory_item.get("memory", "")
                created_at = memory_item.get("created_at", "")
                print(f"  {i}. {memory_text}")
                if created_at:
                    print(f"     时间: {created_at}")
        except Exception as e:
            print(f"❌ 获取记忆失败: {e}")
        
        print(f"\n✅ Embedder 测试完成!")
        print(f"📁 数据存储路径: ./test_embedder_storage")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n💡 可能的原因:")
        print("1. 网络连接问题")
        print("2. API Key 无效")
        print("3. 千问服务不可用")
        print("4. ChromaDB 安装问题")

def test_embedder_with_different_models():
    """测试不同的嵌入模型"""
    print("\n" + "=" * 60)
    print("🧪 测试不同嵌入模型")
    print("=" * 60)
    
    # 获取 API Key
    llm_api_key = os.getenv("DEFAULT_LLM_API_KEY")
    if not llm_api_key:
        print("❌ 错误: 请设置 DEFAULT_LLM_API_KEY 环境变量")
        return
    
    # 设置环境变量
    os.environ["OPENAI_API_KEY"] = llm_api_key
    os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # 测试不同的嵌入模型
    embedder_models = [
        "text-embedding-v1",
        "text-embedding-3-small", 
        "text-embedding-3-large"
    ]
    
    for model in embedder_models:
        print(f"\n🔄 测试模型: {model}")
        try:
            config = {
                "vector_store": {
                    "provider": "chroma",
                    "config": {
                        "collection_name": f"test_{model.replace('-', '_')}",
                        "path": f"./test_embedder_storage_{model.replace('-', '_')}",
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
                        "model": model,
                    }
                }
            }
            
            memory = Memory.from_config(config)
            
            # 添加测试文本
            test_text = f"这是使用 {model} 模型的测试文本"
            result = memory.add(test_text, user_id="test_user")
            
            # 搜索测试
            search_results = memory.search("测试", user_id="test_user", limit=1)
            
            print(f"✅ {model} 模型测试成功")
            
        except Exception as e:
            print(f"❌ {model} 模型测试失败: {e}")

if __name__ == "__main__":
    # 基础测试
    test_embedder()
    
    # 自动测试不同模型
    print("\n" + "=" * 60)
    print("🔄 自动测试不同嵌入模型...")
    test_embedder_with_different_models()
    
    print("\n🎉 所有测试完成!")
