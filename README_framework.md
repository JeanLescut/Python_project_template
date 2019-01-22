# Project X (PLEASE ADAPT)

## 1. Creating the project and Deploying for the first time :

### 1.1 Clone the repo :

- Deploy the code under `/opt/` :
```
cd /opt/
sudo git clone ... # &#x1F534; TODO: PLEASE ADAPT 
sudo chown -R $(whoami)":"$(id -gn) ./Project # &#x1F534; TODO: PLEASE ADAPT 
cd ./Project # &#x1F534; TODO: PLEASE ADAPT 
# git checkout master # Only in prod
```

&#x1F534;


### 1.2 (If the project is using Python) Install Python Environment
- All project (or group of projects) run on their own Conda environment. This allows to fix not only python version but also specific version for each python module, that could be different from one project to another. Thus, any change of the machine, on any other project can NOT affect the current project. To create an environment, follow precise instructions here :
https://ewegithub.sb.karmalab.net/jlescutmuller/Dev_init_scripts/blob/master/01_Create_new_conda_env_and_kernel.sh

- Install the dependencies of your project. Example :
```
sudo ./bin/python -m pip install paramiko pandas pymssql # &#x1F534; TODO: PLEASE ADAPT 
```

### 1.3 Configure the local symlinks
```
cp -R ./bin_template ./bin
ll ./bin/
ln -sf /opt/miniconda3/envs/python36_controltower/bin/python ./bin/python # &#x1F534; TODO: PLEASE ADAPT 
```

### 1.4 In Inte/Prod only : Add Cron Job

- If the project is meant to be run regularly, add a line in `/etc/crontab`. Example :
```
00 03 *  *  *  root cd /opt/Project/; git pull; ./main.sh # &#x1F534; TODO: PLEASE ADAPT 
```
Or in prod :
```
00 03 *  *  *  root cd /opt/Project/; git pull; conf="prod.json" ./main.sh # &#x1F534; TODO: PLEASE ADAPT 
```


## 2. To run, to test :

In dev : `./main.sh`

Ad-hoc, in prod : `conf="prod.sh" ./main.sh` (this is dangerous, as it will potentially update prod data) 



## 3. Commiting a change ( = saving your change on Github, for versioning) :

#### If working using Jupyter :
> 1. make sure you dont open the same notebook in 2 different tabs, otherwise the changes of one can overwrite the changes made through the second...
> 2. Save your notebook (Windows : Ctrl + S, Mac : Cmd + S)
> 3. A .ipynb is never run in production, as a lot of unexpected behavior could happen. Instead, you can generate a .py file for it using :
> ```
> # From the Geneva server :
> find . -iregex ".*\.ipynb" | grep -v "\.ipynb_checkpoints" | xargs -I{} -d'\n' /opt/anaconda3/envs/python_3.6.2/bin/jupyter nbconvert --to python {}
> ```


Review and commit :
```
git status
git add --all
git commit -m 'foobar'
git push
```

## 4. Deploying ( = pushing your changes into production)
Merge :
Following the good practice https://stackoverflow.com/questions/14168677/merge-development-branch-with-master :
Merge first master into develop, then develop into master without conflicts :
```
git merge master # resolve any merge conflicts if there are any
git checkout master
git merge develop # there won't be any conflicts now
git push
git checkout develop # DO NOT FORGET THAT.
```
