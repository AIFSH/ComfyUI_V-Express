import os
import sys
import time
import folder_paths
import V_Express
from pydub import AudioSegment
from moviepy.editor import VideoFileClip,AudioFileClip
from imageio_ffmpeg import get_ffmpeg_exe

input_path = folder_paths.get_input_directory()
out_path = folder_paths.get_output_directory()

now_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(now_dir, "model_ckpts")
unet_config_path = os.path.join(model_path,"stable-diffusion-v1-5","unet","config.json")
vae_path = os.path.join(model_path,"sd-vae-ft-mse")
audio_encoder_path = os.path.join(model_path,"wav2vec2-base-960h")
insightface_model_path = os.path.join(model_path,"insightface_models")

vexpress_path = os.path.join(model_path,"v-express")
denoising_unet_path = os.path.join(vexpress_path,"denoising_unet.pth")
reference_net_path = os.path.join(vexpress_path,"reference_net.pth")
v_kps_guider_path = os.path.join(vexpress_path,"v_kps_guider.pth")
audio_projection_path = os.path.join(vexpress_path,"audio_projection.pth")
motion_module_path = os.path.join(vexpress_path,"motion_module.pth")

class VExpress:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ref_img":("IMAGE",),
                "audio": ("AUDIO",),
                "retarget_strategy":(["fix_face", "no_retarget", "offset_retarget", "naive_retarget"],{
                    "default": "fix_face"
                }),
                "device": ("STRING",{
                    "default": "cuda"
                }),
                "gpu_id": ("INT",{
                    "default": 0
                }),
                "dtype": ("STRING",{
                    "default": "fp16"
                }),
                "num_pad_audio_frames": ("INT",{
                    "default": 2
                }),
                "standard_audio_sampling_rate": ("INT",{
                    "default": 16000
                }),
                "image_width": ("INT",{
                    "default": 512
                }),
                "image_height": ("INT",{
                    "default": 512
                }),
                "fps": ("FLOAT",{
                    "default": 30.0
                }),
                "seed": ("INT",{
                    "default": 42
                }),
                "num_inference_steps": ("INT",{
                    "default": 30
                }),
                "guidance_scale": ("FLOAT",{
                    "default": 3.5
                }),
                "context_frames": ("INT",{
                    "default": 12
                }),
                "context_stride": ("INT",{
                    "default": 1
                }),
                "context_overlap": ("INT",{
                    "default": 4
                }),
                "reference_attention_weight": ("FLOAT",{
                    "default": 0.95
                }),
                "audio_attention_weight": ("FLOAT",{
                    "default": 3.
                }),
            },
            "optional":{
                "target_video": ("VIDEO",)
            }
        }
    
    CATEGORY = "AIFSH_VExpress"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO",)

    OUTPUT_NODE = False

    FUNCTION = "process"

    def process(self,ref_img,audio,retarget_strategy,device,
                gpu_id,dtype,num_pad_audio_frames,standard_audio_sampling_rate,
                image_width,image_height,fps,seed,num_inference_steps,guidance_scale,
                context_frames,context_stride,context_overlap,reference_attention_weight,
               audio_attention_weight,target_video=None):
        python_exec = sys.executable or "python"
        parent_directory = os.path.join(now_dir,"V_Express")
        # todo autoclip image and video to 512
        output_path = os.path.join(out_path,f"{time.time()}_vexpress.mp4")
        if target_video:
            kps_path = os.path.join(input_path,os.path.basename(target_video)[:-4]+"_kps.pth")
            audio_save_path = os.path.join(input_path,os.path.basename(target_video)[:-4]+"_aud.mp3")
            fps_cmd = f"{python_exec} {parent_directory}/scripts/extract_kps_sequence_and_audio.py --video_path {target_video} --kps_sequence_save_path {kps_path} \
            --audio_save_path {audio_save_path} --device {device} --gpu_id {gpu_id} --insightface_model_path {insightface_model_path} --height {image_height} --width {image_width}"
            os.system(fps_cmd)
        else:
            retarget_strategy = "fix_face"
            kps_path = None
        
        vexprss_cmd = f"{python_exec} {parent_directory}/inference.py --unet_config_path {unet_config_path} --vae_path {vae_path} --audio_encoder_path {audio_encoder_path} \
        --insightface_model_path {insightface_model_path} --denoising_unet_path {denoising_unet_path} --reference_net_path {reference_net_path} --v_kps_guider_path {v_kps_guider_path} \
        --audio_projection_path {audio_projection_path} --motion_module_path {motion_module_path} --retarget_strategy {retarget_strategy} --device {device} --gpu_id {gpu_id} --dtype {dtype} \
        --num_pad_audio_frames {num_pad_audio_frames} --standard_audio_sampling_rate {standard_audio_sampling_rate} --reference_image_path {ref_img} --audio_path {audio} --kps_path {kps_path if kps_path else 'None'} \
        --output_path {output_path} --image_width {image_width} --image_height {image_height} --fps {fps} --seed {seed} --num_inference_steps {num_inference_steps} --guidance_scale {guidance_scale} \
        --context_frames {context_frames} --context_stride {context_stride} --context_overlap {context_overlap} --reference_attention_weight {reference_attention_weight} --audio_attention_weight {audio_attention_weight}"
        print(vexprss_cmd)
        os.system(vexprss_cmd)
        return (output_path,)

class LoadAudio:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1].lower() in ["wav", "mp3","WAV","flac","m4a"]]
        return {"required":
                    {"audio": (sorted(files),)},
                }

    CATEGORY = "AIFSH_VExpress"

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        return (audio_path,)

class LoadImagePath:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "AIFSH_VExpress"

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"
    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        return (image_path,)
    
class CombineAudioVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"vocal_AUDIO": ("AUDIO",),
                     "bgm_AUDIO": ("AUDIO",),
                     "video": ("VIDEO",)
                    }
                }

    CATEGORY = "AIFSH_VExpress"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO",)

    OUTPUT_NODE = False

    FUNCTION = "combine"

    def combine(self, vocal_AUDIO,bgm_AUDIO,video):
        vocal = AudioSegment.from_file(vocal_AUDIO)
        bgm = AudioSegment.from_file(bgm_AUDIO)
        audio = vocal.overlay(bgm)
        audio_file = os.path.join(out_path,"ip_lap_voice.wav")
        audio.export(audio_file, format="wav")
        cm_video_file = os.path.join(out_path,"voice_"+os.path.basename(video))
        video_clip = VideoFileClip(video)
        audio_clip = AudioFileClip(audio_file)
        new_video_clip = video_clip.set_audio(audio_clip)
        new_video_clip.write_videofile(cm_video_file)
        return (cm_video_file,)


class PreViewVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "video":("VIDEO",),
        }}
    
    CATEGORY = "AIFSH_VExpress"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_video"

    def load_video(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui":{"video":[video_name,video_path_name]}}

class LoadVideo:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1] in ["mp4", "webm","mkv","avi"]]
        return {"required":{
            "video":(files,),
        }}
    
    CATEGORY = "AIFSH_VExpress"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO","AUDIO")

    OUTPUT_NODE = False

    FUNCTION = "load_video"

    def load_video(self, video):
        video_path = os.path.join(input_path,video)
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(input_path,video+".wav")
        video_clip.audio.write_audiofile(audio_path)
        return (video_path,audio_path,)
