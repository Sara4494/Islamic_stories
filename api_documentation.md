# 📘 API Documentation

**Base URL:**  
```
http://localhost:8000
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

## 🧪 cURL Examples

### Register
```bash
curl -X POST http://localhost:8000/register/   -H "Content-Type: application/json"   -d '{
    "email": "user@example.com",
    "full_name": "User Test",
    "password": "123456",
    "confirm_password": "123456"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/login/   -H "Content-Type: application/json"   -d '{
    "email": "user@example.com",
    "password": "123456"
  }'
```

### Google Callback
```bash
curl -X GET "http://localhost:8000/api/auth/google/callback/?code=YOUR_GOOGLE_CODE"
```

---

## 📱 Flutter Integration

### Register
```dart
Future<Map<String, dynamic>> register(String email, String fullName, String password, String confirmPassword) async {
  final url = Uri.parse("http://localhost:8000/register/");
  final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({
      "email": email,
      "full_name": fullName,
      "password": password,
      "confirm_password": confirmPassword
    }),
  );
  return jsonDecode(response.body);
}
```

### Login
```dart
Future<String> login(String email, String password) async {
  final url = Uri.parse("http://localhost:8000/login/");
  final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"email": email, "password": password}),
  );
  final data = jsonDecode(response.body);
  return data["token"];
}
```

### Google Callback
```dart
Future<Map<String, dynamic>> googleCallback(String code) async {
  final url = Uri.parse("http://localhost:8000/api/auth/google/callback/?code=$code");
  final response = await http.get(url);
  return jsonDecode(response.body);
}
```

---

## 🧰 Notes
- خزّن التوكن في `SecureStorage` أو `SharedPreferences`.
- أرسل التوكن في الـ headers مع أي API محمي:
```dart
headers: {
  "Content-Type": "application/json",
  "Authorization": "Token $token"
}
```
