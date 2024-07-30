# No Voice Overed Quests TTS
[![Last Commit](https://img.shields.io/github/last-commit/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/commits/master)
[![Repo size](https://img.shields.io/github/repo-size/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/graphs/code-frequency)
[![LICENSE](https://img.shields.io/github/license/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/blob/master/LICENSE.md)


Have you ever wanted to listen to non-voiced quests in Genshin Impact or Honkai: Star Rail? Well, now it's possible with the use of AI.


## Important

On lower-end PCs, your game can take a SIGNIFICANT performance hit.

Also the use of AI voices is completely optional. So if you don't want to use them, you can skip some parts of the installation process.


## Installation

### Requirements

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.10 or [Anaconda](https://www.anaconda.com/download#downloads)
- [CUDA](https://developer.nvidia.com/cuda-toolkit-archive) (If you want to use GPU)
- [FFmpeg](https://ffmpeg.org/) (Can be skipped if you don't want to use AI)
- [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui) (Can be skipped if you don't want to use AI)


### Installing

1. Install [Python](https://www.python.org/) 3.10 or [Anaconda](https://www.anaconda.com/download#downloads) (Anaconda is useful if you want to use different Python versions and/or you don't want to mess with your main Python installation.)
2. Install [CUDA](https://developer.nvidia.com/cuda-toolkit-archive) version 11.8
3. Install [FFmpeg](https://ffmpeg.org/) and make sure that it's added to your PATH environment variable.
4. Install [Git](https://git-scm.com/)
5. Set up and install [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui). If you are using [Anaconda](https://www.anaconda.com/download#downloads) environments, you can skip making a venv while following the install guide for [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui).
6. Clone this repo.
```
git clone https://github.com/nitolar/No-Voice-Overed-Quests-TTS
```
7. If you created a venv or [Anaconda](https://www.anaconda.com/download#downloads) environment for [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui), you can reuse it or create a new one.
8. Install [Python](https://www.python.org/) requirements.
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```


### Updating

```
git pull
pip install -r requirements.txt --upgrade
```


### Usage

1. Configure `settings.yaml` to your liking.
2. Add some voices. An example of how to add one is in `voices/example.yaml`. (This step can be skipped if you don't want to use AI voices.)
3. Start [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui). (Only if you plan on using AI voices.)
```
python app.py
```

#### Worth to note! 

If you want to force the [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui) to use your CPU instead of your GPU, you can edit the `config.py` file like this:
```
# AROUND LINE 60
# USE GPU IF AVAILABLE (ORIGINAL CODE):
if torch.cuda.is_available():
# FORCE USAGE OF CPU:
if torch.cuda.is_available() == False:
```

4. Start the script.
```
python tts.py
```
5. You are ready to go!


## Changelog

### 30.07.2024

- Improved the process of cleaning up text passed to be read by pyttsx3 or AI TTS.
- Added more debugging text, making it easier to detect errors when creating the `Text Final`.
- Added colors to improve the readability of the output.
- Added some new commonly misinterpreted characters.
- Fixed the alt-tab feature not alt-tabbing to the game if no text was found.

### 29.07.2024

- Refined the text extraction accuracy; it should now be more precise.
- Added a new auto alt-tab feature; more info is available in `settings.yaml`.
- Added some new commonly misinterpreted characters.
- Fixed a lot of spelling mistakes 😑 and rephrased a lot of the text.

### 30.09.2023

- Fixed the script crashing if no text was found.
- Fixed the script not replacing commonly misinterpreted characters.
- Added some new commonly misinterpreted characters.

### 25.09.2023

- Initial release.


## Feedback

Like what you see? Give a star it motivates.

Found any bugs? Report them here: https://github.com/nitolar/No-Voice-Overed-Quests-TTS/issues


## Authors

- [nitolar](https://www.github.com/nitolar)


## Special thanks to

- [MrQuariti](https://www.youtube.com/@mrquariti261) For testing
- [litagin02](https://github.com/litagin02) For creating [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui)