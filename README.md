# ComfyUI_V-Express
the comfyui custom node of [V-Express](https://github.com/tencent-ailab/V-Express) to make audio driven videos!
<div>
  <figure>
  <img alt='webpage' src="web.png?raw=true" width="600px"/>
  <figure>
</div>

## How to use
make sure `ffmpeg` is worked in your commandline
for Linux
```
apt update
apt install ffmpeg
```
for Windows,you can install `ffmpeg` by [WingetUI](https://github.com/marticliment/WingetUI) automatically

then!
```
git clone https://github.com/AIFSH/ComfyUI_V-Express.git
cd ComfyUI_V-Express
pip install -r requirements.txt

## insatll xformers match your torch,for torch==2.1.0+cu121
pip install xformers==0.0.22.post7 
```
weights will be downloaded from huggingface

You can also download [model_ckpts](https://huggingface.co/tk93/V-Express) manually then put it in `ComfyUI_V-Express`


## Tutorial
- [Demo]()

## WeChat Group && Donate
<div>
  <figure>
  <img alt='Wechat' src="wechat.jpg?raw=true" width="300px"/>
  <img alt='donate' src="donate.jpg?raw=true" width="300px"/>
  <figure>
</div>
    
## Thanks
- [V-Express](https://github.com/tencent-ailab/V-Express)
