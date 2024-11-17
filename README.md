# Auto Subtitle Generator Using Whisper-Large-V3-Turbo-Ct2
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NeuralFalconYT/edge-tts-webui/blob/main/edge_tts_webui_colab.ipynb) <br>
[![hfspace](https://img.shields.io/badge/🤗-Space%20demo-yellow)](https://huggingface.co/spaces/NeuralFalcon/Edge-TTS) <br>
This application can run on CPU or CUDA.

### Step 1:
```
git clone https://github.com/NeuralFalconYT/edge-tts-webui.git
```
### Step 2:
```
cd edge-tts-webui
```
### Step 3:
```
pip install -r requirements.txt
```
### Step 4:
For local development:
```
python app.py 
```
For debugging:
```
python app.py --debug 
```
For cloud servers or notebooks:
```
python app.py --debug --share
```
```--debug```: Enables debug mode, providing more detailed logs and helpful error messages.<br>
```--share```: Shares the application by generating a public link, allowing access from external networks.
![app](https://github.com/user-attachments/assets/98c720ea-6cfd-4584-a194-0e1bf8e352ea)

### Credit:
[edge-tts GitHub](https://github.com/rany2/edge-tts)


