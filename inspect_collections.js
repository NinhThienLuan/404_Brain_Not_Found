// MongoDB Inspect Collections Script
// Chạy: mongosh "mongodb://mongo:OtfagZQFKuslkxmpTCZTlvctRGsQBLnk@shortline.proxy.rlwy.net:21101/basic-hackathon?authSource=admin&directConnection=true" < inspect_collections.js

// Hoặc trong mongosh:
// load('inspect_collections.js')

print("\n========================================");
print("  🔍 MONGODB COLLECTIONS INSPECTOR");
print("========================================\n");

// Kết nối database
const db = db.getSiblingDB('basic-hackathon');

print("📊 Database: " + db.getName());
print("----------------------------------------\n");

// Lấy danh sách tất cả collections
const collections = db.getCollectionNames();

print("📁 Total Collections: " + collections.length);
print("----------------------------------------\n");

// Inspect từng collection
collections.forEach(function(collectionName) {
    print("\n┌─────────────────────────────────────");
    print("│ Collection: " + collectionName);
    print("└─────────────────────────────────────");
    
    const collection = db.getCollection(collectionName);
    
    // Đếm số documents
    const count = collection.countDocuments();
    print("  📊 Documents Count: " + count);
    
    if (count > 0) {
        // Lấy 1 document mẫu để xem structure
        print("\n  📄 Sample Document:");
        const sample = collection.findOne();
        printjson(sample);
        
        // Liệt kê tất cả fields trong collection
        print("\n  🔑 Fields:");
        const fields = Object.keys(sample);
        fields.forEach(function(field) {
            const type = typeof sample[field];
            const value = sample[field];
            let displayType = type;
            
            if (value === null) {
                displayType = "null";
            } else if (Array.isArray(value)) {
                displayType = "array [" + value.length + " items]";
            } else if (type === "object") {
                if (value.constructor.name === "ObjectId") {
                    displayType = "ObjectId";
                } else if (value.constructor.name === "Date") {
                    displayType = "Date";
                } else {
                    displayType = "object";
                }
            }
            
            print("    - " + field + ": " + displayType);
        });
        
        // Indexes
        print("\n  🔖 Indexes:");
        const indexes = collection.getIndexes();
        indexes.forEach(function(index) {
            print("    - " + index.name + ": " + JSON.stringify(index.key));
        });
        
        // Stats
        print("\n  📈 Stats:");
        const stats = collection.stats();
        print("    - Average Document Size: " + Math.round(stats.avgObjSize) + " bytes");
        print("    - Total Size: " + Math.round(stats.size / 1024) + " KB");
        print("    - Storage Size: " + Math.round(stats.storageSize / 1024) + " KB");
        
    } else {
        print("  ⚠️  Collection is empty");
    }
    
    print("\n");
});

// Summary
print("\n========================================");
print("  📊 SUMMARY");
print("========================================");

collections.forEach(function(collectionName) {
    const count = db.getCollection(collectionName).countDocuments();
    print("  " + collectionName + ": " + count + " documents");
});

print("\n✅ Inspection Complete!\n");
