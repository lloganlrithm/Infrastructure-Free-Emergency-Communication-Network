# 📘 Infrastructure-Free Communication System
##  รายงานสถาปัตยกรรมและการจำลองระบบ
- Youtube: NotebookLM 
https://youtu.be/1PTrfmPo8hk

-**MVP** -- Info graphic & Video
https://drive.google.com/drive/folders/1oPPGz_XRjRqeQvhdGwUutLZihlrJ2cre?usp=sharing
---

## 📑 Table of Contents
- [1. System Overview](#1-system-overview)
- [2. Code Architecture](#2-code-architecture)
- [3. System Model (4 Layers)](#3-system-model-4-layers)
- [4. Mesh Communication Model](#4-mesh-communication-model)
- [5. Dashboard & Visualization](#5-dashboard--visualization)
- [6. Installation & Usage](#6-installation--usage)
- [7. Metrics Summary](#7-metrics-summary)

---

## 1. System Overview

Adaptive Emergency Mesh Network เป็นระบบสื่อสารฉุกเฉินแบบ **Decentralized Mesh Network**  
ที่สามารถทำงานได้โดยไม่ต้องพึ่งพา:

- Internet  
- Cellular Network  
- Central Server  

ทุกอุปกรณ์ในระบบทำหน้าที่เป็น:

- Sender  
- Receiver  
- Relay Node  

### 🔑 Key Concepts
- Multi-hop Communication  
- Self-healing Network  
- Offline-first Design  
- Delay-tolerant Messaging  

---

## 2. Code Architecture

ระบบแบ่งออกเป็น 3 ส่วนหลัก:

### 🔹 Frontend
- `index.html`
- `demooo.html`
- `style.css`

หน้าที่:
- แสดง Dashboard  
- รับ input ผู้ใช้  
- แสดงข้อความ  

---

### 🔹 Backend
- `server.py`

หน้าที่:
- REST API (`/send`, `/messages`)  
- ประมวลผล message  
- เชื่อมกับ mesh simulation  

---

### 🔹 Core Simulation
- `mesh_simulator.py`

หน้าที่:
- จำลอง Mesh Network  
- Routing Message  
- Duplicate Detection  
- Node Management  

---

## 3. System Model (4 Layers)

ระบบสามารถอธิบายเป็น 4 Layer:

### Layer 1: Device Connectivity
- Peer Discovery  
- Node Connection  

### Layer 2: Routing Layer
- Multi-hop Routing  
- Flooding Algorithm  

### Layer 3: Data Layer
- Message Cache  
- Duplicate Detection  

### Layer 4: Application Layer
- User Interface  
- SOS System  
- Messaging  

---

## 4. Mesh Communication Model

### 🔁 Message Flow

1. Create message  
2. Assign Message ID  
3. Broadcast to neighbors  
4. Check duplicate  
5. Forward to next nodes  

---

### 🔬 Routing Logic

```python
def forward_message(message):
    if is_duplicate(message):
        return

    if ttl_exceeded(message):
        return

    store(message)

    for neighbor in neighbors:
        send(message)
