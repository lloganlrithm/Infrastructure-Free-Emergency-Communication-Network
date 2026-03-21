# Infrastructure-Free Communication System for Disaster Recovery
 
 
---
## 🛠 โครงสร้างระบบ (System Architecture)

ระบบประกอบด้วยส่วนงานหลัก 3 ส่วน:

1.  **Core Simulator (`mesh_simulator.py`):** * จัดการ Logic ของเครือข่ายทั้งหมด
    * กำหนดโปรโตคอล **EMTP (Emergency Mesh Transfer Protocol)**
    * จัดการระบบ Priority, TTL (Time to Live) และการป้องกันข้อความซ้ำ (Duplicate Detection)
2.  **Web Backend (`server.py`):**
    * สร้าง HTTP Server บน Port 8081
    * ทำหน้าที่เป็นตัวกลางเชื่อมต่อ UI เข้ากับ Mesh Simulator
3.  **Frontend Dashboard (`index.html`, `style.css`, `app.js`):**
    * UI จำลองหน้าจอสมาร์ทโฟนสำหรับผู้ใช้งาน
    * แสดงสถานะเครือข่าย จำนวนโหนดที่เชื่อมต่อ และกล่องข้อความ

---

## ✨ คุณสมบัติทางเทคนิค (Technical Features)

### 📡 1. Mesh Routing & Self-Healing
* **Multi-hop Propagation:** ข้อความสามารถเดินทางผ่านหลายโหนดเพื่อไปถึงปลายทาง
* **Path Tracking:** ระบบจะบันทึกเส้นทางที่ข้อความวิ่งผ่าน (เช่น `Node_A → Node_B → You`)
* **Fault Tolerance:** หากโหนดใดโหนดหนึ่งล่ม ระบบจะพยายามหาเส้นทางใหม่เพื่อส่งข้อความให้ถึงเป้าหมาย

### ⚠️ 2. Emergency Services
* **SOS Broadcast:** การส่งข้อความแบบกระจายเสียงไปยังทุกโหนดในเครือข่ายพร้อมระบุพิกัด GPS
* **Priority Levels:** รองรับการแบ่งระดับความรุนแรงของเหตุการณ์ (Normal, Medium, High, Critical)

### 🛡️ 3. Network Stability
* **Duplicate Drop:** ป้องกันการส่งข้อความซ้ำซ้อนในเครือข่ายเพื่อประหยัดแบนด์วิธ
* **TTL Control:** มีการจำกัดจำนวน Hop เพื่อป้องกันข้อมูลค้างในระบบนานเกินไป

---

## 📊 ข้อมูลจำลองในระบบ (Simulation Data)

| ข้อมูล | รายละเอียด |
| :--- | :--- |
| **Nodes** | Node_You, Node_A, Node_B, Node_C, Node_D, Node_E |
| **Protocol** | EMTP (Emergency Mesh Transfer Protocol) |
| **Port** | 8081 |
| **Priority** | 4 ระดับ (Normal - Critical) |

---

## 🚀 การติดตั้งและใช้งาน (Installation)

1. **ดาวน์โหลดไฟล์โครงการ** และตรวจสอบว่ามี Python 3 ติดตั้งอยู่ในเครื่อง
2. **รันเซิร์ฟเวอร์หลัก:**
   ```bash
   python server.py```
