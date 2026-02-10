"""
[파일 역할]
수집된 치과 지식 데이터(JSON)를 로컬 벡터 데이터베이스(Milvus Lite)에 적재하는 스크립트입니다.
RAG 시스템이 지식을 검색할 수 있도록 '학습 데이터'를 DB에 밀어넣는 전처리 단계에 해당합니다.

[실행 방법]
프로젝트 루트에서 아래 명령어를 실행합니다.
$ export PYTHONPATH=$PYTHONPATH:.
$ python3 src/denticheck_ai/pipelines/rag/ingest.py

[동작 순서]
1. `data/snudh_knowledge.json` 파일을 읽어옵니다.
2. 각 데이터를 LangChain의 `Document` 객체로 변환합니다.
3. 로컬 임베딩 모델(`ko-sroberta`)을 로드합니다.
4. Milvus Standalone(또는 Lite)을 사용하여 벡터화된 데이터를 저장합니다.
"""

import json
import os
from dotenv import load_dotenv
from langchain_milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# 환경 변수 로드
load_dotenv()

def ingest_data():
    """
    JSON 지식 베이스 데이터를 읽어 임베딩 과정을 거친 후 Milvus DB에 적재합니다.
    기존 데이터가 있을 경우 삭제하고 새로 적재(drop_old=True)합니다.
    """
    json_path = "data/snudh_knowledge.json"
    
    if not os.path.exists(json_path):
        print(f"[에러] {json_path} 파일이 존재하지 않습니다.")
        return

    # 1. 데이터 로드
    with open(json_path, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)

    # 2. Document 객체로 변환
    documents = []
    for item in knowledge_base:
        if not item['content']: continue
        
        doc = Document(
            page_content=item['content'],
            metadata={
                "title": item['title'],
                "source": item['source'],
                "url": item['url']
            }
        )
        documents.append(doc)

    print(f"총 {len(documents)}건의 문서를 준비했습니다.")

    # 3. 로컬 임베딩 모델 설정 (OpenAI 대신 로컬 모델 사용)
    # 한국어 성능이 우수한 jhgan/ko-sroberta-multitask 모델 사용
    print("로컬 임베딩 모델 로드 중 (처음 실행 시 수백 MB 다운로드가 필요할 수 있습니다)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        model_kwargs={'device': 'cpu'}, # GPU가 있다면 'cuda'로 변경 가능
        encode_kwargs={'normalize_embeddings': True}
    )

    # 4. Milvus 연결 및 적재
    # Standalone일 경우 uri는 'http://localhost:19530' 형태, 
    # Lite일 경우 './data/milvus_dental.db' 형태입니다.
    milvus_uri = os.getenv("MILVUS_URI", "./data/milvus_dental.db")
    collection_name = os.getenv("COLLECTION_NAME", "dental_knowledge")

    print(f"Milvus 연결 중... (URI: {milvus_uri})")
    
    try:
        vector_db = Milvus.from_documents(
            documents,
            embeddings,
            connection_args={
                "uri": milvus_uri,
            },
            collection_name=collection_name,
            drop_old=True # 기존 데이터 삭제 후 새로 적재
        )
        print(f"성공적으로 {len(documents)}건의 지식을 Milvus({milvus_uri})에 적재했습니다.")
    except Exception as e:
        print(f"[에러] Milvus 적재 실패: {e}")

if __name__ == "__main__":
    ingest_data()
