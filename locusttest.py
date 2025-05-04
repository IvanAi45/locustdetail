import os
import base64
import uuid
import random
from locust import HttpUser, task, between

# Specify a folder for storing images
IMAGE_DIR = "inputfolder"

# On startup, load all images from this folder and encode them in Base64.
def load_images_as_base64(image_dir):
    imgs = []
    for fn in os.listdir(image_dir):
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(image_dir, fn)
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                imgs.append(b64)
    if not imgs:
        raise RuntimeError(f"No images found in {image_dir}")
    return imgs

IMG_POOL = load_images_as_base64(IMAGE_DIR)

class CloudPoseUser(HttpUser):
    wait_time = between(1, 0)

    @task(1)
    def pose_json(self):
        req_id = str(uuid.uuid4())
        # randomly choose 1 img
        img_b64 = random.choice(IMG_POOL)
        payload = {"id": req_id, "image": img_b64}
        self.client.post("/pose/json", json=payload, name="/pose/json",timeout=60)

    @task(2)
    def pose_image(self):
        req_id = str(uuid.uuid4())
        img_b64 = random.choice(IMG_POOL)
        payload = {"id": req_id, "image": img_b64}
        self.client.post("/pose/image", json=payload, name="/pose/image",timeout=60)

