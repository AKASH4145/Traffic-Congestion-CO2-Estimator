## Traffic-Based CO₂ Emission Estimator (Computer Vision)

A real-time system that detects vehicles from traffic video using YOLOv3 + OpenCV and estimates CO₂ emissions. Includes analytics like peak emission tracking , recommended signal timing, and cleaner route suggestions.

Note : CO₂ values and route suggestions are estimates for demonstration and not sensor-based or map-based.

---


##  Features
- Real-time vehicle detection using YOLOv3 + OpenCV  
- Vehicle counting by class (car, bike, bus, truck)  
- CO₂ emission estimation using average emission factors  
- Peak CO₂ tracking with timestamp  
- Emission trend analysis (Increasing / Stable / Decreasing)  
- Recommended alternative routes based on estimated emissions  
- Adaptive traffic signal green-time recommendation (rule-based)  
- Live analytics dashboard (Tkinter UI)  


---

##  Motivation
Urban traffic congestion leads to increased fuel consumption and CO₂ emissions, contributing to air pollution and climate change. Most real-time pollution monitoring solutions require expensive sensors and infrastructure. This project explores a low-cost, camera-based approach to estimate traffic emissions and support smarter traffic management decisions.


---

##  Tech Stack
- Python  
- OpenCV  
- YOLOv3  
- Tkinter  
- JSON  

---

##  System Architecture

Workflow:
1. Input traffic video  
2. Vehicle detection using YOLOv3  
3. Vehicle counting per frame  
4. CO₂ estimation using emission factors  
5. Data exchange via JSON  
6. Live dashboard visualization  
7. Decision support (route + signal timing recommendations)

---

##  Project Structure

```text
Traffic Congestion & CO2 Estimator/
├── yolo/
│   ├── yolov3.cfg
│   ├── yolov3.weights   # (not committed to GitHub)
│   └── coco.names
├── src/
│   ├── main.py     # YOLO + vehicle detection & counting
│   └── dashboard.py   # Tkinter dashboard UI
├── Sample videos/
│   ├── traffic.mp4
│   └── traffic1.mp4
├── Sample videos/ 
|    ├── Dashboard.png
│    ├── Detection Window.png
|    └── Demo Video.mp4
├── emission.json      # generated at runtime
├── counts.json        # generated at runtime
├── requirements.txt
└── README.md

```
---

## Setup & Run

- git clone https://github.com/AKASH4145/Traffic-Congestion-CO2-Estimator
- cd traffic-co2-estimator  
- pip install -r requirements.txt  
- Download YOLOv3 files  
- python src/detector.py
- python src/main.py

---

## Demo Screenshots and Video
 ![Vehicle Detection](Demo%20Screenshots/Detection%20Window.png)
 ![Dashboard](Demo%20Screenshots/Dashboard.png)
 <video controls src="Demo Screenshots/Demo Video.mp4" title="Demo Video"></video>

---

## Observations

- Higher traffic density results in higher estimated CO₂ emission
- Emission peaks occur during congestion periods
- Trend analysis helps identify whether congestion is building up or clearing
- Route and signal recommendations demonstrate how this data can support traffic management decisions

---

## Limitations

- CO₂ values are estimated using average emission factors (not sensor-based)
- Auto-rickshaws are grouped under cars (YOLO model class limitation)
- No unique vehicle tracking (possible double counting)
- Accuracy depends on camera angle, lighting, and video quality
- Route and signal recommendations are rule-based prototypes

---

## Future Scope

- Vehicle tracking to avoid double counting
- Integration with live CCTV feeds
- Real-time map-based route recommendations
- Validation using real pollution sensors
- Custom model training for local vehicle types (e.g., auto-rickshaws)

---

## Author

Akash GS | Mechanical Engineering student exploring AI, computer vision, and applied Python development

---