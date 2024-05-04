# HackUPC_2024

pip install SpeechRecognition fuzzywuzzy

sudo apt-get install python3-pyaudio

pip install python-Levenshtein

pip install google-cloud-speech

## Execution to avoid a pile of messasges 
python3 main.py 2> errores.log

## Development set up
Install dependencies
```
pip install pyenv
pyenv install 3.11.0
pip install poetry
```

Go into the project folder and install the project's dependencies
```
pyenv local 3.11.0
python3 --version
poetry install
```

Every time you open the project run
```poetry shel```
