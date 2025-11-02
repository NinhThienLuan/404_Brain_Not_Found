# 🔍 MongoDB Collections Inspector

## 📋 Mô tả:

Tools để inspect và xem chi tiết tất cả collections trong MongoDB database.

---

## 🚀 Cách sử dụng:

### **Option 1: Python Script** (Recommended) ⭐

```bash
python inspect_collections.py
```

**Output sẽ hiển thị:**
- ✅ Danh sách tất cả collections
- ✅ Số lượng documents trong mỗi collection
- ✅ Sample document (structure)
- ✅ Tất cả fields và types
- ✅ Indexes
- ✅ Collection stats (size, average doc size, etc.)
- ✅ Recent documents (3 latest)
- ✅ Database summary

**Ví dụ Output:**
```
========================================
  🔍 MONGODB COLLECTIONS INSPECTOR
========================================

📡 Connecting to MongoDB...
   Host: shortline.proxy.rlwy.net:21101
   Database: basic-hackathon

✓ Connected successfully!

📁 Total Collections: 5
------------------------------------------------------------

────────────────────────────────────────────────────────────
│ Collection: users
────────────────────────────────────────────────────────────
  📊 Documents Count: 2

  📄 Sample Document:
     "6906ae5b2484813d2b42c6db"

  🔑 Fields:
     - _id: ObjectId (6906ae5b2484813d2b42c6db)
     - name: string: Nguyễn Văn A
     - email: string: a@example.com
     - created_at: Date (2025-11-02T01:05:31.153000)

  🔖 Indexes:
     - _id_: {'_id': 1}

  📈 Stats:
     - Average Document Size: 123 bytes
     - Total Size: 0.24 KB
     - Storage Size: 20.00 KB

  📋 Recent Documents (Latest 3):
     1. ID: 6906ae692484813d2b42c6dc
        Created: 2025-11-02T01:05:45.823000
        Name: Trần Thị B
        Email: b@example.com
     2. ID: 6906ae5b2484813d2b42c6db
        Created: 2025-11-02T01:05:31.153000
        Name: Nguyễn Văn A
        Email: a@example.com

========================================
  📊 SUMMARY
========================================
  ✓ users........................................ 2 documents
  ✓ code_generations............................. 5 documents
  ✓ code_reviews................................. 3 documents
  ✗ execution_logs............................... 0 documents
  ✓ requests..................................... 1 documents

  TOTAL DOCUMENTS: 11

  Database Stats:
     - Data Size: 0.05 MB
     - Storage Size: 0.12 MB
     - Collections: 5
     - Indexes: 5

✅ Inspection Complete!
```

---

### **Option 2: JavaScript (mongosh)**

```bash
# Chạy trực tiếp
mongosh "mongodb://mongo:OtfagZQFKuslkxmpTCZTlvctRGsQBLnk@shortline.proxy.rlwy.net:21101/basic-hackathon?authSource=admin&directConnection=true" < inspect_collections.js

# Hoặc trong mongosh shell
load('inspect_collections.js')
```

---

### **Option 3: MongoDB Compass** (GUI)

1. Download MongoDB Compass: https://www.mongodb.com/products/compass
2. Connect string:
   ```
   mongodb://mongo:OtfagZQFKuslkxmpTCZTlvctRGsQBLnk@shortline.proxy.rlwy.net:21101/basic-hackathon?authSource=admin&directConnection=true
   ```
3. Browse collections visually

---

## 📊 Thông tin được hiển thị:

### **Per Collection:**
- 📊 **Documents Count** - Số lượng documents
- 📄 **Sample Document** - Một document mẫu
- 🔑 **Fields** - Tất cả fields và data types
- 🔖 **Indexes** - Các indexes đã được tạo
- 📈 **Stats** - Statistics (size, average, etc.)
- 📋 **Recent Documents** - 3 documents mới nhất

### **Database Summary:**
- ✅ Tổng số documents trong toàn bộ database
- 📊 Data size và Storage size
- 📁 Số lượng collections
- 🔖 Tổng số indexes

---

## 🎯 Use Cases:

### **1. Debug MongoDB Data:**
```bash
python inspect_collections.py
```
→ Xem structure của tất cả collections

### **2. Check Empty Collections:**
```bash
python inspect_collections.py | grep "empty"
```
→ Tìm collections trống

### **3. Verify Data After API Calls:**
1. Call API để tạo data
2. Run inspector
3. Verify data đã được lưu đúng

### **4. Monitor Database Growth:**
```bash
# Run định kỳ để xem database size
python inspect_collections.py | grep "TOTAL DOCUMENTS"
```

---

## 🔧 Customization:

### **Thay đổi số recent documents:**

Trong `inspect_collections.py`, line ~120:
```python
recent = list(collection.find().sort("_id", -1).limit(3))  # Đổi 3 thành số khác
```

### **Filter specific collection:**

```python
# Chỉ inspect 1 collection
for coll_name in ["users"]:  # Thay vì collection_names
    ...
```

### **Export to JSON:**

```bash
python inspect_collections.py > collections_report.json
```

---

## 📝 Quick Commands:

```bash
# Inspect tất cả
python inspect_collections.py

# Chỉ xem summary
python inspect_collections.py | grep -A 20 "SUMMARY"

# Count total documents
python inspect_collections.py | grep "TOTAL DOCUMENTS"

# Xem collections có data
python inspect_collections.py | grep "Documents Count"
```

---

## 🐛 Troubleshooting:

### **Lỗi connection:**
```bash
# Test connection trước
python test_connection.py
```

### **Không thấy collections:**
→ Database có thể trống hoặc sai tên database

### **Lỗi permission:**
→ Check MongoDB credentials trong `.env`

---

## 💡 Tips:

### **1. Chạy trước khi test API:**
```bash
# 1. Inspect hiện tại
python inspect_collections.py > before.txt

# 2. Call API
curl -X POST "http://localhost:8000/api/users/" -d '{...}'

# 3. Inspect lại
python inspect_collections.py > after.txt

# 4. So sánh
diff before.txt after.txt
```

### **2. Monitor trong development:**
```bash
# Watch mode (Linux/Mac)
watch -n 5 python inspect_collections.py

# PowerShell (Windows)
while($true) { cls; python inspect_collections.py; sleep 5 }
```

### **3. Export specific collection:**
```bash
# Sử dụng mongoexport
mongoexport --uri="mongodb://..." --collection=users --out=users.json
```

---

## 📚 Related Tools:

- `test_connection.py` - Test MongoDB connection
- `test_user_api.py` - Test User API
- MongoDB Compass - GUI tool
- Studio 3T - Advanced MongoDB IDE

---

## 🎨 Features:

✅ **Color-coded output** - Dễ đọc  
✅ **Comprehensive stats** - Đầy đủ thông tin  
✅ **Recent documents** - Xem data mới nhất  
✅ **Field types** - Hiểu structure  
✅ **Database summary** - Overview nhanh  
✅ **Empty collection detection** - Tìm lỗi  
✅ **Size metrics** - Monitor storage  

---

## 🚀 Example Usage:

```bash
# Scenario 1: Verify sau khi tạo user
$ python inspect_collections.py
# → Xem collection "users" có 1 document mới

# Scenario 2: Check tất cả collections
$ python inspect_collections.py | grep "Collection:"
# → List tất cả collections

# Scenario 3: Find empty collections
$ python inspect_collections.py | grep -B1 "empty"
# → Tìm collections trống
```

---

Happy inspecting! 🔍✨

