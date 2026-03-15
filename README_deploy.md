# Spelling Bee Trainer — Web Version
## Deploy Guide (Render — Free)

---

## ไฟล์ทั้งหมด

```
spellingbee-web/
├── main.py                  ← FastAPI server
├── index.html               ← Frontend (ไฟล์เดียว)
├── requirements.txt         ← Python packages
├── words.csv
├── trap_words.csv
├── final_round_words.csv
└── README_deploy.md         ← ไฟล์นี้
```

---

## ขั้นตอน Deploy บน Render (ฟรี)

### 1. สร้าง GitHub repo

1. เปิด https://github.com → New repository
2. ชื่อ: `spellingbee` (หรืออะไรก็ได้)
3. Public หรือ Private ก็ได้
4. อัพโหลดไฟล์ทั้งหมดเข้า repo

### 2. สมัคร Render

1. เปิด https://render.com → Sign up ด้วย GitHub account
2. ฟรีทันที ไม่ต้องใส่บัตรเครดิต

### 3. Deploy

1. Render dashboard → **New** → **Web Service**
2. เลือก GitHub repo ที่สร้างไว้
3. ตั้งค่า:
   - **Name**: `spellingbee` (จะเป็นส่วนหนึ่งของ URL)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. กด **Create Web Service**
5. รอ ~2 นาที → ได้ URL เช่น `https://spellingbee.onrender.com`

### 4. แชร์ URL

ส่ง URL ให้ทุกคนได้เลย เปิดใน browser ได้ทันที ไม่ต้องติดตั้งอะไร

---

## ทดสอบบนเครื่องก่อน Deploy

```bash
# ติดตั้ง
pip install -r requirements.txt

# รัน
python main.py

# เปิด browser
http://localhost:8000
```

---

## ข้อควรรู้ (Render Free Tier)

- **Cold start**: ถ้าไม่มีคนใช้นาน 15 นาที server จะ sleep
  → ครั้งแรกที่เปิดจะช้า ~30 วิ หลังจากนั้นปกติ
- **ไม่มีค่าใช้จ่าย**: ฟรีตลอด สำหรับ traffic ปกติ
- **Profile บันทึกใน browser**: ต่างคนต่าง device — progress ไม่ข้ามกัน

---

## อัพเดท

แก้ไขไฟล์ใน GitHub → Render deploy ใหม่อัตโนมัติ
