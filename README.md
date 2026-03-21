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

### 4.1 กลไกการประมวลผลข้อความ (Message Processing Flow)
เมื่อโหนดได้รับข้อความ (Packet) จะมีการประมวลผลตามอัลกอริทึมดังนี้:
1.  **Duplicate Detection:** ตรวจสอบ `message_id` ใน `processed_messages` (Set) หากซ้ำจะทำการ Drop ทันที
2.  **TTL Validation:** ตรวจสอบค่า `ttl` หากค่าเป็น 0 จะไม่ส่งต่อ
3.  **Priority Queuing:** ข้อความระดับ `CRITICAL` จะถูกแทรกคิวเพื่อส่งออก (Forward) เป็นลำดับแรก
4.  **Path Tracking:** บันทึกชื่อโหนดลงใน `forwarding_path` เพื่อใช้ในการ Trace เส้นทางกลับ

### 4.2 การจำลองความล้มเหลว (Node Failure Simulation)
ใน `demo_node_failure()` ระบบจะทำการ `disconnect_nodes` หรือตั้งค่าโหนดให้ `Inactive` ระหว่างการส่งข้อมูล:
* **Self-Healing Test:** ระบบจะพยายามส่งข้อความผ่านทางเลือกอื่น (เช่น จากเดิม You → A → B เปลี่ยนเป็น You → C → D)
* **Metrics:** วัดผลจาก `delivery_success_rate` และ `average_hop_count` ที่เพิ่มขึ้นจากการอ้อมโหนดที่ล่ม

---

## 5. ทฤษฎีการจัดการคิวและเครือข่าย (Queue & Network Theory)

### M/M/1 Queue Analogy
ในระบบจำลองนี้ แต่ละโหนดทำงานเสมือนเป็นระบบคิวเดี่ยว (Single Server Queue):
* **Arrival Rate ($\lambda$):** อัตราการรับข้อความจากโหนดรอบข้าง
* **Service Rate ($\mu$):** ความเร็วในการประมวลผลและส่งต่อข้อมูลผ่านโปรโตคอล EMTP
* **Priority Scheduling:** ระบบใช้ **Non-preemptive Priority Queue** เพื่อจัดการข้อความ SOS ให้มีความหน่วงต่ำที่สุด

---

## 6. Dashboard และการแสดงผล (Visual Analytics)

### ส่วนแสดงผล Real-Time (Web Interface)
หน้าจอ Dashboard ใน `index.html` ถูกออกแบบมาเพื่อจำลองประสบการณ์ผู้ใช้จริง:
* **Network Status Card:** แสดงจำนวนโหนดที่ออนไลน์อยู่ (Nodes Active) และโหนดใกล้เคียง (Local Peers)
* **Message Feed:** แสดงรายการข้อความพร้อมแถบสีระบุความเร่งด่วน (แดง = Critical, ส้ม = High)
* **Path Trace:** แสดงผล "Node_A → Node_B → You" เพื่อให้ผู้ใช้ทราบว่าข้อความเดินทางผ่านใครมาบ้าง

---

## 7. ตารางสรุป Metrics & Success Criteria

| Layer / Component | Metric (ตัวชี้วัด) | เกณฑ์ความสำเร็จ (Target) | คำอธิบาย |
| :--- | :--- | :--- | :--- |
| **Network** | Delivery Success Rate | ≥ 99% | อัตราความสำเร็จในการส่งข้อความ |
| **Routing** | Max Hop Count | 30 Hops | ขอบเขตการกระจายข้อมูล (TTL) |
| **Performance** | Latency per Hop | < 3 Seconds | ความเร็วในการ Relay ข้อมูล |
| **Reliability** | Recovery Time | < 5 Seconds | เวลาที่ใช้หาเส้นทางใหม่เมื่อโหนดล่ม |

---

## 8. การติดตั้งและรันโปรแกรม (Setup Guide)

### สิ่งที่ต้องการ (Prerequisites)
* Python 3.8 หรือเวอร์ชันที่สูงกว่า
* Web Browser (Chrome, Firefox, Safari)

### ขั้นตอนการเริ่มใช้งาน
1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/your-username/emergency-mesh-network.git](https://github.com/your-username/emergency-mesh-network.git)
    cd emergency-mesh-network
    ```
2.  **Start Simulator & Server:**
    ```bash
    python server.py
    ```
3.  **Access Dashboard:**
    เปิด Browser ไปที่ `http://localhost:8080`

---

## 9. สมาชิกผู้จัดทำ (Project Team)

| รายชื่อสมาชิก | รหัสนักศึกษา | บทบาทหน้าที่ |
| :--- | :--- | :--- |
| นางสาวกมลพร เกตุแก้ว | 673380571-1 | System Architecture & UI |
| นางสาวพรีมภัทร ภาวัฒนวคุณ | 673380594-9 | Network Simulation Logic |
| นางสาวพิชยา สิทธิพันธ์ | 673380596-5 | EMTP Protocol Design |
| นางสาวมุกดา บุญประจันทร์ | 673380598-1 | Backend Server & Integration |
| นางสาวสรนันท์ บุสดี | 673380605-0 | Testing & Data Analysis |

---
**Infrastructure-Free Emergency Communication Network**
*Computer Network Project - 2024*
   ```bash
   python server.py
