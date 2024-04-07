import json



model_path = "/home/bakobi/repos/hub/comfyui/custom_nodes/ComfyUI-Manager/.cache/4245046894_model-list.json"

with open(model_path, "r", encoding="utf-8") as f:
    models = json.load(f)

for model in models:
    print(model)