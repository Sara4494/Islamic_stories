# 📘 API Documentation

**Base URL:**  
```
https://islamicstories.pythonanywhere.com/
```

---

## 🧾 Headers المشتركة

كل الطلبات (ما عدا Google Callback) لازم تحتوي على:

```
Content-Type: application/json
```

ولو المستخدم مسجّل دخول:
```
Authorization: Token <USER_TOKEN>
```

---

## 📌 Endpoints

### 1) Register (تسجيل مستخدم جديد)

**Endpoint:**  
```
POST /register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "full_name": "User Name",
  "password": "123456",
  "confirm_password": "123456"
}
```

**Response (201 Created):**
```json
{
  "email": "user@example.com",
  "full_name": "User Name",
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab"
}
```

**Errors:**
- إذا الباسوردين مختلفين:
```json
{
  "password": "Passwords do not match"
}
```

- إذا الإيميل موجود بالفعل:
```json
{
  "email": ["user with this email already exists."]
}
```

---

### 2) Login (تسجيل الدخول)

**Endpoint:**  
```
POST /login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

**Response (200 OK):**
```json
{
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab"
}
```

**Errors (400 Bad Request):**
```json
{
  "error": "Invalid credentials"
}
```

---

### 3) Google Login (Callback)

**Endpoint:**  
```
GET /api/auth/google/callback/?code=<GOOGLE_AUTH_CODE>
```

**Response (200 OK):**
```json
{
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab",
  "user": {
    "email": "user@gmail.com",
    "full_name": "User Google"
  }
}
```

**Errors:**
- لو مفيش كود:
```json
{
  "error": "No code provided"
}
```

- خطأ من Google:
```json
{
  "error": "invalid_grant",
  "error_description": "Bad Request"
}
```


### 4) Request Password Reset (إرسال OTP على الإيميل)

**Endpoint:**  
```
POST /password-reset/
```

**Request Body:**  
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**  
```json
{
  "message": "OTP sent to your email!"
}
```

**Errors:**  
- لو الإيميل مش موجود:  
```json
{
  "error": "No user with this email"
}
```  
- لو الإيميل مش متبعت:  
```json
{
  "error": "Email required"
}
```

---

### 5) Confirm OTP & Reset Password (تأكيد OTP + تعيين باسورد جديد)

**Endpoint:**  
```
POST /password-reset-confirm/
```

**Request Body:**  
```json
{
  "email": "user@example.com",
  "otp": "123456",
  "password": "new_password123",
  "confirm_password": "new_password123"
}
```

**Response (200 OK):**  
```json
{
  "message": "Password reset successful!"
}
```

**Errors:**  
- لو الباسوردين مش متطابقين:  
```json
{
  "error": "Passwords do not match"
}
```  

- لو OTP مش صحيح:  
```json
{
  "error": "Invalid OTP"
}
```  

- لو OTP منتهي:  
```json
{
  "error": "OTP expired"
}
```


---







# 🛡️ Admin Login API Documentation

## 🔹 Endpoint

```
POST /auth/admin/login/
```

## 🔹 Description

* تسجيل دخول للـ Admin فقط.
* يرجع توكن يمكن استخدامه للوصول لكل الـ dashboard endpoints.
* أي يوزر عادي (`is_staff=False`) سيرفض الدخول برسالة خطأ.

## 🔹 Request Body (JSON)

```json
{
  "email": "admin@example.com",
  "password": "adminpassword"
}
```

## 🔹 Response (Success)

```json
{
  "message": "Admin login successful",
  "token": "d7aab849cf8ad83dfb5d4e44f4c64a1191721362",
  "user": {
    "email": "admin@example.com",
    "full_name": "Admin Name"
  }
}
```

## 🔹 Response (Invalid credentials)

```json
{
  "error": "Invalid credentials"
}
```

## 🔹 Response (Not an admin)

```json
{
  "error": "Admin credentials required"
}
```

## 🔹 Permissions

* متاح لأي شخص يدخل بيانات صحيحة للـ admin.
* يوزر عادي لا يمكنه تسجيل الدخول هنا.

## 🔹 Headers (Postman)

```
Content-Type: application/json
```

## 🔹 Usage Example (Postman)

1. اختر **POST** method.
2. ضع URL:

```
 
```

3. في Body اختر **raw → JSON** وأدخل بيانات admin.
4. اضغط **Send** لتحصل على الـ token.

> استخدم الـ token في الـ Headers لكل الـ dashboard requests:

```
Authorization: Token <your_admin_token>
```




---

## 🖼️ البانرات (Banners)

### 🔹 إضافة بانر
```
POST /banners/
```
**Body:**
```json
{
  "title": "بانر رئيسي",
  "description": "مرحبا",
  "image": "file.png",
  "link": "https://example.com"
}
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم إضافة البانر بنجاح 🎉", "data": {...} }
```

### 🔹 عرض كل البانرات
```
GET /banners/
```
**Permissions:** Authenticated users + admin  
**Response:**  
```json
[ {...}, {...} ]
```

### 🔹 عرض بانر واحد
```
GET /banners/{id}/
```
**Permissions:** Authenticated users + admin  

### 🔹 تعديل بانر
```
PUT /banners/{id}/
```
**Permissions:** Admin only  
**Response:**  
```json
{ "message": "تم تحديث بيانات البانر ✅", "data": {...} }
```

### 🔹 حذف بانر
```
DELETE /banners/{id}/
```
**Permissions:** Admin only  
**Response:**  
```json
{ "message": "تم حذف البانر 🗑️" }
```

---

## 📂 الأقسام (Categories)

### 🔹 إضافة قسم
```
POST /stories/categories/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم إضافة القسم بنجاح 🎉", "data": {...} }
```

### 🔹 عرض كل الأقسام
```
GET /stories/categories/
```
**Permissions:** Authenticated users + admin  

### 🔹 تعديل قسم
```
PUT /stories/categories/{id}/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم تحديث القسم ✅", "data": {...} }
```

### 🔹 حذف قسم
```
DELETE /stories/categories/{id}/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم حذف القسم 🗑️" }
```

---

## 📖 القصص (Stories)

### 🔹 إضافة قصة
```
POST /stories/stories/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم إضافة القصة بنجاح 🎉", "data": {...} }
```

### 🔹 عرض كل القصص
```
GET /stories/stories/
```
**Permissions:** Authenticated users + admin  

### 🔹 عرض قصة واحدة
```
GET /stories/stories/{id}/
```

### 🔹 تعديل قصة
```
PUT /stories/stories/{id}/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم تحديث القصة ✅", "data": {...} }
```

### 🔹 حذف قصة
```
DELETE /stories/stories/{id}/
```
**Permissions:** Admin only  
**Response:**
```json
{ "message": "تم حذف القصة 🗑️" }
```

---

## 🎬 الحلقات (Episodes)

### 🔹 إضافة حلقة
```
POST /stories/episodes/
```
**Permissions:** Admin only  

### 🔹 عرض الحلقات حسب القصة
```
GET /stories/episodes/?story={story_id}
```
**Permissions:** Authenticated users + admin  

### 🔹 عرض حلقة واحدة
```
GET /stories/episodes/{id}/
```

### 🔹 البحث عن حلقة
```
GET /stories/episodes/?story=1&search=الحلقة الأولى
```

### 🔹 تعديل حلقة
```
PUT /stories/episodes/{id}/
```
**Permissions:** Admin only  

### 🔹 حذف حلقة
```
DELETE /stories/episodes/{id}/
```
**Permissions:** Admin only  

---

## 📊 لوحة التحكم (Dashboard)

### 🔹 إحصائيات
```
GET /dashboard/stats/
```
**Permissions:** Admin only  
**Response:**
```json
{
  "message": "تم جلب الإحصائيات بنجاح 📊",
  "data": {
    "categories_count": 3,
    "stories_count": 12,
    "banners_count": 4,
    "users_count": 50
  }
}
```

---

## 👥 المستخدمين (Users)

### 🔹 عرض كل المستخدمين + البحث
```
GET /dashboard/users/?search=ahmed
```
**Permissions:** Admin only  

### 🔹 عرض مستخدم واحد
```
GET /dashboard/users/{id}/
```

### 🔹 تحديث (مثلاً حظر مستخدم)
```
PUT /dashboard/users/{id}/update_user/
```
**Permissions:** Admin only  
**Body:**
```json
{ "is_banned": true }
```
**Response:**
```json
{ "message": "تم تحديث حالة المستخدم ✅", "user": {...} }