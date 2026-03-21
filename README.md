# 📘 Infrastructure-Free Communication System
##  รายงานสถาปัตยกรรมและการจำลองระบบ
- Youtube
https://youtu.be/1PTrfmPo8hk

**MVP**  Info graphic & Video
- https://drive.google.com/drive/folders/1oPPGz_XRjRqeQvhdGwUutLZihlrJ2cre?usp=sharing
---
# 📡 Infrastructure-Free Emergency Communication Network v1.0
**รายงานสถาปัตยกรรมและการจำลองระบบ (Architecture & Simulation Report)**

**Computer Network Project** **Built with:** Python · HTTP Server · EMTP Protocol · HTML/CSS/JS

---

## 1. ภาพรวมของระบบ (System Overview)

ระบบ **Infrastructure-Free Emergency Communication Network** จำลองเครือข่ายสื่อสารแบบกระจายศูนย์ (Mesh Network) ที่ออกแบบมาเพื่อใช้ในสถานการณ์ที่โครงสร้างพื้นฐานล่มสลาย โดยอุปกรณ์แต่ละเครื่องจะทำหน้าที่เป็นโหนด (Node) ที่ช่วยรับ-ส่งและส่งต่อข้อมูล (Relay) เพื่อให้ข้อความไปถึงเป้าหมายได้โดยไม่ต้องพึ่งพาอินเทอร์เน็ต

### การไหลของข้อมูล 5 ชั้นสถาปัตยกรรม (5-Layer Architecture)
สัญญาณและข้อความจะถูกประมวลผลผ่าน Pipeline ดังนี้:

1.  **Device Connectivity Layer** → ค้นหาโหนดใกล้เคียง (Peer Discovery) ผ่าน Bluetooth/Wi-Fi
2.  **Local Data Layer** → เก็บข้อมูลแบบ Offline-first ลงใน Local Database
3.  **Mesh Routing Engine** → ตัดสินใจเส้นทางส่งต่อผ่านโปรโตคอล EMTP
4.  **Emergency Communication Layer** → จัดลำดับความสำคัญ (Priority) และประเภทข้อความ
5.  **Mobile Application Layer** → แสดงผลผ่าน Dashboard และระบบ SOS สำหรับผู้ใช้

---

## 2. สถาปัตยกรรมโค้ด (Code Architecture)

โปรแกรมแบ่งออกเป็น **3 Modules** หลักตามโครงสร้างการทำงาน:

### Module A — `mesh_simulator.py` (Core Logic)
หัวใจหลักของการคำนวณเครือข่าย ประกอบด้วย Class สำคัญ:
* `class EMTPMessage`: กำหนดโครงสร้าง Packet (ID, TTL, Hop Count, Priority)
* `class MeshNode`: จัดการคิวข้อความและพฤติกรรมการส่งต่อ (Forwarding Logic)
* `class MeshNetwork`: จำลอง Topology และการเชื่อมต่อระหว่างโหนด

### Module B — `server.py` (Simulation Wrapper)
ทำหน้าที่เป็น Backend จำลองสถานการณ์เครือข่าย (Network Scenarios):
* `demo_basic_routing()`: ทดสอบการส่งข้อมูลพื้นฐาน
* `demo_mesh_topology()`: จำลองเครือข่ายแบบใยแมงมุม (Complex Mesh)
* `demo_node_failure()`: ทดสอบความทนทานเมื่อโหนดล่ม (Self-Healing)

### Module C — `index.html` & `style.css` (UI Dashboard)
* จำลองหน้าจอสมาร์ทโฟนสำหรับใช้งานในพื้นที่ภัยพิบัติ
* แสดงสถานะเครือข่าย (Nodes Active) และประวัติการรับ-ส่งข้อความ
* ระบบปุ่ม SOS สำหรับกระจายข้อความฉุกเฉินระดับ Critical

---

## 3. แบบจำลองทางคณิตศาสตร์และโปรโตคอล (Mathematical Modeling)

### Layer 3 — Mesh Routing (EMTP Protocol)
โมเดล: **Multi-hop Forwarding with Delay-Tolerant Networking (DTN)**
ใช้ Unique Message ID เพื่อป้องกัน Loop และ Duplicate Packets:
* **TTL (Time-to-Live):** กำหนดอายุข้อความ (Default = 30) เพื่อป้องกัน Network Congestion
* **Hop Count:** ติดตามจำนวนการส่งต่อเพื่อวิเคราะห์ประสิทธิภาพเส้นทาง

### Layer 4 — Priority-Based Forwarding
ระบบจัดลำดับความสำคัญของข้อความตามโมเดล Urgency:

| Priority | Level | Payload Type | Action |
|:---:|:---|:---|:---|
| 3 | **CRITICAL** | SOS / Emergency | Broadcast ทันที (Highest Priority) |
| 2 | **HIGH** | Injured / Medical | ส่งแบบเร่งด่วน (Urgent Queue) |
| 1 | **MEDIUM** | Supply / Food | ส่งตามคิวปกติ |
| 0 | **NORMAL** | Status Update | ส่งเมื่อเครือข่ายว่าง (Low Priority) |

---

## 4. สถานการณ์การจำลอง (Simulation Mechanics)

ระบบใช้ **Event-Driven Simulation** ในการทดสอบประสิทธิภาพเครือข่าย:

1.  **Topology Construction:** สร้างโหนดจำลอง (Node_You, Node_A, Node_B... Node_E) และเชื่อมต่อแบบ Static/Dynamic
2.  **Message Propagation:** เมื่อส่งข้อความจาก `Node_You` ระบบจะค้นหาเพื่อนบ้าน (Neighbors) และส่งต่อข้อมูลเป็นทอดๆ
3.  **Fault Tolerance:** หากโหนดตัวกลาง (เช่น Node_B) หยุดทำงาน ระบบจะพยายามหาเส้นทางสำรอง (Alternative Path) ผ่านโหนดอื่นโดยอัตโนมัติ

---

## 5. การติดตั้งและรันโปรแกรม (Installation)

1. **ติดตั้ง Python 3.x** ในเครื่องของคุณ
2. **รันเซิร์ฟเวอร์จำลอง:**
   ```bash
   python server.py
