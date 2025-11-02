# 🏗️ Architecture Documentation

## Tổng quan

Project sử dụng **Clean Architecture** với Entity-based design, tách biệt rõ ràng giữa các layer:

```
┌─────────────────────────────────────────────┐
│           Controller Layer (API)            │  ← FastAPI endpoints
├─────────────────────────────────────────────┤
│           Service Layer (Logic)             │  ← Business logic
├─────────────────────────────────────────────┤
│        Repository Layer (Database)          │  ← MongoDB operations
├─────────────────────────────────────────────┤
│           Entity Layer (Domain)             │  ← Domain models
└─────────────────────────────────────────────┘
```

---

## 📁 Cấu trúc Thư mục

```
BE/
├── entities/              # Domain entities (business objects)
│   ├── __init__.py
│   └── user_entity.py    # User domain model
│
├── repository/            # Data access layer
│   ├── __init__.py
│   └── user_repo.py      # User CRUD operations
│
├── service/               # Business logic layer
│   ├── __init__.py
│   └── user_service.py   # User business rules
│
├── controller/            # API layer
│   ├── __init__.py
│   └── user_controller.py # User API endpoints
│
├── models/                # Pydantic models (validation)
│   ├── __init__.py
│   └── user_model.py     # Request/Response models
│
└── main.py               # FastAPI application
```

---

## 🎯 Chi tiết từng Layer

### 1. **Entity Layer** (`entities/`)

**Mục đích:** Định nghĩa domain objects (business entities)

**Đặc điểm:**
- Pure Python dataclasses
- Không phụ thuộc vào database hay framework
- Chứa business logic cơ bản
- Dễ test, dễ maintain

**Ví dụ:**

```python
@dataclass
class User:
    name: str
    email: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Convert từ MongoDB document"""
        
    def to_dict(self) -> dict:
        """Convert sang MongoDB document"""
        
    def to_response(self) -> dict:
        """Convert sang API response"""
```

**Lợi ích:**
✅ Domain logic tập trung
✅ Dễ test (không cần mock database)
✅ Type-safe với IDE support
✅ Reusable across layers

---

### 2. **Repository Layer** (`repository/`)

**Mục đích:** Thao tác với database

**Đặc điểm:**
- Xử lý tất cả database operations
- Convert giữa entities và database documents
- Handle database errors
- Không chứa business logic

**Interface:**

```python
class UserRepository:
    def create(self, user: User) -> User
    def find_by_id(self, user_id: str) -> Optional[User]
    def find_by_email(self, email: str) -> Optional[User]
    def find_all(self, skip: int, limit: int) -> List[User]
    def update(self, user: User) -> Optional[User]
    def delete(self, user_id: str) -> bool
    def count(self, filter_query: dict) -> int
    def exists_by_email(self, email: str, exclude_id: str) -> bool
```

**Luồng dữ liệu:**

```
Controller → Service → Repository → MongoDB
                ↓           ↓
            Entity      Entity
```

**Lợi ích:**
✅ Single Responsibility (chỉ lo database)
✅ Dễ swap database (MongoDB → PostgreSQL)
✅ Centralized error handling
✅ Consistent data mapping

---

### 3. **Service Layer** (`service/`)

**Mục đích:** Business logic và validation

**Đặc điểm:**
- Xử lý business rules
- Validation logic
- Orchestrate repository calls
- Transaction handling (nếu cần)

**Interface:**

```python
class UserService:
    def create_user(self, name: str, email: str) -> User
    def get_user_by_id(self, user_id: str) -> Optional[User]
    def get_user_by_email(self, email: str) -> Optional[User]
    def get_all_users(self, page: int, page_size: int) -> Dict
    def update_user(self, user_id: str, name: str, email: str) -> Optional[User]
    def delete_user(self, user_id: str) -> bool
```

**Business Rules Example:**

```python
def create_user(self, name: str, email: str) -> User:
    # Validation
    if not name or not name.strip():
        raise ValueError("Tên không được để trống")
    
    # Business rule: email phải unique
    if self.repo.exists_by_email(email):
        raise ValueError("Email đã tồn tại")
    
    # Create entity
    user = User(name=name.strip(), email=email.strip())
    return self.repo.create(user)
```

**Lợi ích:**
✅ Business logic tập trung
✅ Dễ test (mock repository)
✅ Reusable across controllers
✅ Clean separation of concerns

---

### 4. **Controller Layer** (`controller/`)

**Mục đích:** HTTP API endpoints

**Đặc điểm:**
- Handle HTTP requests/responses
- Input validation (Pydantic)
- Convert entities to API responses
- Error handling (HTTP status codes)

**Example:**

```python
@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreateRequest):
    try:
        created_user = user_service.create_user(
            name=user.name,
            email=user.email
        )
        return created_user.to_response()  # Entity → Dict
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Lợi ích:**
✅ HTTP-specific logic isolated
✅ Auto-generated API docs (Swagger)
✅ Type-safe requests (Pydantic)
✅ Consistent error responses

---

## 🔄 Data Flow

### Create User Flow:

```
1. Client Request
   POST /api/users/
   {"name": "John", "email": "john@example.com"}
   
2. Controller (user_controller.py)
   ├─ Validate request (Pydantic)
   └─ Call service.create_user()
   
3. Service (user_service.py)
   ├─ Validate business rules
   ├─ Check email uniqueness
   ├─ Create User entity
   └─ Call repo.create()
   
4. Repository (user_repo.py)
   ├─ Convert entity to MongoDB document
   ├─ Insert into database
   ├─ Get inserted ID
   └─ Return User entity with ID
   
5. Service
   └─ Return User entity to controller
   
6. Controller
   ├─ Convert entity to response dict
   └─ Return JSON response
   
7. Client receives:
   {
     "_id": "123...",
     "name": "John",
     "email": "john@example.com",
     "created_at": "2025-11-02T..."
   }
```

### Get User Flow:

```
Client → Controller → Service → Repository → MongoDB
                                      ↓
                                  User entity
                                      ↓
Client ← Response ← Controller ← Service ← Repository
```

---

## 🎨 Design Patterns

### 1. **Repository Pattern**
- Abstraction layer cho database operations
- Dễ test, dễ swap implementation

### 2. **Service Pattern**
- Centralize business logic
- Reusable across controllers

### 3. **Data Transfer Object (DTO)**
- Pydantic models cho API validation
- Entity classes cho domain logic

### 4. **Dependency Injection**
- Service inject Repository
- Controller inject Service

---

## ✨ Lợi ích của Architecture này

### 1. **Separation of Concerns**
- Mỗi layer có trách nhiệm riêng
- Dễ maintain và extend

### 2. **Testability**
```python
# Test Service (mock Repository)
def test_create_user():
    mock_repo = Mock()
    service = UserService(repo=mock_repo)
    service.create_user("John", "john@example.com")
    mock_repo.create.assert_called_once()
```

### 3. **Type Safety**
- IDE autocomplete
- Catch errors at compile time
- Better refactoring support

### 4. **Scalability**
- Dễ thêm features mới
- Dễ thay đổi database
- Dễ thêm caching, logging, etc.

### 5. **Reusability**
- Service có thể dùng cho multiple controllers
- Repository có thể dùng cho multiple services
- Entity có thể dùng across project

---

## 🔧 Extend Architecture

### Thêm Entity mới (vd: Post):

1. **Create Entity** (`BE/entities/post_entity.py`)
```python
@dataclass
class Post:
    title: str
    content: str
    user_id: str
    id: Optional[str] = None
```

2. **Create Repository** (`BE/repository/post_repo.py`)
```python
class PostRepository:
    def create(self, post: Post) -> Post: ...
```

3. **Create Service** (`BE/service/post_service.py`)
```python
class PostService:
    def create_post(self, title, content, user_id) -> Post: ...
```

4. **Create Controller** (`BE/controller/post_controller.py`)
```python
@router.post("/")
async def create_post(post: PostCreateRequest): ...
```

---

## 📚 Best Practices

### 1. **Entity Rules**
- ✅ Pure Python objects
- ✅ No framework dependencies
- ✅ Include domain logic
- ❌ No database-specific code

### 2. **Repository Rules**
- ✅ Only database operations
- ✅ Return entities (not dicts)
- ✅ Handle database errors
- ❌ No business logic

### 3. **Service Rules**
- ✅ Business logic only
- ✅ Validate input
- ✅ Orchestrate repositories
- ❌ No HTTP-specific code

### 4. **Controller Rules**
- ✅ HTTP handling only
- ✅ Convert entities to responses
- ✅ Handle HTTP errors
- ❌ No business logic

---

## 🎯 So sánh với Architecture cũ

### Trước (Dict-based):

```python
# Repository trả về dict
def find_by_id(self, user_id: str) -> dict:
    return self.collection.find_one({"_id": ObjectId(user_id)})

# Service xử lý dict
def get_user(self, user_id: str) -> dict:
    user = self.repo.find_by_id(user_id)
    return {"_id": str(user["_id"]), "name": user["name"], ...}
```

**Vấn đề:**
❌ Không type-safe
❌ Dễ nhầm lẫn field names
❌ Khó refactor
❌ Không có IDE support

### Sau (Entity-based):

```python
# Repository trả về Entity
def find_by_id(self, user_id: str) -> Optional[User]:
    data = self.collection.find_one({"_id": ObjectId(user_id)})
    return User.from_dict(data) if data else None

# Service xử lý Entity
def get_user(self, user_id: str) -> Optional[User]:
    return self.repo.find_by_id(user_id)
```

**Lợi ích:**
✅ Type-safe
✅ IDE autocomplete
✅ Dễ refactor
✅ Clean và maintainable

---

## 🚀 Next Steps

- [ ] Add caching layer (Redis)
- [ ] Add logging/monitoring
- [ ] Add authentication (JWT)
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Add API rate limiting
- [ ] Add database migration tool

