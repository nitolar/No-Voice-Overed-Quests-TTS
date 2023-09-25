# No Voice Overed Quests TTS
[![Last Commit](https://img.shields.io/github/last-commit/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/commits/master)
[![Repo size](https://img.shields.io/github/repo-size/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/graphs/code-frequency)
[![LICENSE](https://img.shields.io/github/license/nitolar/No-Voice-Overed-Quests-TTS)](https://github.com/nitolar/No-Voice-Overed-Quests-TTS/blob/master/LICENSE.md)


Have you ever wanted to listen to not voice overed quests in Genshin Impact or Honkai: Star Rail? Well now it possible with use of the AI.


## Important

On lower end pc's your game can take SIGNIFICANT performance hit.

Also the use of the AI voices is completely optional. So if you don't want to use it, you can skip some parts of the install process.


## Installation

### Requirements

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.10 or [Anaconda](https://www.anaconda.com/download#downloads)
- [CUDA](https://developer.nvidia.com/cuda-toolkit-archive) (If you want to use GPU)
- [FFmpeg](https://ffmpeg.org/) (Can be skiped if you don't want to use AI)
- [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui) (Can be skiped if you don't want to use AI)


### Installing

1. Install [Python](https://www.python.org/) 3.10 or [Anaconda](https://www.anaconda.com/download#downloads) (Anaconda is useful if you want to use different python versions and/or you don't want to mess with your main install of python.)
2. Install [CUDA](https://developer.nvidia.com/cuda-toolkit-archive) version 11.8
3. Install [FFmpeg](https://ffmpeg.org/) and make sure that it's added to your Path environment variable.
4. Install [Git](https://git-scm.com/)
5. Set up and install [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui). If you are using [Anaconda](https://www.anaconda.com/download#downloads) environments you can skip making a venv while following the install guide of the [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui).
6. Clone this repo.
```
git clone https://github.com/nitolar/No-Voice-Overed-Quests-TTS
```
7. If you made venv/[Anaconda](https://www.anaconda.com/download#downloads) environment for [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui) you can reuse it or create a new one.
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
2. Add some voices. Example how to add one is in `voices/example.yaml`. (Can be skipped if you don't want to use AI voices)
3. Start [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui). (If you plan on using AI voices)
```
python app.py
```

#### Worth to note! 

If you want to force the [RVC-TTS-WEBUI](https://github.com/litagin02/rvc-tts-webui) to use your CPU insted of your GPU you can edit the `config.py` file like this:
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