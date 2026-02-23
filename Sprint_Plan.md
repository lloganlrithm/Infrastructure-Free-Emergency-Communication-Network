# Zero-Infrastructure Emergency Network
## Sprint Plan
# 1. Executive Engineering Overview

โครงการนี้มีเป้าหมายในการพัฒนาเครือข่ายสื่อสารฉุกเฉินแบบกระจายศูนย์
(Fully Decentralized Mesh Network)
ที่สามารถทำงานได้โดยไม่พึ่งพาโครงสร้างพื้นฐาน เช่น
เสาสัญญาณโทรศัพท์หรืออินเทอร์เน็ต ระบบต้องสามารถส่งข้อความแบบ Multi-hop
ผ่านหลายโหนด
และมีความสามารถในการฟื้นตัวเมื่อเกิดความล้มเหลวของโหนดบางส่วน

| Attribute | Target Specification |
| --- | --- |
| Network Model | Fully Decentralized Mesh |
| Protocol | Emergency Mesh Transfer Protocol (EMTP) v1.0 |
| Routing Strategy | Controlled Flooding with TTL |
| Multi-hop Target | ≥ 5 Nodes (Live Demo) |
| Simulation Target | ≥ 10 Nodes |
| Avg Latency (5 hops) | ≤ 3 seconds |
| Packet Delivery Rate | ≥ 99% |
| Packet Loss | < 1% |
| Recovery Time (Node Failure) | ≤ 2 seconds |
| Duplicate Rate | 0% |

---
# 2. Emergency Mesh Transfer Protocol (EMTP) v1.0

โปรโตคอล EMTP ถูกออกแบบมาเพื่อรองรับการส่งข้อความฉุกเฉินในเครือข่าย Mesh
โดยเน้นความเรียบง่าย ความทนทาน และความสามารถในการป้องกันการส่งซ้ำ

## 2.1 Packet Structure

  | Field | Size | Description |
| --- | --- | --- |
| Version | 1B | ระบุเวอร์ชันของโปรโตคอล |
| Message ID | 16B | รหัส UUID สำหรับป้องกันข้อความซ้ำ |
| Sender ID | 8B | รหัสประจำอุปกรณ์ผู้ส่ง |
| Priority | 1B | ระดับความสำคัญ (Normal / High / Critical) |
| TTL | 1B | จำนวน hop สูงสุดที่อนุญาต |
| Hop Count | 1B | จำนวน hop ที่ข้อความผ่าน |
| Timestamp | 8B | เวลาที่สร้างข้อความ |
| Checksum | 4B | ตรวจสอบความถูกต้องของข้อมูล |
| Payload | Variable | เนื้อหาข้อความฉุกเฉิน |

## 2.2 Protocol Rules

-   TTL จะลดลงทุกครั้งที่มีการส่งต่อข้อความ\
-   หาก TTL เท่ากับ 0 จะยุติการส่งต่อทันที\
-   ใช้ Message ID เพื่อตรวจจับข้อความซ้ำ\
-   ต้องตรวจสอบ Checksum ก่อนส่งต่อ\
-   ระบบต้องรอ ACK เพื่อยืนยันการส่งสำเร็จ\
-   จำกัดการ Retry ไม่เกิน 3 ครั้ง

------------------------------------------------------------------------

# 3. 4-Week Advanced Sprint Execution Plan

------------------------------------------------------------------------

# Week 1 -- Protocol Engineering & Baseline Connectivity

## Objective

จัดทำเอกสารโปรโตคอลอย่างเป็นทางการ และทำให้การสื่อสารแบบ 1-hop
ทำงานได้อย่างเสถียร

## Device Connectivity Layer

พัฒนาโมดูลค้นหาอุปกรณ์ใกล้เคียง กำหนดรอบการสแกนทุก 5 วินาที
และตรวจจับการหลุดการเชื่อมต่อหากไม่มีสัญญาณภายใน 10 วินาที
ระบบต้องสามารถเชื่อมต่อใหม่ได้อัตโนมัติสูงสุด 3 ครั้ง
พร้อมบันทึกสถานะโหนดเพื่อใช้ในการวิเคราะห์ภายหลัง

## EMTP Core Module

พัฒนาโมดูลสำหรับเข้ารหัสและถอดรหัสแพ็กเก็ต เพิ่มกลไก TTL และตรวจสอบ
Checksum เพื่อป้องกันข้อมูลเสียหาย ใช้ LRU Cache เพื่อเก็บ Message ID
ล่าสุดจำนวน 500 รายการ และกำหนดอายุของ cache เป็น 30 วินาที

## Local Data Layer

จัดเก็บข้อความและสถานะการส่งในฐานข้อมูลภายในเครื่อง รองรับการทำงานแบบ
Offline-first
และสามารถนำข้อความที่ค้างอยู่กลับมาส่งต่อเมื่อเชื่อมต่อใหม่ได้

### Week 1 Deliverables

-   เอกสาร EMTP Specification ฉบับสมบูรณ์\
-   การส่งข้อความแบบ 1-hop สำเร็จ\
-   ตรวจสอบ Checksum ผ่านทุกกรณี\
-   ไม่มีการส่งข้อความซ้ำ

---

# Week 2 -- Multi-Hop Routing & Reliability

## Objective

พัฒนาการส่งข้อความแบบ Multi-hop ผ่านอย่างน้อย 5 โหนด พร้อมระบบ ACK และ
Retry ที่มีความเสถียร

## Mesh Routing Engine

พัฒนา Controlled Flooding โดยใช้ TTL จำกัดจำนวน hop
เพิ่มระบบกรองข้อความซ้ำ และป้องกันการเกิด loop แบบไม่มีที่สิ้นสุด
ระบบต้องสามารถติดตามจำนวน hop และบันทึกข้อมูลสำหรับวิเคราะห์ latency

## ACK & Retry Engine

กำหนด Retry Interval 500ms และจำกัดการ Retry สูงสุด 3 ครั้ง
หากเกินจำนวนที่กำหนดให้ยุติการส่งและบันทึกสถานะล้มเหลว พร้อมแสดงผลในระบบ
monitoring

## Metrics Collection Module

บันทึกข้อมูลเพื่อวิเคราะห์ประสิทธิภาพ เช่น ค่า Latency ต่อ hop,
End-to-End Latency, จำนวน Retry, Packet Drop และ Duplicate Rate
เพื่อใช้ในรายงานสรุป

### Week 2 Deliverables

-   Multi-hop ≥ 5 โหนด\
-   Packet Loss \< 1%\
-   ค่า Latency เฉลี่ย ≤ 3 วินาที\
-   ระบบ ACK และ Retry ทำงานถูกต้อง

---

# Week 3 -- Reliability Engineering & Failure Simulation

## Objective

ทดสอบความสามารถในการฟื้นตัวของเครือข่ายเมื่อเกิดความล้มเหลว
และยืนยันว่าเป็น Self-Healing Mesh จริง

## Failure Simulation

จำลองสถานการณ์ปิดโหนดแบบสุ่ม 30%
จำลองการหลุดการเชื่อมต่อระหว่างส่งข้อความ และจำลอง Network Partition
เพื่อทดสอบการทำงานในสภาพเครือข่ายขาดช่วง

## Recovery Mechanisms

พัฒนาระบบ Store-and-Forward เมื่อโหนดกลับมาออนไลน์
ระบบต้องสามารถส่งข้อความค้างอยู่ได้ทันทีโดยไม่สูญหาย และต้องไม่เกิด loop
ซ้ำ

## Stress Testing

จำลองการส่งข้อความฉุกเฉินพร้อมกัน 10 ข้อความ และจำลอง Packet Drop
10--20% เพื่อวิเคราะห์เสถียรภาพของระบบ

### Week 3 Deliverables

-   Recovery Time ≤ 2 วินาที\
-   ไม่มี Infinite Loop\
-   ระบบยังคงทำงานได้แม้บางโหนดล้มเหลว\
-   Stability ≥ 90%

---

# Week 4 -- Security Hardening & Performance Validation

## Objective

เพิ่มความปลอดภัยของข้อมูล วิเคราะห์พลังงาน
และจัดทำรายงานยืนยันประสิทธิภาพระบบ

## Security Layer

เข้ารหัสข้อความด้วย AES ตรวจสอบความถูกต้องของ Sender ID และป้องกัน
Replay Attack โดยตรวจสอบ Timestamp ภายในช่วงเวลา 30 วินาที
หากข้อมูลไม่ถูกต้องต้องปฏิเสธการส่งต่อทันที

## Energy Profiling

เปรียบเทียบการใช้พลังงานในช่วง Scan Interval ต่าง ๆ เช่น 3s, 5s, 10s
พร้อมวัด CPU Usage และ Battery Drain ภายในช่วงทดสอบ 10 นาที

---

# Performance Validation Report

รายงานฉบับนี้ใช้ยืนยันว่าระบบสามารถทำงานได้ตามเป้าหมายที่กำหนดจริง
ไม่ใช่เพียงการทดสอบเชิงฟังก์ชัน

## Test Scenarios

  | Nodes | Target Latency |
| --- | --- |
| 2 | ≤ 1 second |
| 3 | ≤ 2 seconds |
| 5 | ≤ 3 seconds |
| 10 (Simulation) | ≤ 5 seconds |

## Measured Metrics

-   ค่าเฉลี่ย End-to-End Latency\
-   ค่าสูงสุดของ Latency\
-   อัตราการส่งสำเร็จ (%)\
-   อัตราการสูญหายของ Packet\
-   จำนวน Retry\
-   ระยะเวลาการฟื้นตัว\
-   อัตราการเกิด Duplicate\
-   ผลกระทบต่อพลังงานแบตเตอรี่

## Acceptance Criteria

-   Delivery Success ≥ 99%\
-   Packet Loss \< 1%\
-   Latency เฉลี่ย ≤ 3 วินาที (5 โหนด)\
-   Recovery ≤ 2 วินาที\
-   ไม่มีระบบล่มระหว่างทดสอบ

---

# Engineering Definition of Done

งานจะถือว่าเสร็จสมบูรณ์เมื่อ:

-   Unit Test Coverage ≥ 80%\
-   Integration Test ≥ 20 กรณี\
-   ผ่าน Failure Simulation\
-   มี Performance Validation Report\
-   ไม่มี Critical Bug\
-   เอกสารถูกอัปเดตครบถ้วน\
-   Demo สามารถรันซ้ำได้อย่างน้อย 3 ครั้งติดต่อกัน
