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
    json 데이터를 읽어 Milvus DB에 적재합니다.
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

    # 4. Milvus 연결 및 적재 (Lite 방식 - 로컬 파일 저장)
    # 별도의 서버 설치 없이 ./milvus_dental.db 파일에 저장됨
    # ./ 로 시작하는 경로를 사용해야 Lite 모드로 안정적으로 인식됩니다.
    milvus_path = "./data/milvus_dental.db"
    collection_name = "dental_knowledge"

    print(f"Milvus Lite 초기화 중... (데이터 저장소: {milvus_path})")
    
    try:
        vector_db = Milvus.from_documents(
            documents,
            embeddings,
            connection_args={
                "uri": milvus_path,
            },
            collection_name=collection_name,
            drop_old=True # 기존 데이터 삭제 후 새로 적재
        )
        print(f"성공적으로 {len(documents)}건의 지식을 Milvus Lite({milvus_path})에 적재했습니다.")
    except Exception as e:
        print(f"[에러] Milvus 적재 실패: {e}")

if __name__ == "__main__":
    ingest_data()
