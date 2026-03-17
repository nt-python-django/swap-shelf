# 📚 SwapShelf

**SwapShelf** — bu **peer-to-peer book exchange platform** bo‘lib, foydalanuvchilar o‘z kitoblarini boshqalar bilan **vaqtincha (borrow)** yoki **doimiy (permanent)** almashishlari mumkin.

Platforma ikki interfeysdan iborat:

1. **Web Application** — asosiy funksiyalar (kitob qo‘shish, browse, request yuborish, swap boshqarish)
2. **Telegram Bot** — authentication, notifications va quick actions

Bundan tashqari, yangi qo‘shilgan kitoblar **Telegram kanalga avtomatik publish qilinadi**.

---

# 🧩 System Overview

Platforma **REST API backend** asosida qurilgan.

```
                ┌─────────────────────┐
                │     Web Client      │
                │ (React / Next.js)   │
                └──────────┬──────────┘
                           │
                           │ REST API
                           │
                    ┌──────▼──────┐
                    │   Django     │
                    │   Backend    │
                    │ (DRF API)    │
                    └──────┬──────┘
                           │
           ┌───────────────┼────────────────┐
           │               │                │
     PostgreSQL       Telegram Bot     Telegram Channel
        Database     (python-telegram)     (Publish)
```

---

# ✨ Core Features

### 📚 Book Shelf

Foydalanuvchilar:

* o‘z kitoblarini **shelf** ga qo‘shishadi
* kitob haqida ma'lumot kiritishadi
* rasm yuklashadi
* share qilinsa **telegram kanalga post qilinadi**

---

### 🔎 Browse Books

Foydalanuvchilar:

* janr bo‘yicha qidirish
* kitob holatini ko‘rish
* egasining reytingini ko‘rish
* swap request yuborish

---

### 🔄 Swap System

Swap jarayoni:

```
User A → Request yuboradi
User B → Accept qiladi

→ Swap yaratiladi
→ Kitob unavailable bo‘ladi
→ Contact info yuboriladi
```

Borrow swap uchun:

```
Return → Owner confirm
→ Swap closed
→ Review qoldiriladi
```

---

### ⭐ Review & Reputation

Har bir tugagan swapdan so‘ng:

* ikkala tomon **1–5 rating**
* **review comment**

User rating:

```
rating = avg(all_reviews)
```

Bu rating browse sahifasida ko‘rinadi.

---

# 🔐 Authentication Flow

Authentication **Telegram asosida** ishlaydi.

### Registration

```
User → Telegram Bot

/start
  ↓
Phone number
  ↓
User created
```

---

### Login (Telegram bot)

```
User → Telegram Bot
Enter /login command
  ↓
OTP sent via Telegram bot
  ↓
OTP verify by website
  ↓
JWT token issued
```

Texnologiya:

* **DRF Simple JWT**
* Telegram orqali **OTP delivery**

---

# 🤖 Telegram Bot Responsibilities

Bot **core logic uchun emas**, balki **integration layer** sifatida ishlaydi.

### Bot funksiyalari

| Feature        | Description                      |
| -------------- | -------------------------------- |
| Registration   | User ro'yxatdan o'tadi           |
| OTP login      | Website login uchun OTP          |
| Notifications  | Request / swap updates           |
| Quick requests | Telegram orqali request yuborish |
| Contact share  | Swap boshlanganda                |

---

### Notifications

Bot orqali yuboriladigan xabarlar:

* 📩 New swap request
* ✅ Request accepted
* ❌ Request rejected
* 📦 Return confirmation
* ⭐ Review reminder

---

# 📢 Telegram Channel Integration

Agar user **kitobni share qilsa**, quyidagi jarayon ishlaydi:

```
User adds book
     ↓
share=True
     ↓
Backend → Telegram Bot API
     ↓
Book post published
     ↓
Channel subscribers see it
```

Post tarkibi:

```
📚 Book Title
✍ Author
📖 Genre
⭐ Owner rating

Condition: Good
Type: Borrow

Description...

🔗 Request via website
```

---

# 🏗 Tech Stack

| Layer         | Technology            |
| ------------- | --------------------- |
| Backend       | Django                |
| API           | Django REST Framework |
| Auth          | DRF Simple JWT        |
| Bot           | python-telegram-bot   |
| Database      | PostgreSQL            |
| Config        | django-environ        |
| Media storage | Local / S3 compatible |

---

# 📂 Project Structure

```
swapshelf/
│
├── apps/
│   ├── users/
│   ├── bot/
│   │   ├── handlers/
│   │   ├── services/
│   │   └── bot.py
│   ├── books/
│   ├── swaps/
│   ├── reviews/
│   └── notifications/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   └── asgi.py
│
├── scripts/
│
├── manage.py
└── requirements.txt
```

---

# 🗄 Database Schema

Relationship overview:

```
users
  │
  ├── books
  │
  ├── swap_requests
  │
  └── reviews

books
  └── swap_requests

swap_requests
  └── swaps

swaps
  └── reviews
```

---

## users

Telegram foydalanuvchilar.

```
id
username -> telegram_id
phone
name
rating
created_at
```

---

## genres

```
id
name
```

Seed data:

* Roman
* Fantastika
* Ilmiy
* Tarix
* Biznes

---

## books

```
id
owner_id
title
author
genre_id
condition
type
description
image
status
share
created_at
```

---

## swap_requests

```
id
book_id
requester_id
message
status
created_at
```

status:

```
pending
accepted
rejected
```

---

## swaps

```
id
book_id
owner_id
borrower_id
type
status
return_deadline
created_at
```

status:

```
active
completed
cancelled
```

---

## reviews

```
id
swap_id
reviewer_id
reviewed_user_id
rating
comment
created_at
```

---

# 🌐 REST API Overview

## Authentication

```
POST /auth/login
POST /auth/refresh
```

---

## Books

```
GET    /books
POST   /books
GET    /books/{id}
PATCH  /books/{id}
DELETE /books/{id}
```

---

## Swap Requests

```
POST /swap-requests
GET  /swap-requests
PATCH /swap-requests/{id}/accept
PATCH /swap-requests/{id}/reject
```

---

## Swaps

```
GET /swaps
POST /swaps/{id}/mark-returned
POST /swaps/{id}/confirm-return
```

---

## Reviews

```
POST /reviews
GET /users/{id}/reviews
```

---

# 🚀 Local Development Setup

## 1. Clone repository

```bash
git clone https://github.com/yourname/swapshelf.git
cd swapshelf
```

---

## 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Create database

```
CREATE DATABASE swapshelf;
```

---

## 5. Environment variables

```
cp .env.example .env
```

```
BOT_TOKEN=
CHANNEL_ID=
ADMIN_IDS=

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

## 6. Run migrations

```
python manage.py migrate
```

---

## 7. Run backend

```
python manage.py runserver
```

---

# 🧠 Future Improvements

* Recommendation system
* Geo-based book discovery
* Book reservation queue
* Anti-fraud reputation system
* Mobile app
