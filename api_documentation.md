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

 
 

## 📌 Endpoints Profile 


## 🧾 Headers المشتركة

كل الطلبات لازم تحتوي على:

```
Content-Type: application/json
Authorization: Token <USER_TOKEN>
```

### 1) Get Profile (عرض البروفايل)



**Endpoint:**

```
GET /profile/
```

**Response (200 OK):**

```json
{
  "email": "user@example.com",
  "full_name": "User Name",
  "phone": "+201001234567",
  "profile_image": "https://islamicstories.pythonanywhere.com/media/users/avatar.png"
}
```

---

### 2) Update Profile (تعديل البروفايل)

**Endpoint:**

```
PUT /profile/
```

أو

```
PATCH /profile/
```

> 🔹 `PUT` → لازم تبعت كل الحقول (تحديث كامل).
> 🔹 `PATCH` → تبعت بس الحقول اللي عايز تعدلها (تحديث جزئي).

**Request Body (مثال):**

```json
{
  "email": "newemail@example.com",
  "full_name": "New Name",
  "phone": "+201112223344",
  "password": "newpassword123"
}
```

**Response (200 OK):**

```json
{
  "message": "Profile updated",
  "user": {
    "email": "newemail@example.com",
    "full_name": "New Name",
    "phone": "+201112223344",
    "profile_image": "https://islamicstories.pythonanywhere.com/media/users/avatar.png"
  }
}
```

---

### 3) Update Profile Image (لو بترفع صورة)

لو Flutter هيبعت صورة Multipart:

**Endpoint:**

```
PATCH /profile/
```

**Headers:**

```
Authorization: Token <USER_TOKEN>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**

```
profile_image: <IMAGE_FILE>
```

**Response (200 OK):**

```json
{
  "message": "Profile updated",
  "user": {
    "email": "user@example.com",
    "full_name": "User Name",
    "phone": "+201001234567",
    "profile_image": "https://islamicstories.pythonanywhere.com/media/users/new_avatar.png"
  }
}
```

---

### ⚠️ Errors

* لو التوكن مش صالح أو مش موجود:

```json
{
  "detail": "Invalid token."
}
```

* لو في خطأ في البيانات:

```json
{
  "email": ["Enter a valid email address."]
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
```json
{
  "name": "قصص الأنبياء",
  "description": "قسم خاص بقصص الأنبياء للأطفال",
  "image": "http://example.com/media/categories/prophets.png"
}
```
**Multipart form-data**
**Response:**
```json
{ "message": "تم إضافة القسم بنجاح 🎉", "data": {...} }
```

### 🔹 عرض كل الأقسام
```
GET /stories/categories/
```
**Permissions:** Authenticated users + admin 
```json
{
  "message": "تم جلب قائمة الاقسام بنجاح ✅",
  "data": [
    {
      "id": 1,
      "name": "قصص الأنبياء",
      "description": "قسم خاص بقصص الأنبياء للأطفال",
      "image": "http://127.0.0.1:8000/media/categories/prophets.png",
      "stories_count": 5
    },
    {
      "id": 2,
      "name": "قصص الصحابة",
      "description": "قصص تربوية من حياة الصحابة",
      "image": "http://127.0.0.1:8000/media/categories/sahaba.png",
      "stories_count": 3
    }
  ]
}

```

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
```json 
{
  "title": "قصة سيدنا يوسف",
  "description": "قصة سيدنا يوسف عليه السلام للأطفال",
  "category": 1,
  "thumbnail": "http://example.com/media/stories/yusuf.png"
}
```
**Response:**
```json
{ "message": "تم إضافة القصة بنجاح 🎉", "data": {...} }
```

### 🔹 عرض كل القصص
```
GET /stories/stories/
```
``` json 
{
  "message": "تم جلب قائمة القصص بنجاح ✅",
  "data": [
    {
      "id": 1,
      "title": "قصة سيدنا يوسف",
      "description": "قصة سيدنا يوسف عليه السلام للأطفال",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/yusuf.png",
      "created_at": "2025-09-17T10:35:00Z"
    },
    {
      "id": 2,
      "title": "قصة أصحاب الكهف",
      "description": "قصة دينية للأطفال من القرآن الكريم",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/kahf.png",
      "created_at": "2025-09-17T11:20:00Z"
    }
  ]
}
```

### عرض القصص علي حسب القسم 
GET /stories/stories/?category={category_id}

``` json 
{
  "message": "تم جلب قائمة القصص بنجاح ✅",
  "data": [
    {
      "id": 1,
      "title": "قصة سيدنا يوسف",
      "description": "قصة سيدنا يوسف عليه السلام للأطفال",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/yusuf.png",
      "created_at": "2025-09-17T10:35:00Z"
    },
    {
      "id": 2,
      "title": "قصة أصحاب الكهف",
      "description": "قصة دينية للأطفال من القرآن الكريم",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/kahf.png",
      "created_at": "2025-09-17T11:20:00Z"
    }
  ]
}
```
**Permissions:** Authenticated users + admin  

### 🔹 عرض قصة واحدة
 
GET /stories/stories/{id}/

```json
{
  "message": "تم جلب القصه بنجاح ✅",
  "data": {
    "id": 1,
    "title": "قصة سيدنا يوسف",
    "description": "قصة سيدنا يوسف عليه السلام للأطفال",
    "category": 1,
    "thumbnail": "http://127.0.0.1:8000/media/stories/yusuf.png",
    "created_at": "2025-09-17T10:35:00Z",
    "views_count": 13
  }
}
```

> **ملاحظة:** عند كل طلب `GET /stories/stories/{id}/` يتم زيادة العداد `views_count` تلقائيًا.
---

### 🔹 عرض القصص الأكثر شعبية

```
GET /stories/stories/popular/
```

**Description:** إرجاع قائمة بالقصص الأكثر مشاهدة (`views_count` الأعلى).
**Permissions:** Authenticated users + admin

**Response:**

```json
{
  "message": "تم جلب القصص الأكثر شعبية ✅",
  "data": [
    {
      "id": 5,
      "title": "قصة موسى عليه السلام",
      "description": "قصة سيدنا موسى للأطفال",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/musa.png",
      "created_at": "2025-09-18T09:30:00Z",
      "views_count": 50
    },
    {
      "id": 1,
      "title": "قصة سيدنا يوسف",
      "description": "قصة سيدنا يوسف عليه السلام للأطفال",
      "category": 1,
      "thumbnail": "http://127.0.0.1:8000/media/stories/yusuf.png",
      "created_at": "2025-09-17T10:35:00Z",
      "views_count": 13
    }
  ]
}
```

---
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

## 📌 Endpoints

### 1) عرض المفضلة (Get Favorites)

**Endpoint:**

```
GET stories/favorite-stories/
```

**Response (200 OK):**

```json
{
  "favorites": [
    {
      "id": 1,
      "title": "قصة أصحاب الكهف",
      "description": "تفاصيل القصة ...",
      "image": "http://islamicstories.pythonanywhere.com/media/stories/cave.jpg",
      "category": 2,
      "created_at": "2025-09-21T20:22:14Z"
    },
    {
      "id": 5,
      "title": "قصة يوسف عليه السلام",
      "description": "تفاصيل القصة ...",
      "image": null,
      "category": 1,
      "created_at": "2025-09-20T18:10:05Z"
    }
  ]
}
```

---

### 2) إضافة قصة للمفضلة (Add Favorite)

**Endpoint:**

```
POST stories/favorite-stories/
```

**Request Body:**

```json
{
  "story_id": 1
}
```

**Response (200 OK):**

```json
{
  "message": "تم إضافة القصة إلى المفضلة ✅"
}
```

**Errors:**

* لو القصة غير موجودة:

```json
{
  "error": "القصة غير موجودة"
}
```

* لو story\_id مش مبعوت:

```json
{
  "error": "story_id is required"
}
```

---

### 3) حذف قصة من المفضلة (Remove Favorite)

**Endpoint:**

```
DELETE stories/favorite-stories/
```

**Request Body:**

```json
{
  "story_id": 1
}
```

**Response (200 OK):**

```json
{
  "message": "تم حذف القصة من المفضلة 🗑️"
}
```

**Errors:**

* لو القصة غير موجودة:

```json
{
  "error": "القصة غير موجودة"
}
```

* لو story\_id مش مبعوت:

```json
{
  "error": "story_id is required"
}
```

---

### ✅ ملاحظات للمطور (Flutter Dev Notes)

* لازم المستخدم يكون عامل **Login** ومعاه `Token`.
* الـ `story_id` هو الـ ID اللي بيرجع من API القصص (`/stories/`).
* البيانات المعادة من المفضلة هي نفس شكل بيانات القصص.

---








---

## 🎬 الحلقات (Episodes)

### 🔹 إضافة حلقة
```
POST /stories/episodes/
```
**Permissions:** Admin only  

``` json 
{
  "story": 1,
  "episode_number": 1,
  "title": "الحلقة الأولى",
  "description": "بداية القصة مع المقدمة",
  "thumbnail": "http://example.com/media/episodes/ep1.png",
  "audio_file": "http://example.com/media/episodes/ep1.mp3",
  "video_file": ""
  "youtube_url": "https://youtube.com/watch?v=xxxx",
  "duration_minutes": 15
}
```


### 🔹 عرض الحلقات حسب القصة
```
GET /stories/episodes/?story={story_id}
```

```json 
{
  "message": "تم جلب قائمة الحلقات بنجاح ✅",
  "data": [
    {
      "id": 1,
      "story": 1,
      "story_title": "قصة سيدنا يوسف",
      "episode_number": 1,
      "title": "الحلقة الأولى",
      "description": "بداية القصة مع المقدمة",
      "thumbnail": "http://127.0.0.1:8000/media/episodes/ep1.png",
      "audio_file": "http://127.0.0.1:8000/media/episodes/ep1.mp3",
      "youtube_url": "https://youtube.com/watch?v=xxxx",
      "video_url": "https://dropbox.com/s/abcd123/episode1.mp4?dl=1",
      "duration_minutes": 15,
      "created_at": "2025-09-17T10:35:00Z"
    },
    {
      "id": 2,
      "story": 1,
      "story_title": "قصة سيدنا يوسف",
      "episode_number": 2,
      "title": "الحلقة الثانية",
      "description": "تكملة الأحداث",
      "thumbnail": "http://127.0.0.1:8000/media/episodes/ep2.png",
      "audio_file": null,
      "youtube_url": null,
      "video_url": "https://dropbox.com/s/efgh456/episode2.mp4?dl=1",
      "duration_minutes": 12,
      "created_at": "2025-09-17T10:50:00Z"
    }
  ]
}
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


 