import os
now_dir = os.path.dirname(os.path.abspath(__file__))
from huggingface_hub import snapshot_download
if not os.path.isfile(os.path.join(now_dir,"model_ckpts","v-express","v_kps_guider.pth")):
    snapshot_download(repo_id="tk93/V-Express",local_dir=now_dir)
else:
    print("V-Express use cache models,make sure your 'model_ckpts' complete")

from .nodes import LoadVideo,PreViewVideo,CombineAudioVideo,VExpress
WEB_DIRECTORY = "./web"
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadVideo": LoadVideo,
    "PreViewVideo": PreViewVideo,
    "CombineAudioVideo": CombineAudioVideo,
    "VExpress": VExpress
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VExpress": "VExpress Node",
    "LoadVideo": "Video Loader",
    "PreViewVideo": "PreView Video",
    "CombineAudioVideo": "Combine Audio Video",
}
