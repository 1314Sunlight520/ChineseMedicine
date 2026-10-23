"""
FAISS 向量搜索 Demo
接收一个文本，使用 embedding 模型转换为向量，搜索最相似的 top3 文本
"""
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from common.config import Config
from common.path_utils import get_file_path

conf = Config()
# 索引文件路径
INDEX_PATH = get_file_path("__000__demo/faiss_index.index")
ID2TEXT_PATH = get_file_path("__000__demo/faiss_id2text.pkl")


def get_embedding_model():
    """
    获取或初始化 embedding 模型
    优先使用配置中的模型路径，否则使用默认的中文模型
    """
    embedding_model = SentenceTransformer(conf.EMBEDDING_MODEL_PATH)
    return embedding_model


def text_to_embedding(text: str) -> np.ndarray:
    """
    将单个文本转换为 embedding 向量
    
    Args:
        text: 输入文本
    
    Returns:
        numpy array, shape (dimension,) - 向量
    """
    model = get_embedding_model()
    embedding = model.encode([text], convert_to_numpy=True)[0]
    return embedding.astype('float32')


def load_index(index_path: str = INDEX_PATH):
    """
    加载 FAISS 索引
    
    Args:
        index_path: 索引文件路径
    
    Returns:
        faiss.Index: 加载的索引对象
    """

    print(f"正在加载索引: {index_path}")
    index = faiss.read_index(index_path)
    return index


def load_id2text(id2text_path: str = ID2TEXT_PATH):
    """
    加载 ID 到文本的映射
    
    Args:
        id2text_path: 映射文件路径
    
    Returns:
        dict: ID 到文本的映射字典
    """

    print(f"正在加载 ID 到文本的映射: {id2text_path}")
    with open(id2text_path, 'rb') as f:
        id2text = pickle.load(f)
    print(f"映射加载成功！包含 {len(id2text)} 个条目")

    return id2text


def search_similar_texts(index: faiss.Index, query_text: str, k: int = 3):
    """
    搜索最相似的文本
    
    Args:
        index: FAISS 索引对象
        query_text: 查询文本
        k: 返回最相似的 k 个文本（默认3）
    
    Returns:
        distances: 距离数组，shape (k,)
        indices: 索引数组，shape (k,)
    """
    # 将查询文本转换为向量
    query_vector = text_to_embedding(query_text)

    # 归一化查询向量（与存储时的归一化保持一致）
    query_vector = query_vector.reshape(1, -1)
    # 归一化向量
    faiss.normalize_L2(query_vector)

    # 搜索
    distances, indices = index.search(query_vector, k)

    return distances[0], indices[0]


def search_with_threshold(index: faiss.Index, query_text: str, k: int = 3, threshold: float = 0.5,
                          id2text: dict = None):
    """
    搜索最相似文本，返回 top-k 中相似度 >= 阈值的结果

    Args:
        index: FAISS 索引
        query_text: 查询文本
        k: top-k 数量
        threshold: 相似度阈值
        id2text: 映射字典

    Returns:
        filtered_results: list, Top-k 中满足阈值的结果
    """
    distances, indices = search_similar_texts(index, query_text, k)

    filtered_results = []

    for dist, idx in zip(distances, indices):
        similarity = 1 / (1 + dist)
        if similarity >= threshold:
            filtered_results.append({
                "id": int(idx),
                "distance": float(dist),
                "similarity": float(similarity),
                "text": id2text.get(int(idx), "未知文本")
            })

    return filtered_results


def display_results(query_text: str, distances: np.ndarray, indices: np.ndarray, id2text: dict = None):
    """
    显示搜索结果
    
    Args:
        query_text: 查询文本
        distances: 距离数组
        indices: 索引数组
        id2text: ID 到文本的映射（可选）
    """
    print(f"查询文本: {query_text}")
    print(f"\n找到 {len(distances)} 个相似文本（Top {len(distances)}）:")

    for i, (distance, idx) in enumerate(zip(distances, indices), 1):
        print(f"\n排名 {i}:")
        print(f"  相似度分数: {1 / (1 + distance):.4f}")  # 将距离转换为相似度分数
        print(f"  距离: {distance:.6f}")
        print(f"  文本: {id2text.get(idx, '未知文本')}")


def search_text(query_text: str, k: int = 3):
    """
    搜索相似文本的主函数
    
    Args:
        query_text: 查询文本
        k: 返回最相似的 k 个文本（默认3）
    """
    # 1、加载索引
    print("\n1. 加载 FAISS 索引文件...")
    index = load_index()

    # 2、加载 ID 到文本的映射
    print("\n2. 加载 ID 到文本的映射...")
    id2text = load_id2text()

    # 3、搜索相似文本
    print(f"\n3. 搜索与 '{query_text}' 最相似的 {k} 个文本...")
    distances, indices = search_similar_texts(index, query_text, k)

    # 4、显示结果
    display_results(query_text, distances, indices, id2text)

    return distances, indices, id2text


def main():
    """主函数"""
    index = load_index()
    id2text = load_id2text()

    query_text = "感冒都有什么症状？"
    threshold = 0.5

    results = search_with_threshold(index, query_text, k=3, threshold=threshold, id2text=id2text)

    print("=== Top-k 过滤后结果 ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
