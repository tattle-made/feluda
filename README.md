## setup:
### ubuntu-swair
1.  Setup virtual env 
    `virtualenv --no-site-packages -p python3.6 .`
2. Activate the env
    `source bin/activate`
3. Install pip-tools.
    `pip install pip-tools`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc. `pip-compile` will generate `requirements.txt` which will
   have all the dependencies.
    `pip-compile requirements.in`
    `pip install -r requirements.txt`
5. Run local server
    `python application.py`

### windows-conda-git-bash [failing]
1.  setup conda env
    `conda create -n tattle python=3.6`
2. Activate the env
    `conda activate tattle`
3. Install pip-tools.
    `pip install pip-tools`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc. `pip-compile` will generate `requirements.txt` which will
   have all the dependencies.
    `pip-compile requirements.in`  TODO: this step fails
    `pip install -r requirements.txt`  
        - TODO: this fails on torch==1.1.0,  
        - and fasttext due to bad VisualStudio C++ install, issue: https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe
    Fix run this prior:  
    `pip3 install torch===1.1.0 torchvision===0.3.0 -f https://download.pytorch.org/whl/torch_stable.html`
5. Run local server
    `python application.py`

### windows-wsl-ubuntu
update apt-get:  
`sudo apt-get update`  
1.  Setup virtual env 
    install virtualenv:  
    `sudo apt install virtualenv`
    `mkdir py36`  
    `virtualenv --no-site-packages -p python3.6 .`
2. Activate the env
    `cd py36`  
    `source bin/activate`
3. Install pip-tools.
    install pip3:  
    `sudo apt install python3-pip`
    `pip3 install pip-tools`
    `git clone git@github.com:tattle-made/tattle-api.git`  
    `cd tattle-api`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc. `pip-compile` will generate `requirements.txt` which will
   have all the dependencies.
    `pip-compile requirements.in`
    cannot see pip-tools at ALL
    `pip install -r requirements.txt`
5. Run local server
    `python application.py`

## steps after setup
- create word2vec
    - cd word2vec/
    - . get_data.sh
    - python gen_sqlite.py
- have local server running
    - python application.py

## documentation
`aplication.py`: user-facing API functions, removed references to google vision API, added comments
`analyzer.py`: get word embeddings and CNN representation of images, added comments  
`search.py`: classes for duplication detection within threshold  
`db.py`: wrappers for different databases, added sqlite wrapper  
`./video_analysis/`: extract frames from videos  
`./tests/`: test text/image API functions

## application testing commands
find_text [fails: no google API connection]: `curl -X POST localhost:5000/find_text -H "Content-Type: application/json" -d '{"image_url": "https://i.redd.it/qy14se6kuid11.jpg"}'`  
upload_text: `curl -X POST localhost:5000/upload_text -H "Content-Type:application/json" -d '{"text": "i like pie"}'`  
find_duplicate: `curl -X POST localhost:5000/find_duplicate -H "Content-Type: application/json" -d '{"text": "this is english!"}'`  
find_duplicate: `curl -X POST localhost:5000/find_duplicate -H "Content-Type: application/json" -d '{"image_url": "https://i.redd.it/qy14se6kuid11.jpg"}'`  
