from pymongo import MongoClient
import urllib.parse
import ssl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- URI + TLS 1.2 ---
username = os.getenv("MONGO_USERNAME", "mongo")
password = os.getenv("MONGO_PASSWORD", "OtfagZQFKuslkxmpTCZTlvctRGsQBLnk")
host = os.getenv("MONGO_HOST", "shortline.proxy.rlwy.net")
port = int(os.getenv("MONGO_PORT", "21101"))
database = os.getenv("MONGO_DATABASE", "basic-hackathon")

password_encoded = urllib.parse.quote_plus(password)
uri = f"mongodb://{username}:{password_encoded}@{host}:{port}/{database}?authSource=admin&directConnection=true"

print("🔌 Đang kết nối MongoDB...")
print(f"📍 Host: {host}:{port}")
print(f"📁 Database: {database}\n")

try:
    client = MongoClient(
        uri,
        directConnection=True,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000
    )
    
    # Test connection
    result = client.admin.command('ping')
    
    print("✅ KẾT NỐI THÀNH CÔNG!")
    print(f"📊 Ping: {result}")
    
    # List all databases
    dbs = client.list_database_names()
    print(f"📂 Databases ({len(dbs)}):")
    for db in dbs:
        print(f"   - {db}")
    
    # Test working database
    db = client[database]
    collections = db.list_collection_names()
    print(f"\n📦 Collections trong '{database}' ({len(collections)}):")
    if collections:
        for coll in collections:
            count = db[coll].count_documents({})
            print(f"   - {coll}: {count} documents")
    else:
        print("   (chưa có collection nào)")
    
    client.close()
    print("\n✅ Test hoàn tất!")
    
except Exception as e:
    print("❌ LỖI KẾT NỐI:")
    print(f"   {str(e)}")