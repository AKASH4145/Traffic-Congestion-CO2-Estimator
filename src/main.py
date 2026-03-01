import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import time

#Global Constants
EMISSION_FACTORS = {
    "car": 137,        
    "motorbike": 60,
    "bus": 800,
    "truck": 900
}
last_save_time = 0
SAVE_EVERY = 2  #seconds
peak_co2 = 0
peak_time = None
 #Traffic Signal Timing
low = 3000;
medium = 7000;

# Load YOLOv3
weight_path=r'C:\Users\akash\Desktop\Traffic Congestion & CO2 Estimator\Yolo\yolov3.weights'
config_path=r'C:\Users\akash\Desktop\Traffic Congestion & CO2 Estimator\Yolo\yolov3.cfg'
net = cv2.dnn.readNet(weight_path,config_path)

# Load class names
with open(r"C:\Users\akash\Desktop\Traffic Congestion & CO2 Estimator\Yolo\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Video source (0 = webcam or put video path)
cap = cv2.VideoCapture(r'C:\Users\akash\Desktop\Traffic Congestion & CO2 Estimator\Sample videos\traffic1.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Create blob
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for det in out:
            scores = det[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]

            if conf > 0.5:
                label = classes[class_id]
                if label in ["car", "bus", "truck", "motorbike"]:
                    cx, cy, bw, bh = det[0:4]
                    x = int((cx - bw/2) * w)
                    y = int((cy - bh/2) * h)
                    bw = int(bw * w)
                    bh = int(bh * h)

                    boxes.append([x, y, bw, bh])
                    confidences.append(float(conf))
                    class_ids.append(class_id)

    # Non-Max Suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    counts = {"car": 0, "bus": 0, "truck": 0, "motorbike": 0}

    if len(idxs) > 0:
        for i in idxs.flatten():
            x, y, bw, bh = boxes[i]
            label = classes[class_ids[i]]
            counts[label] += 1

            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidences[i]:.2f}",
                        (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
   
    now = time.time()
    
    with open("counts.json", "w") as f:
        json.dump({
            "timestamp": int(now),
            "counts": counts
        }, f, indent=2)
    last_save_time = now     

    #CO2 calculation

    def compute_co2(counts, factors):
      total = 0
      for vtype, count in counts.items():
        total += count * factors.get(vtype, 0)
        return total

    co2_per_min = compute_co2(counts, EMISSION_FACTORS)
    now = int(time.time())

    if co2_per_min > peak_co2:
      peak_co2 = co2_per_min
      peak_time = now

    #Emission Levels

    if co2_per_min < 3000:
      level = "LOW"
    elif co2_per_min < 7000:
      level = "MEDIUM"
    else:
      level = "HIGH"
    
# Alternate routes
    routes = {
    "Route A (Main Road)": co2_per_min,
    "Route B (Bypass Road)": int(co2_per_min * 0.7),
    "Route C (Inner Road)": int(co2_per_min * 0.5)
}      
    best_route = min(routes, key=routes.get)     

#Traffic Signal Optimization

    def recommend_signal_time(co2_per_min):
       if co2_per_min < low:
        return 30   # seconds
       elif co2_per_min < medium:
        return 45
       else:
        return 60
       
    signal_time = recommend_signal_time(co2_per_min)
   


    #Display counts

    text = f"Cars: {counts['car']}  Bikes: {counts['motorbike']}  Buses: {counts['bus']}  Trucks: {counts['truck']}"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(frame, f"Estimated CO2/min: {co2_per_min:.0f} g",
            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(frame, f"Emission Level: {level}",
            (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(frame, f"Recommended Green Signal Time: {signal_time} sec",
            (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    cv2.putText(frame,
            "CO2 values are estimates (not sensor-based)",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    #Updating JSON

    with open("emission.json", "w") as f:
     json.dump({
        "timestamp": int(now),
        "co2_per_min": int(co2_per_min),
        "level": level,
        "peak_co2": int(peak_co2),
        "peak_time": int(peak_time) if peak_time else None,
        "recommended_green_time": signal_time,
        "recommended_route": best_route,
        "route_emissions": routes
    }, f, indent=2)
    
    cv2.namedWindow("Vehicle Detection (YOLOv3)", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Vehicle Detection (YOLOv3)", 900, 700)
    cv2.imshow("Vehicle Detection (YOLOv3)", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()