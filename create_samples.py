import cv2
import numpy as np
import os

def create_sample_data():
    os.makedirs("data/samples", exist_ok=True)
    
    # Create a dummy handwriting sample for student123
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv2.putText(img, "Sample Handwriting", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imwrite("data/samples/student123.png", img)
    print("Created sample handwriting for student123 at data/samples/student123.png")

if __name__ == "__main__":
    create_sample_data()
