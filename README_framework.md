# Project X (&#x1F534; PLEASE ADAPT)

## 1. Creating  the project and Deploying for the first time :

### 1.1 Clone the repo :

- Deploy the code under `/opt/` :
<pre><code>
cd /opt/
sudo git clone ... # &#x1F534; TODO: PLEASE ADAPT 
sudo chown -R $(whoami)":"$(id -gn) ./Project # &#x1F534; TODO: PLEASE ADAPT 
cd ./Project # &#x1F534; TODO: PLEASE ADAPT 
# git checkout master # Only in prod
</code></pre>




### 1.2 (If the project is using Python) Install Python Environment
- All project (or group of projects) run on their own Conda environment. This allows to fix not only python version but also specific version for each python module, that could be different from one project to another. Thus, any change of the machine, on any other project can NOT affect the current project. To create an environment, follow precise instructions here :

#########################################################
### Step 1 : Installing a new conda env :
#########################################################

# This create a conda env on the machine. Persistent at each reboot.
# More info at : https://conda.io/docs/user-guide/tasks/manage-environments.html
# 1) it is VISIBLE in '/opt/anaconda3/bin/conda env list'
# 2) it is VISIBLE in 'ls -la /opt/anaconda3/envs' (because this has been launched from root)
# 3) it is NOT visible in 'ls -la /usr/local/share/jupyter/kernels/'
# 4) it is NOT visible in Jupyter interface
# Note : if not done in root ;
#    - the conda env will be installed in /home/{user}/.conda/env ...
#    - the conda env will not be visible from a root session => unable to install it as a Jupyterhub kernel
# Examples :
sudo /opt/anaconda3/bin/conda  create -n python_2.7.14     python=2.7.14 ipykernel # (in Dev)
sudo /opt/anaconda3/bin/conda  create -n python_3          python=3      ipykernel # (in Dev) Python 3 latest
sudo /opt/miniconda3/bin/conda create -n python27_projectx python=2.7.14 ipykernel # (in Prod) Env of a project "ProjectX"
sudo /opt/miniconda3/bin/conda create -n python36_projectx python=3.6.2  ipykernel # (in Prod) Env of a project "ProjectY"

# Verification : You can verify that the new conda env has been created :
/opt/anaconda3/bin/conda env list # (in Dev)
/opt/miniconda3/bin/conda env list # (in Prod)


#########################################################
### Step 2 : Install this "conda env" as a kernel in Jupyterhub
### WARNING : this step is NOT relevant in Int/Prod
#########################################################

# Install kernel : This will installed the CURRENTLY active conda env in /usr/loacl/share/jupyter/kernels
# Source 1 : http://ipython.readthedocs.io/en/stable/install/kernel_install.html
# You have to active the environment before you can launch this command
# 1) it becomes visible in 'ls -la /usr/local/share/jupyter/kernels/'
# 2) it becomes visible in Jupyter interface
# Note : the '--name' has nothing to do with the name previously created. 
#        This is the ipykernel name, that can be different than the conda env name
#        But by convention, we set them up to be THE SAME.
sudo /opt/anaconda3/envs/{env_name}/bin/python -m ipykernel install --name {same as conda env} --display-name "{displayed text in Jupyterhub}"


#########################################################
### DO NOT :
#########################################################

# Step 3 : Don't put '--user' as it would install the kernel only for the current user (root)
# Step 3 : his is NOT working : /opt/anaconda3/bin/ipython kernel install --name python_2.7.14 --display-name "Python 2.7.14"


- Install the dependencies of your project. Example :
<pre><code>
sudo ./bin/python -m pip install paramiko pandas pymssql # &#x1F534; TODO: PLEASE ADAPT 
</code></pre>

### 1.3 Configure the local symlinks
<pre><code>
cp -R ./bin_template ./bin
ll ./bin/
ln -sf /opt/miniconda3/envs/python36_controltower/bin/python ./bin/python # &#x1F534; TODO: PLEASE ADAPT 
</code></pre>


### 1.4 In Inte/Prod only : Add Cron Job

- If the project is meant to be run regularly, add a line in `/etc/crontab`. Example :
<pre><code>
00 03 *  *  *  root cd /opt/Project/; git pull; ./main.sh # &#x1F534; TODO: PLEASE ADAPT 
</code></pre>
Or in prod :
<pre><code>
00 03 *  *  *  root cd /opt/Project/; git pull; conf="prod.json" ./main.sh # &#x1F534; TODO: PLEASE ADAPT 
</code></pre>


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
