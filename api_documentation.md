# 📘 API Documentation

**Base URL:**

    http://localhost:8000

> 🔁 *قم بتعديل Base URL حسب بيئة العمل لديك (Development/Production)*

------------------------------------------------------------------------

## 🧾 Headers المشتركة

كل طلبات الـ API (ما عدا Google Callback) يجب أن تحتوي على:

    Content-Type: application/json

في حال كان المستخدم مسجّل دخولًا:

    Authorization: Token <USER_TOKEN>

------------------------------------------------------------------------

## 📌 Endpoints

### 1) تسجيل مستخدم جديد (Register)

**Endpoint:**

    POST /api/auth/register/

**الطلب (Request Body):**

``` json
{
  "email": "user@example.com",
  "full_name": "User Name",
  "password": "123456",
  "confirm_password": "123456"
}
```

**الاستجابة الناجحة (201 Created):**

``` json
{
  "email": "user@example.com",
  "full_name": "User Name",
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab"
}
```

**أخطاء محتملة:** - إذا كان الباسوردين غير متطابقين:

``` json
{
  "password": ["Passwords do not match"]
}
```

-   إذا كان الإيميل مستخدمًا من قبل:

``` json
{
  "email": ["user with this email already exists."]
}
```

------------------------------------------------------------------------

### 2) تسجيل الدخول (Login)

**Endpoint:**

    POST /api/auth/login/

**الطلب (Request Body):**

``` json
{
  "email": "user@example.com",
  "password": "123456"
}
```

**الاستجابة الناجحة (200 OK):**

``` json
{
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab"
}
```

**أخطاء محتملة (400 Bad Request):**

``` json
{
  "error": "Invalid credentials"
}
```

------------------------------------------------------------------------

### 3) تسجيل الدخول عبر Google (Google OAuth)

**Endpoint:**

    GET /api/auth/google/callback/?code=<GOOGLE_AUTH_CODE>

**شرح مبسّط:** - يقوم تطبيق الـ Flutter بفتح صفحة الموافقة على Google
ويأخذ `code` بعد موافقة المستخدم. - يتم إرسال هذا `code` إلى هذا الـ
endpoint. - السيرفر يتواصل مع Google ويستخرج بيانات المستخدم ويرجع
`token`.

**الاستجابة الناجحة (200 OK):**

``` json
{
  "token": "a3b12c0b0e2348805b6d5d0f34184f89f4d3a2ab",
  "user": {
    "email": "user@gmail.com",
    "full_name": "User Google"
  }
}
```

**أخطاء محتملة (400):** - لو مفيش code:

``` json
{
  "error": "No code provided"
}
```

-   لو حصل خطأ من Google:

``` json
{
  "error": "invalid_grant",
  "error_description": "Bad Request"
}
```

------------------------------------------------------------------------

## 🔒 التوثيق (Authentication)

-   كل API خاص يتطلب إدراج Header:

```{=html}
<!-- -->
```
    Authorization: Token <USER_TOKEN>

------------------------------------------------------------------------

## 🧪 أمثلة باستخدام cURL

### Register

``` bash
curl -X POST http://localhost:8000/api/auth/register/   -H "Content-Type: application/json"   -d '{
    "email": "user@example.com",
    "full_name": "User Test",
    "password": "123456",
    "confirm_password": "123456"
  }'
```

### Login

``` bash
curl -X POST http://localhost:8000/api/auth/login/   -H "Content-Type: application/json"   -d '{
    "email": "user@example.com",
    "password": "123456"
  }'
```

### Google Login (Callback)

``` bash
curl -X GET "http://localhost:8000/api/auth/google/callback/?code=YOUR_GOOGLE_CODE"
```

------------------------------------------------------------------------

## 📱 Flutter Integration Examples

### باستخدام حزمة `http`

**1) Register**

``` dart
import 'dart:convert';
import 'package:http/http.dart' as http;

const String baseUrl = "http://localhost:8000";

Future<Map<String, dynamic>> register(String email, String fullName, String password, String confirmPassword) async {
  final url = Uri.parse("$baseUrl/api/auth/register/");
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

  final data = jsonDecode(response.body);
  if (response.statusCode == 201 || response.statusCode == 200) {
    return data; // يحتوي على token وبيانات المستخدم
  } else {
    throw Exception(data);
  }
}
```

**2) Login**

``` dart
Future<String> login(String email, String password) async {
  final url = Uri.parse("$baseUrl/api/auth/login/");
  final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"email": email, "password": password}),
  );

  final data = jsonDecode(response.body);
  if (response.statusCode == 200) {
    return data["token"];
  } else {
    throw Exception(data["error"] ?? "Login failed");
  }
}
```

**3) Google Login (Callback)** \> تقوم أولًا بفتح متصفح خارجي للحصول على
`code` من Google، ثم:

``` dart
Future<Map<String, dynamic>> googleCallback(String code) async {
  final url = Uri.parse("$baseUrl/api/auth/google/callback/?code=$code");

  final response = await http.get(url);
  final data = jsonDecode(response.body);

  if (response.statusCode == 200) {
    return data;  // { token: "...", user: {...} }
  } else {
    throw Exception(data);
  }
}
```

------------------------------------------------------------------------

## 🧰 ملاحظات مهمة للمطور

-   **تخزين التوكن:**\
    استخدم `SharedPreferences` أو `SecureStorage` لتخزين التوكن بعد
    تسجيل الدخول.

-   **إرسال التوكن مع الطلبات المحمية:**\
    أضف Header:

    ``` dart
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Token $token"
    }
    ```

-   **الإيميل فريد:**\
    لا يمكن تسجيل نفس الإيميل مرتين.

-   **التأكد من Google Client ID/Secret:**\
    تأكد أن إعدادات Google OAuth صحيحة في `settings.py`:

    ``` python
    GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
    GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
    ```
