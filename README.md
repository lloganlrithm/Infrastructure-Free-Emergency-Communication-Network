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
