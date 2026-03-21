# 📘 Infrastructure-Free Communication System
## รายงานสถาปัตยกรรมและการจำลองระบบ

### 🎥 สื่อนำเสนอโครงการ
* **YouTube:** [ดูวิดีโอนำเสนอ](https://youtu.be/1PTrfmPo8hk)
* **MVP Info Graphic & Video:** [Google Drive Folder](https://drive.google.com/drive/folders/1oPPGz_XRjRqeQvhdGwUutLZihlrJ2cre?usp=sharing)

---

# 📡 Infrastructure-Free Emergency Communication Network v1.0
**รายงานสถาปัตยกรรมและการจำลองระบบ (Architecture & Simulation Report)**

**Computer Network Project** **Built with:** Python · HTTP Server · EMTP Protocol · HTML/CSS/JS

---

## 1. ภาพรวมของระบบ (System Overview)

ระบบ **Infrastructure-Free Emergency Communication Network** จำลองเครือข่ายสื่อสารแบบกระจายศูนย์ (Mesh Network) ที่ออกแบบมาเพื่อใช้ในสถานการณ์ที่โครงสร้างพื้นฐานล่มสลาย โดยอุปกรณ์แต่ละเครื่องจะทำหน้าที่เป็นโหนด (Node) ที่ช่วยรับ-ส่งและส่งต่อข้อมูล (Relay) เพื่อให้ข้อความไปถึงเป้าหมายได้โดยไม่ต้องพึ่งพาอินเทอร์เน็ต

### การไหลของข้อมูล 5 ชั้นสถาปัตยกรรม (5-Layer Architecture)
สัญญาณและข้อความจะถูกประมวลผลผ่าน Pipeline ดังนี้:
1. **Device Connectivity Layer** → ค้นหาโหนดใกล้เคียง (Peer Discovery) ผ่าน Bluetooth/Wi-Fi
2. **Local Data Layer** → เก็บข้อมูลแบบ Offline-first ลงใน Local Database
3. **Mesh Routing Engine** → ตัดสินใจเส้นทางส่งต่อผ่านโปรโตคอล EMTP
4. **Emergency Communication Layer** → จัดลำดับความสำคัญ (Priority) และประเภทข้อความ
5. **Mobile Application Layer** → แสดงผลผ่าน Dashboard และระบบ SOS สำหรับผู้ใช้



---

## 2. สถาปัตยกรรมโค้ด (Code Architecture)

### Module A — `mesh_simulator.py` (Core Logic)
* `class EMTPMessage`: กำหนดโครงสร้าง Packet (ID, TTL, Hop Count, Priority)
* `class MeshNode`: จัดการคิวข้อความและพฤติกรรมการส่งต่อ (Forwarding Logic)
* `class MeshNetwork`: จำลอง Topology และการเชื่อมต่อระหว่างโหนด

### Module B — `server.py` (Simulation Wrapper)
* `demo_basic_routing()`: ทดสอบการส่งข้อมูลพื้นฐาน
* `demo_mesh_topology()`: จำลองเครือข่ายแบบใยแมงมุม (Complex Mesh)
* `demo_node_failure()`: ทดสอบความทนทานเมื่อโหนดล่ม (Self-Healing)

### Module C — `index.html` & `style.css` (UI Dashboard)
* จำลองหน้าจอสมาร์ทโฟนสำหรับใช้งานในพื้นที่ภัยพิบัติ
* แสดงสถานะเครือข่าย (Nodes Active) และระบบปุ่ม SOS ระดับ Critical

---

## 3. แบบจำลองทางคณิตศาสตร์และโปรโตคอล (Mathematical Modeling)

### Layer 3 — Mesh Routing (EMTP Protocol)
ใช้โมเดล **Multi-hop Forwarding with Delay-Tolerant Networking (DTN)** และ Unique Message ID เพื่อป้องกัน Loop:
* **TTL (Time-to-Live):** กำหนดอายุข้อความ (Default = 30)
* **Hop Count:** ติดตามจำนวนการส่งต่อเพื่อวิเคราะห์ประสิทธิภาพ

### Layer 4 — Priority-Based Forwarding
| Priority | Level | Action |
|:---:|:---|:---|
| 3 | **CRITICAL** | Broadcast ทันที (SOS) |
| 2 | **HIGH** | ส่งแบบเร่งด่วน (Medical) |
| 1 | **MEDIUM** | ส่งตามคิวปกติ (Supply) |
| 0 | **NORMAL** | ส่งเมื่อเครือข่ายว่าง (Status) |

---

## 4. สถานการณ์การจำลอง (Simulation Mechanics)

1. **Topology Construction:** สร้างโหนดจำลองเชื่อมต่อแบบ Static/Dynamic
2. **Message Propagation:** การส่งต่อข้อมูลแบบทอดๆ ผ่าน Neighbors
3. **Fault Tolerance:** ระบบจะพยายามหาเส้นทางสำรอง (Alternative Path) หากโหนดตัวกลางหยุดทำงาน

### 4.1 กลไกการประมวลผลข้อความ (Message Processing Flow)
1. **Duplicate Detection:** ตรวจสอบ `message_id` ป้องกันการส่งซ้ำ
2. **TTL Validation:** ตรวจสอบอายุข้อความก่อนส่งต่อ
3. **Priority Queuing:** ลำดับความสำคัญของข้อความระดับ `CRITICAL`
4. **Path Tracking:** บันทึกเส้นทางเดินของข้อความลงใน `forwarding_path`

### 4.2 การจำลองความล้มเหลว (Node Failure Simulation)
ทดสอบความสามารถ **Self-Healing** โดยการปิดโหนดระหว่างการส่ง เพื่อวัดผล `delivery_success_rate`

---

## 5. Dashboard และการแสดงผล (Visual Analytics)

* **Network Status Card:** แสดงจำนวนโหนดที่ออนไลน์ และโหนดใกล้เคียง
* **Message Feed:** แสดงรายการข้อความแยกตามระดับความสำคัญ
* **Path Trace:** แสดงผลเส้นทางการเดินทางของข้อมูล เช่น "Node_A → Node_B → You"

---

## 6. ตารางสรุป Metrics & Success Criteria

| Layer / Component | Metric (ตัวชี้วัด) | เกณฑ์ความสำเร็จ (Target) |
| :--- | :--- | :--- |
| **Network** | Delivery Success Rate | ≥ 99% |
| **Routing** | Max Hop Count | 30 Hops |
| **Performance** | Latency per Hop | < 3 Seconds |
| **Reliability** | Recovery Time | < 5 Seconds |

---

## 7. การติดตั้งและรันโปรแกรม (Setup Guide)

1. **Clone Repository:**
   ```bash
   git clone [https://github.com/your-username/emergency-mesh-network.git](https://github.com/your-username/emergency-mesh-network.git)
   cd emergency-mesh-network
---

## 8. การติดตั้งและรันโปรแกรม (Installation & Execution)

เพื่อให้ผู้ใช้งานสามารถรันระบบจำลอง (Simulator) ได้อย่างถูกต้อง ให้ปฏิบัติตามขั้นตอนดังนี้:

### 8.1 การเตรียมระบบ (Prerequisites)
* **Python 3.8 หรือสูงกว่า:** ตรวจสอบโดยใช้คำสั่ง `python --version` ใน Terminal/Command Prompt
* **Web Browser:** แนะนำให้ใช้ Google Chrome หรือ Microsoft Edge เพื่อการแสดงผลที่สมบูรณ์

### 8.2 ขั้นตอนการเริ่มทำงาน (Step-by-Step Guide)
1. **เตรียมไฟล์โปรเจกต์:**
   ตรวจสอบให้แน่ใจว่าไฟล์ `server.py`, `mesh_simulator.py`, `index.html` และ `style.css` อยู่ในโฟลเดอร์เดียวกัน
2. **เปิด Terminal / Command Prompt:**
   ใช้คำสั่ง `cd` เพื่อเข้าไปยังโฟลเดอร์ที่เก็บไฟล์โปรเจกต์
3. **รันเซิร์ฟเวอร์จำลอง (Simulator Server):**
   ใช้คำสั่งต่อไปนี้เพื่อเริ่มระบบ:
   ```bash
   python server.py
   (หากระบบแจ้งว่าไม่รู้จักคำสั่ง python ให้ลองใช้ python3 server.py แทน)
4. **เข้าใช้งาน Dashboard:**
   เมื่อ Terminal ขึ้นข้อความ Server started, ให้เปิด Browser และไปที่:
   http://localhost:8080

### 8.3 กรณีที่พบปัญหา (Troubleshooting)
   Error: Port 8080 is already in use: เกิดจากมีโปรแกรมอื่นใช้ Port นี้อยู่ ให้ปิดโปรแกรมนั้น หรือรีสตาร์ทเครื่อง

   หน้าเว็บขาว/โหลดไม่ขึ้น: ตรวจสอบว่าในโฟลเดอร์มีไฟล์ index.html หรือไม่ และตรวจสอบว่าชื่อไฟล์ตรงกับที่เรียกใน server.py

   ส่งข้อความแล้วไม่ไป: ตรวจสอบใน Terminal ว่ามี Error log สีแดงขึ้นหรือไม่ (ส่วนใหญ่เกิดจากไฟล์ mesh_simulator.py ไม่อยู่ในโฟลเดอร์เดียวกัน)

   ---

## 9. แผนการดำเนินงาน (Timeline Overview)

โครงการนี้ใช้รูปแบบการพัฒนาแบบ **Phase-Based Iterative Development** โดยมีระยะเวลาดำเนินการรวมทั้งสิ้น 5 เดือน ดังนี้:

* **Phase 1: Core Mesh Prototype (1 เดือน)** – พัฒนาระบบเชื่อมต่อ P2P พื้นฐานและการรับ-ส่งข้อความเบื้องต้น
* **Phase 2: Mesh Routing Engine (1 เดือน)** – พัฒนาโปรโตคอล EMTP และระบบ Multi-hop Forwarding
* **Phase 3: Emergency Communication (1 เดือน)** – ระบบจัดการลำดับความสำคัญ (Priority) และการส่งพิกัด GPS
* **Phase 4: Optimization & Security (1 เดือน)** – ปรับปรุงการใช้พลังงาน (Low-power) และการเข้ารหัสข้อมูลเบื้องต้น
* **Phase 5: Field Testing & Finalization (1 เดือน)** – ทดสอบในสภาวะจำลอง (Failure Simulation) และจัดทำสรุปโครงการ

---

## 10. การจัดการความเสี่ยง (Risk Management)

| ความเสี่ยง | แนวทางป้องกันและแก้ไข |
| :--- | :--- |
| **การเชื่อมต่อไม่เสถียร** | ใช้ระบบ Retry และ Acknowledgement ในระดับโปรโตคอล |
| **ข้อความซ้ำซ้อน (Duplicate)** | ใช้ Unique Message ID และ Duplicate Detection เพื่อป้องกัน Loop |
| **แบตเตอรี่อุปกรณ์หมดเร็ว** | ปรับปรุงระบบให้ทำงานแบบ Low-power Background Service |
| **ความเป็นส่วนตัวของข้อมูล** | นำระบบเข้ารหัสข้อมูลเบื้องต้นมาใช้ก่อนการ Broadcast |

---

## 11. ตัวชี้วัดความสำเร็จ (Success Metrics - KPIs)

จากการทดสอบผ่านระบบจำลอง (Simulator) ระบบมีประสิทธิภาพเป็นไปตามเกณฑ์ดังนี้:

* **Delivery Success Rate:** อัตราการส่งข้อความสำเร็จระหว่างอุปกรณ์ $\ge 99\%$
* **Scalability:** รองรับการส่งต่อข้อมูล (Hop) อย่างน้อย 5 โหนด
* **Performance:** เวลาเฉลี่ยในการส่งข้อมูล (Latency) $\le 3$ วินาที
* **Reliability:** อัตราการสูญหายของข้อความ (Message Loss) $< 1\%$

---

## 12. สมาชิกผู้จัดทำ (Project Team)

| ลำดับ | รายชื่อสมาชิก | รหัสนักศึกษา | บทบาทหน้าที่ |
| :---: | :--- | :---: | :--- |
| 1 | นางสาวกมลพร เกตุแก้ว | 673380571-1 | System Architecture & UI Design |
| 2 | นางสาวพรีมภัทร ภาวัฒนวคุณ | 673380594-9 | Network Simulation Logic |
| 3 | นางสาวพิชยา สิทธิพันธ์ | 673380596-5 | EMTP Protocol Design |
| 4 | นางสาวมุกดา บุญประจันทร์ | 673380598-1 | Backend Server & Integration |
| 5 | นางสาวสรนันท์ บุสดี | 673380605-0 | Testing & Data Analysis |

---

**Infrastructure-Free Emergency Communication Network** *Computer Network Project · Faculty of Engineering · 2024*
