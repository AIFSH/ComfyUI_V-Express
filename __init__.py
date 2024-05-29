import os
import site
now_dir = os.path.dirname(os.path.abspath(__file__))

site_packages_roots = []
for path in site.getsitepackages():
    if "packages" in path:
        site_packages_roots.append(path)
if(site_packages_roots==[]):site_packages_roots=["%s/runtime/Lib/site-packages" % now_dir]
#os.environ["OPENBLAS_NUM_THREADS"] = "4"
for site_packages_root in site_packages_roots:
    if os.path.exists(site_packages_root):
        try:
            with open("%s/VExpress.pth" % (site_packages_root), "w") as f:
                f.write(
                    "%s\n%s/VExpress\n"
                    % (now_dir,now_dir)
                )
            break
        except PermissionError:
            raise PermissionError

if os.path.isfile("%s/VExpress.pth" % (site_packages_root)):
    print("!!!VExpress path was added to " + "%s/VExpress.pth" % (site_packages_root) 
    + "\n if meet `No module` error,try `python main.py` again, don't be foolish to pip install modules")



from huggingface_hub import snapshot_download
if not os.path.isfile(os.path.join(now_dir,"model_ckpts","v-express","v_kps_guider.pth")):
    snapshot_download(repo_id="tk93/V-Express",local_dir=now_dir)
else:
    print("V-Express use cache models,make sure your 'model_ckpts' complete")

from .nodes import LoadVideo,PreViewVideo,CombineAudioVideo,VExpress,LoadImagePath
WEB_DIRECTORY = "./web"
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadVideo": LoadVideo,
    "PreViewVideo": PreViewVideo,
    "CombineAudioVideo": CombineAudioVideo,
    "VExpress": VExpress,
    "LoadImagePath": LoadImagePath
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VExpress": "VExpress Node",
    "LoadVideo": "Video Loader",
    "PreViewVideo": "PreView Video",
    "CombineAudioVideo": "Combine Audio Video",
    "LoadImagePath": "LoadImagePath"
}
