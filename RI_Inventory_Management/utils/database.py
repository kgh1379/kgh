from pymongo import MongoClient

# Create MongoDB client and connect to database
def get_db_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["nuclear_medicine"]
    return db

# 보관 항목 조회
def get_storage_items():
    db = get_db_connection()
    storage_items = list(db.storage.find({}))  # 'storage' 컬렉션에서 모든 문서 조회
    return storage_items

# 폐기 항목 조회
def get_disposal_items():
    db = get_db_connection()
    disposal_items = list(db.disposal.find({}))  # 'disposal' 컬렉션에서 모든 문서 조회
    return disposal_items

# 입고 항목 삽입
def insert_stock_item(item):
    db = get_db_connection()
    db.stock.insert_one(item)  # 'stock' 컬렉션에 새 문서 삽입

# 사용 내역 삽입
def insert_usage_log(log):
    db = get_db_connection()
    db.usage_logs.insert_one(log)  # 'usage_logs' 컬렉션에 새 문서 삽입
