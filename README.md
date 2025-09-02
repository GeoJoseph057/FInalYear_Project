# 🤖 Telechir Robotic Arm with Adaptive Grip Control

This repository contains the design and development of a **telechir robotic arm** capable of mimicking human hand movements while applying **adaptive grip control** for safe object handling.

The system integrates:
* **Master (Glove):** Equipped with FSR sensors + ESP32 for gesture detection.
* **Slave (Robotic Arm):** 3D printed InMoov-based robotic arm controlled by MG90S servo motors & Raspberry Pi 5.
* **Object Detection:** YOLOv8 for real-time object recognition.
* **Grip Control:** PID-based adaptive force adjustment using FSR feedback.
* **Communication:** MQTT protocol for low-latency data transfer.

## 🚀 Features

* Human-like robotic arm design
* Real-time **object detection + classification** (YOLOv8)
* Adaptive grip control with **4 grip levels**
* Wireless **master-slave communication** using MQTT
* PID-based precise servo actuation
* Tested on multiple objects (e.g., phone, tape, delicate items)

## 🛠️ Hardware Used

* ESP32 / ESP8266 (Master glove controller)
* Force Sensing Resistors (FSRs)
* Raspberry Pi 5
* MG90S Micro Servo Motors
* Camera Module (for YOLO detection)
* 3D Printed InMoov-based arm (PLA material)

## 📊 Results

* Successfully grasped and released objects with adaptive force
* YOLOv8 achieved real-time detection (~25 FPS on Raspberry Pi 5)
* Robust wireless communication via MQTT
* Achieved **high grip success rate** with minimal slippage

## 🔮 Future Scope

* Integrating reinforcement learning for improved grip control
* Extending for **surgical/medical applications**
* Energy-efficient design for portable robotic systems

## 👨‍💻 Authors

* Austin Jeremiah J
* Clatson J
* Geo Joseph

Supervisor: **Mr. S. Robert Rajkumar, AP/ECE, LICET**

## 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.
