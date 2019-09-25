## setup:
### ubuntu
1.  Setup virtual env  
    `virtualenv --no-site-packages -p python3.6 .`
2. Activate the env  
    `source bin/activate`
3. Install pip-tools  
    `pip install pip-tools`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc   
   `pip-compile` will generate `requirements.txt` which will have all the dependencies  
    `pip-compile requirements.in`  
    `pip install -r requirements.txt`  
5. Run local server  
    `python application.py`

<!-- ### windows-conda-git-bash [failing]
1.  setup conda env  
    `conda create -n tattle python=3.6`
2. Activate the env  
    `conda activate tattle`
3. Install pip-tools  
    `pip install pip-tools`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc
   `pip-compile` will generate `requirements.txt` which will have all the dependencies  
    `pip-compile requirements.in`  TODO: this step fails  
    `pip install -r requirements.txt`  
        - TODO: this fails on torch==1.1.0,  
        - and fasttext due to bad VisualStudio C++ install, issue: https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe
    Fix run this prior:  
    `pip3 install torch===1.1.0 torchvision===0.3.0 -f https://download.pytorch.org/whl/torch_stable.html`
5. Run local server
    `python application.py` -->

### windows-wsl-ubuntu
`sudo apt-get update` ~ update package lists
1.  Setup virtual env   
    `sudo apt install virtualenv`  
    `mkdir py36`  
    `virtualenv --no-site-packages -p python3.6 ./py36`
2. Activate the env  
    `source py36/bin/activate`
3. Install pip-tools  
    `pip install pip-tools`     
4. Clone repo  
    `git clone git@github.com:tattle-made/tattle-api.git`  
    `cd tattle-api`
4. `requirements.in` should contain the high level packages that we want e.g.
   flask, numpy etc  
   `pip-compile` will generate `requirements.txt` which will have all the dependencies  
    `pip-compile requirements.in`  TODO: https://github.com/jazzband/pip-tools/issues/832  
    `pip install -r requirements.txt`
5. setup db
    - create word2vec
        - `cd word2vec/`
        - `. get_data.sh`
        - `python gen_sqlite.py`
    - create mongodb
        - db.py => create_mongo_db()
    - define .env (see env_template)
5. Run local server  
    `python application.py`  

- Misc. in case of installation errors: https://stackoverflow.com/questions/22571848/debugging-the-error-gcc-error-x86-64-linux-gnu-gcc-no-such-file-or-directory
    - sudo apt-get install gcc build-essential python3-dev

## documentation
`application.py`: user-facing API functions  
`analyzer.py`: get word embeddings and CNN representation of images  
`search.py`: classes for duplication detection within threshold  
`db.py`: wrappers for different databases  
`./video_analysis/`: extract frames from videos    
`./tests/`: test API functions

## application testing
define params in .env  
`. testing_live_server.sh`  
`cat ./tests/testing_live_server.out`  
`cat ./tests/testing_live_server.err`

