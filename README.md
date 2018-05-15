# Framework for Python/Bash project 
Please use this framework for any project you intend to write in Python and/or Bash.

## 1. Creating the project and Deploying for the first time :

- Deploy the code under `/opt/` :
```
cd /opt/
sudo git clone ...
sudo chown -R $(whoami)":"$(id -gn) ./Project 
cd ./Project
# git checkout master # Only in prod
```

- In main.sh, by default, we keep the last 100 `.log` files. Please change if it doesnt suit you.

- Copy `local.sh.template` into your `local.sh` and adapt it for your local envinroment 
```
cp ./etc/local.sh.template ./etc/local.sh
vim ./etc/local.sh
```

- If the project is meant to be run regularly, add a line in `/etc/crontab`. Example :
```
00 03 *  *  *  root /opt/Project/main.sh
```

#### If you use Bash utils :
- Make sure the python_utils conda envs is properly installed on the machine. If not (brand new server for example), please follow instructions here :
https://ewegithub.sb.karmalab.net/jlescutmuller/Dev_init_scripts/blob/master/01_Create_new_conda_env_and_kernel.sh

#### If you use Python :

- All project (or group of projects) run on their own Conda environment. This allows to fix not only python version but also specific version for each python module, that could be different from one project to another. Thus, any change of the machine, on any other project can NOT affect the current project. To create an environment, follow precise instructions here :
https://ewegithub.sb.karmalab.net/jlescutmuller/Dev_init_scripts/blob/master/01_Create_new_conda_env_and_kernel.sh

- Install the dependencies of your project. Example :
```
sudo /opt/miniconda3/envs/python36_controltower/bin/python -m pip install paramiko
sudo /opt/miniconda3/envs/python36_controltower/bin/python -m pip install pymssql
```


## 2. Logging

### Bash
- A logging library has already been implemented. Please see source code for documentation. It supports log level, and level/keywords highlighting. Please always use this function while logging in bash.

- When main.sh is called, it :
  1. It delete all the old log on the machine, if any
  2. log everything to stdout, **AND** to a file (example : ./log/2018-05-04_053021.log)

  Therefore, you don't have to deal with bash redirection yourself (in Crontab for example), and all execution (even the manual ones) are logged.

### Python
- The notebook already contains a logging properly configured. **Please use this library rather than print() or your own**
  1. Because the format of this library is normalize, which ease post-treatment of logs for all projects
  2. Because some imported modules will automatically add their insightful logs to the file
- **Prefer to log to stdout (as shown in the example notebook)** than logging directly to a file. the redirection to a file happens in bash, which allows redirecting Exception (or stderr in general) as well.



## 3. Managing Credentials :
- For authenticating to external service (SQL, Hive, ...etc), please use the **user 's-shpm' rather than your own** 
- Please **keep the 'reading credentials' cell as it is**. Do not hardcode any path to any other file, or hard-code credentials yourself. the reason is that all system credentials should be in a single location, so when they change, a single change on the machine corrects all project at once
- If you need other system credentials, please add them under `/usr/local/share/credentials/`

## 4. Managing versioning :
- By convention, *master* branch is the Production branch. Every deployment should correspond to a commit on that branch
- By convention, *develop* is the Development branch, meaning the branch used to share advancements in the project without any deployment
- Please **configure *develop* branch as the default branch**, which prevents to work directly on master by mistake.
- For Geneva server : a system-wide gitignore has been created under `/etc/gitignore`, which ignore by default log files, swap files, or ipynb_checkpoints. To ignore any other files (expectially **large** files), please add them in your `.gitignore` file.
- For Geneva server : I configured a pre-commit filter to filter-out any cell output for the Jupyter notebook. which means :
  1. If the code does not change but the output changes (think about datetime for example), nothing will be commited, which is the right behavior
  2. You dont have to do anything, the filter detects all `.ipynb` files are apply the filter
  3. In case of very large cell output, you dont overload the git project.

## 5. Managing Dev/Prod variables :

All conf file are written in bash, as the project could be (or become) an hybrid Bash/Python project. And it's easier to parse bash conf in python than a python conf (yaml, json...) in bash.

Each projects are 3 kind of conf variable :

1. `./etc/default.sh` : This is the main configuration file.:
  - All values should not impact prod (example, for variable "DB", value should be "..Staging", and not the actual one.)
  - No variable should be system-dependent. (example. no variable like "PYTHON_PATH")
  
  You can think that file as containing all the default value. Also here to avoid repetition among dev, int, prod, etc...

2. `./etc/local.sh` : this is file is **ignored** by git (already in `.gitignore`). You have to create it yourself to store your development variable. It is used for 2 reasons :
  - Storing all system-dependent variable (PYTHON_PATH, )
  - All changes on the default variable for test that you do not wish to share with other collaborator.
 It can be tempting to put credentials on that file since it's not versionned. Please don't and follow the **Credentials** section of this doc.
 
>  **GOOD PRACTICE**: It is highly recommended to place a template for this file, so anybody could see the required local > > variable for that project. Example `./etc/local.sh.template`, that contains `PYTHON_PATH=...`.

3. All other paths (free to name whatever you want). This should be passed to the script as an argument in any long-running environment. There are not ignored by git and maintained by the team. Examples: 
  - For maintaining all togeteher a file that will contains value used in prod : `conf="prod.sh" ./main.sh`. This file should contains things like `DB="Project" # "Project" instead of "ProjectStaging"` or `Flash_Upload_Folder="SHPM/" # instead of "SHPM/Test/"`
  - Same for int : `conf="int.sh" ./main.sh`
  
> *Note*: This last layer of conf file could seem needless since you could already do one of the following :
>  1. maintaining `default.sh` in  different branches (`develop`, `master`...)
>  2. maintaining `local.sh` locally on your machine, on the prod server, on the dev server, etc...
> The reasons of adding this layer are :
> - Neither of these solutions allow for a safe-guard while working on prod server (on `master` branch). Launching a script in prod while (hot-fixing/debugging/having a look) is unfortunately common and should be prevented.
> - The solution 1 would have required to change `default.sh` after all merge to `master`.
> - The solution 2 would have mean to lose all prod/int variables/values in case of server crash.
> - Having this level of flexibility ensures perinity in the future.

## 6. Coding : good practice :
- Every project are deployed under `/opt/`, meaning:
   1. log are under `/opt/PROJECT/log/`
   2. binaries are under `/opt/PROJECT/bin/`
   3. Conf files are under `/opt/PROJECT/etc/`
   4. Data files are under `/opt/PROJECT/data/`
   Which means : Please do not hard-code any absolute path in the code.
- While working on the notebook, it can be useful to create cells to print or output variable. But while deploying in prod, make sure the script is as simple as possible
- Every project (bash or python) should contains a file named *main*, which is the only file to run to execute the project. Every other files are called directly or undirectly by this main.



## 7. Deploying a change :

#### 7.1 If working using Jupyter :
1. make sure you dont open the same notebook in 2 different tabs, otherwise the changes of one can overwrite the changes made through the second...
2. Save your notebook (Windows : Ctrl + S, Mac : Cmd + S)
3. A .ipynb is never run in production, as a lot of unexpected behavior could happen. Instead, you can generate a .py file for it using :
```
# From the Geneva server :
/opt/anaconda3/envs/python_3.6.2/bin/ipython nbconvert ./*.ipynb --to script
```


#### 7.2 Review, commit your changes, merge and integrate :

Review and commit :
```
git status
git add --all
git commit -m 'foobar'
```

Merge :
Following the good practice https://stackoverflow.com/questions/14168677/merge-development-branch-with-master :
Merge first master into develop, then develop into master without conflicts :
```
git merge master # resolve any merge conflicts if there are any
git checkout master
git merge develop # there won't be any conflicts now
git checkout develop # DO NOT FORGET THAT.
```


Integrate :
```
ssh chcxarmrop001
cd /opt/Project/
git pull
```

## 8. To run :


In dev :
```
./main.sh
```

Ad-hoc, in prod (to test dangerously) :
```
conf="prod.sh" ./main.sh
```
