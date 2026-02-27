# Zero-Infrastructure Emergency Network
## Sprint Plan 

---

# 1. Executive Engineering Overview

โครงการ Infrastructure-Free Emergency Communication Network เป็นระบบเครือข่าย Mesh แบบกระจายศูนย์
ที่ออกแบบเพื่อใช้ในสถานการณ์ฉุกเฉิน โดยอุปกรณ์แต่ละเครื่องสามารถทำหน้าที่เป็นทั้งผู้ส่งและผู้ส่งต่อข้อมูลแบบ Multi-hop

ระบบสามารถทำงานได้โดยไม่ต้องพึ่ง:
- เสาสัญญาณโทรศัพท์
- อินเทอร์เน็ต
- ศูนย์กลางควบคุม

เป้าหมายของ Sprint นี้คือการสร้าง Prototype ที่สามารถส่งข้อความผ่านหลายโหนดได้
และรองรับ Emergency Broadcast

| Attribute | Target Specification |
| --- | --- |
| Network Model | Decentralized Mesh Network |
| Connectivity | Bluetooth / Wi-Fi Direct |
| Multi-hop Target | ≥ 5 Nodes |
| Message Delivery | ≥ 99% |
| Latency Target | ≤ 3 seconds |
| Packet Loss | < 1% |
| Duplicate Detection | Required |
| Architecture Layers | 5 Layers |

---

# 2. System Architecture Alignment

Sprint นี้พัฒนาระบบตาม Architecture 5 Layer

| Layer | Description |
| --- | --- |
| Mobile Application Layer | ส่วนติดต่อผู้ใช้และการส่งข้อความ |
| Emergency Communication Layer | จัดการข้อความฉุกเฉินและ Priority |
| Mesh Routing Engine | ส่งต่อข้อความแบบ Multi-hop |
| Local Data Layer | จัดเก็บข้อมูลในเครื่อง |
| Device Connectivity Layer | เชื่อมต่อ Peer-to-Peer |

---

# 3. 4-Week Advanced Sprint Execution Plan

---

# Week 1 – Device Connectivity & Basic Messaging

## Objective

พัฒนา Prototype โดยเริ่มจากการเชื่อมต่ออุปกรณ์และการส่งข้อความพื้นฐาน

## Device Connectivity Layer

| Role | Responsibility |
| --- | --- |
| Architect | ออกแบบโครงสร้างการเชื่อมต่อแบบ Peer-to-Peer และกำหนด Node Model |
| Engineer | พัฒนา Peer Discovery และการเชื่อมต่อ Bluetooth หรือ Wi-Fi Direct |
| Specialist | วิเคราะห์รูปแบบข้อความที่ต้องใช้ในสถานการณ์ฉุกเฉิน |
| DevOps | เตรียม Environment สำหรับ Prototype |
| Tester/QA | ทดสอบการเชื่อมต่อ 2 อุปกรณ์ |

## Basic Messaging Module

| Role | Responsibility |
| --- | --- |
| Architect | กำหนดโครงสร้าง Message ID และ Sender ID |
| Engineer | พัฒนาระบบส่งและรับข้อความ |
| Specialist | กำหนดรูปแบบข้อความฉุกเฉิน |
| DevOps | จัดการ Version Control |
| Tester/QA | ทดสอบการส่งข้อความระหว่างอุปกรณ์ |

### Week 1 Deliverables

- Android Prototype
- Peer-to-Peer Connection Working
- Basic Messaging Working
- Local Database Created

---

# Week 2 – Mesh Routing Engine

## Objective

พัฒนา Mesh Routing Engine ให้รองรับ Multi-hop

## Mesh Routing Module

| Role | Responsibility |
| --- | --- |
| Architect | กำหนด Routing Architecture |
| Engineer | พัฒนา Forwarding Logic |
| Specialist | ตรวจสอบความเหมาะสมของข้อมูล |
| DevOps | เตรียม Integration |
| Tester/QA | ทดสอบ Multi-hop ≥ 3 nodes |

## Duplicate Detection

| Role | Responsibility |
| --- | --- |
| Architect | กำหนด Message ID Structure |
| Engineer | พัฒนา Duplicate Detection |
| Specialist | ตรวจสอบ Message Priority |
| DevOps | เตรียม Logging |
| Tester/QA | ทดสอบ Duplicate Message |

### Week 2 Deliverables

- Mesh Routing Working
- Multi-hop Communication
- Duplicate Detection Working
- Routing Test Results

---

# Week 3 – Emergency Communication Features

## Objective

พัฒนา Emergency Broadcast และ Priority System

## Emergency Communication Layer

| Role | Responsibility |
| --- | --- |
| Architect | ออกแบบ Emergency Message Structure |
| Engineer | พัฒนา Emergency Broadcast |
| Specialist | กำหนด Priority Rules |
| DevOps | เตรียม Integration |
| Tester/QA | ทดสอบ Emergency Mode |

## GPS Location Module

| Role | Responsibility |
| --- | --- |
| Architect | กำหนด Location Data Structure |
| Engineer | เชื่อมต่อ Location API |
| Specialist | ตรวจสอบความเหมาะสมของข้อมูล |
| DevOps | เตรียม Database |
| Tester/QA | ทดสอบ Location Sharing |

### Week 3 Deliverables

- Emergency Mode Working
- Broadcast Working
- GPS Location Sharing
- Emergency Test Results

---

# Week 4 – Reliability & Performance Validation

## Objective

ทดสอบระบบและเพิ่มความเสถียร

## Reliability Testing

| Role | Responsibility |
| --- | --- |
| Architect | ตรวจสอบ Architecture Consistency |
| Engineer | พัฒนา Retry Mechanism |
| Specialist | ตรวจสอบ Use Cases |
| DevOps | วิเคราะห์ Stability |
| Tester/QA | ทดสอบ Node Failure |

# Performance Validation

| Nodes | Expected Result |
| --- | --- |
| 2 | Message Delivered |
| 3 | ≤ 2 seconds |
| 5 | ≤ 3 seconds |
| 10 | Simulation Working |

---

# Definition of Done

ระบบจะถือว่าเสร็จสมบูรณ์เมื่อ:

- Architect อนุมัติ Architecture
- Engineer ทำให้ Multi-hop ทำงานได้
- Specialist ตรวจสอบ Emergency Logic
- DevOps รวมระบบสำเร็จ
- Tester ผ่านการทดสอบ
