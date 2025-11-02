"""
Python Script để inspect MongoDB collections
Dễ chạy hơn JavaScript version
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import json
from datetime import datetime

load_dotenv()

# ANSI colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_section(title, char="="):
    """Print section header"""
    print(f"\n{BLUE}{char*60}")
    print(f"  {title}")
    print(f"{char*60}{RESET}\n")

def print_subsection(title):
    """Print subsection"""
    print(f"\n{YELLOW}{'─'*60}")
    print(f"│ {title}")
    print(f"{'─'*60}{RESET}")

def format_value(value):
    """Format value for display"""
    if value is None:
        return "null"
    elif isinstance(value, list):
        return f"array [{len(value)} items]"
    elif isinstance(value, dict):
        return f"object [{len(value)} fields]"
    elif isinstance(value, datetime):
        return f"Date ({value.isoformat()})"
    elif isinstance(value, (int, float)):
        return f"{type(value).__name__} ({value})"
    elif isinstance(value, str):
        if len(value) > 50:
            return f"string ({len(value)} chars): {value[:50]}..."
        return f"string: {value}"
    else:
        return f"{type(value).__name__}"

def inspect_collections():
    """Inspect all MongoDB collections"""
    
    # Connect to MongoDB
    print_section("🔍 MONGODB COLLECTIONS INSPECTOR")
    
    username = os.getenv("MONGO_USERNAME", "mongo")
    password = os.getenv("MONGO_PASSWORD", "OtfagZQFKuslkxmpTCZTlvctRGsQBLnk")
    host = os.getenv("MONGO_HOST", "shortline.proxy.rlwy.net")
    port = int(os.getenv("MONGO_PORT", "21101"))
    database = os.getenv("MONGO_DATABASE", "basic-hackathon")
    
    password_encoded = quote_plus(password)
    uri = f"mongodb://{username}:{password_encoded}@{host}:{port}/{database}?authSource=admin&directConnection=true"
    
    print(f"📡 Connecting to MongoDB...")
    print(f"   Host: {host}:{port}")
    print(f"   Database: {database}\n")
    
    try:
        client = MongoClient(
            uri,
            directConnection=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        
        # Test connection
        client.admin.command('ping')
        print(f"{GREEN}✓ Connected successfully!{RESET}\n")
        
        db = client[database]
        
        # Get all collections
        collection_names = db.list_collection_names()
        
        print(f"{BOLD}📁 Total Collections: {len(collection_names)}{RESET}")
        print(f"{'-'*60}\n")
        
        summary = []
        
        # Inspect each collection
        for coll_name in collection_names:
            print_subsection(f"Collection: {coll_name}")
            
            collection = db[coll_name]
            count = collection.count_documents({})
            
            print(f"  📊 Documents Count: {BOLD}{count}{RESET}")
            
            if count > 0:
                # Get sample document
                sample = collection.find_one()
                
                print(f"\n  📄 {BOLD}Sample Document:{RESET}")
                print(f"     {json.dumps(str(sample['_id']) if '_id' in sample else 'N/A', indent=2)}")
                
                # List all fields
                print(f"\n  🔑 {BOLD}Fields:{RESET}")
                for field, value in sample.items():
                    if field == '_id':
                        print(f"     - {field}: ObjectId ({str(value)})")
                    else:
                        print(f"     - {field}: {format_value(value)}")
                
                # Show indexes
                print(f"\n  🔖 {BOLD}Indexes:{RESET}")
                indexes = collection.list_indexes()
                for idx in indexes:
                    print(f"     - {idx['name']}: {idx['key']}")
                
                # Show stats
                print(f"\n  📈 {BOLD}Stats:{RESET}")
                stats = db.command("collstats", coll_name)
                avg_size = stats.get('avgObjSize', 0)
                total_size = stats.get('size', 0)
                storage_size = stats.get('storageSize', 0)
                
                print(f"     - Average Document Size: {avg_size} bytes")
                print(f"     - Total Size: {total_size / 1024:.2f} KB")
                print(f"     - Storage Size: {storage_size / 1024:.2f} KB")
                
                # Show recent documents
                print(f"\n  📋 {BOLD}Recent Documents (Latest 3):{RESET}")
                recent = list(collection.find().sort("_id", -1).limit(3))
                for i, doc in enumerate(recent, 1):
                    doc_id = str(doc.get('_id', 'N/A'))
                    created = doc.get('created_at', 'N/A')
                    print(f"     {i}. ID: {doc_id}")
                    if created != 'N/A':
                        print(f"        Created: {created}")
                    
                    # Show key fields based on collection
                    if 'name' in doc:
                        print(f"        Name: {doc['name']}")
                    if 'email' in doc:
                        print(f"        Email: {doc['email']}")
                    if 'user_id' in doc:
                        print(f"        User ID: {doc['user_id']}")
                    if 'status' in doc:
                        print(f"        Status: {doc['status']}")
                    if 'language' in doc:
                        print(f"        Language: {doc['language']}")
                
            else:
                print(f"  {YELLOW}⚠️  Collection is empty{RESET}")
            
            summary.append((coll_name, count))
            print()
        
        # Print summary
        print_section("📊 SUMMARY")
        
        total_docs = 0
        for coll_name, count in summary:
            status = f"{GREEN}✓{RESET}" if count > 0 else f"{RED}✗{RESET}"
            print(f"  {status} {coll_name:.<40} {count:>6} documents")
            total_docs += count
        
        print(f"\n  {BOLD}TOTAL DOCUMENTS:{RESET} {total_docs}")
        
        # Database stats
        print(f"\n  {BOLD}Database Stats:{RESET}")
        db_stats = db.command("dbstats")
        print(f"     - Data Size: {db_stats.get('dataSize', 0) / 1024 / 1024:.2f} MB")
        print(f"     - Storage Size: {db_stats.get('storageSize', 0) / 1024 / 1024:.2f} MB")
        print(f"     - Collections: {db_stats.get('collections', 0)}")
        print(f"     - Indexes: {db_stats.get('indexes', 0)}")
        
        print(f"\n{GREEN}✅ Inspection Complete!{RESET}\n")
        
        client.close()
        
    except Exception as e:
        print(f"\n{RED}❌ Error: {str(e)}{RESET}\n")
        return False
    
    return True

if __name__ == "__main__":
    inspect_collections()

