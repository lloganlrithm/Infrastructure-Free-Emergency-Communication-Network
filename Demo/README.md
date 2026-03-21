
# 📡 Emergency Mesh Network Simulator (EMTP)

ระบบจำลองเครือข่ายสื่อสารแบบไร้โครงสร้างพื้นฐาน (Infrastructure-free) สำหรับสถานการณ์ฉุกเฉิน พัฒนาด้วยแนวคิด **Mesh Topology** เพื่อให้การสื่อสารยังคงดำเนินต่อไปได้แม้เสาสัญญาณหลักหรืออินเทอร์เน็ตจะล่ม

## 📋 ภาพรวมโครงการ (Project Overview)

โครงการนี้ประกอบด้วยระบบจำลอง (Simulation Core) ที่เขียนด้วย Python และส่วนติดต่อผู้ใช้ (Dashboard Interface) ในรูปแบบ Web Application เพื่อแสดงให้เห็นการทำงานของ **Emergency Mesh Transfer Protocol (EMTP)** ในการส่งข้อความผ่าน Node ต่างๆ (Multi-hop Forwarding)

### คุณสมบัติเด่น (Key Features)
* **Decentralized Architecture**: ไม่มี Server กลาง ทุก Node ทำหน้าที่เป็นทั้งผู้รับและผู้ส่งต่อข้อความ
* **Multi-hop Routing**: ระบบค้นหาเส้นทางส่งต่อข้อความอัตโนมัติ (Node A -> B -> C)
* **Duplicate Detection**: ระบบป้องกันข้อความวนซ้ำในเครือข่ายเพื่อประหยัดทรัพยากร
* **Priority System**: การแบ่งลำดับความสำคัญของข้อความ (Normal, Medium, High, Critical)
* **Self-Healing**: เครือข่ายสามารถหาเส้นทางใหม่ได้ทันทีหากมี Node ใด Node หนึ่งออกจากระบบ (Node Failure)

---

## 🏗️ โครงสร้างทางเทคนิค (Technical Architecture)

### 1. Backend: Mesh Core (Python)
* **`mesh_simulator.py`**: หัวใจหลักของระบบ ประกอบด้วย Class `MeshNode` และ `MeshNetwork` ที่จัดการ Logic การรับ-ส่งข้อความ, การตรวจสอบ TTL (Time To Live), และการจัดการ Neighbor Table
* **`server.py`**: ทำหน้าที่เป็น API Server ขนาดเล็ก (Base HTTP Server) เพื่อเชื่อมโยงโลกของ Python Simulation เข้ากับหน้าเว็บ

### 2. Frontend: Dashboard (HTML/CSS/JS)
* **`index.html`**: หน้าจอจำลองสมาร์ทโฟนสำหรับผู้ใช้งานในพื้นที่ภัยพิบัติ
* **`app.js`**: จัดการการเรียก API และการอัปเดตสถานะเครือข่ายแบบ Real-time
* **`style.css`**: ออกแบบ UI ให้เหมาะสมกับการใช้งานฉุกเฉิน (High Contrast, Large Buttons)

---

## 🚀 การติดตั้งและเริ่มใช้งาน (Getting Started)

1. **เตรียมความพร้อม**: ตรวจสอบว่าในเครื่องมี Python 3.x ติดตั้งอยู่
2. **ดาวน์โหลดไฟล์**: คัดลอกไฟล์ทั้งหมดลงในโฟลเดอร์เดียวกัน
3. **รันระบบจำลอง**:
   ```bash
   python3 server.py```
4. **เข้าใช้งาน:** เปิด Web Browser แล้วไปที่่ ```http://localhost:8081```
