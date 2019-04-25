# Framework for Python/Bash project 
Please use this framework (and follow these guidelines) for any project you intend to write (Python, Bash, R, whatever)

## 1. Why using this framework :
- Display a **standard Unix-like structure** for each project, **deployed in the same path** (`opt`). Hence the ramping-up time between projects is reduced, teammate can easily debug any projects ==> maintainance is made easier.
- Provide **common Python, Bash, etc... libraries**, that can be shared across projects. ==> Improve cross-project collaboartion, and avoid redundancy between project codes.
- Manage **environment-dependent parameters**, thus enforcing good practice, in a consistent manner across projects, and avoid Production accidents. Also allows overwritting parameters at launch time :)
- Manage **logging** in the project: Enforce all runs to be logged (good practice), in a consistent way accross project (language-agnostic), and print the log systematically both in a file, and in the standard output. ==> povide very good bases for debugging by any teammates.
- **Automatically archive** old logs, avoiding "out-of-space" issues for any projects.
- Propose a standard **Readme.md** for all newly-created projects using this framework
- Propose a way to **manage credentials** inside all projects, without publishing any passwords on git, and without complexifying the deployement process with a list of passwords to enter
- Implement a starting **.gitignore** file to make sure people don't unwillingly version `.swp`, `.csv`, `.dat`, `.log` or any suspecious other file extensions, or file in suspecious path like `./data/...` or `./tmp/...`
- Propose a **git pre-commit hook, to automatically convert .ipynb to .py**, thus making sure only `.py` goes into production
- Propose a system of **symlinked binaries** to easily deploy the project on any system


## 2. How to use this framework to create a new project :

1. First, create a repo in Github. Stay on the page with the git commands

2. On your local dev environment (example : Geneva), clone the framework :
```
git clone https://ewegithub.sb.karmalab.net/ARM-Pricing/Framework_projects.git
rm -rf ./Framework_projects/.git
mv ./Framework_projects/README_framework.md ./Framework_projects/README.md
mv ./Framework_projects ./Project # Please use the name of your project
cd ./Project
```
- In main.sh, by default, we keep the last 100 `.log` files. Please change if it doesnt suit you.
- In main.sh, you have as examples 3 scripts called. Please keep the technology that suits you and change the script name :)
- Don't forget to commit and push

Complete with git commands found on the Github pages :
```
git init
git add --all
git commit -m "First commit"
```

Copy-paste the 2 lines present on the Github page :
/!\ You should NOT use git@ewe... as a remote, as it will ask for ssh key instead of password
```
git remote add origin https://
git push -u origin master
```

Create a develop branch :
```
git checkout -B develop
git push origin develop
```

4. On github, click on your project name (top of the page) and all the framework should appear.
5. Change the default branch for 'develop'

## 3. Logging

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


## 4. Managing Credentials :
- For authenticating to external service (SQL, Hive, ...etc), please use the **user 's-shpm' rather than your own** 
- Please **keep the 'reading credentials' cell as it is**. Do not hardcode any path to any other file, or hard-code credentials yourself. the reason is that all system credentials should be in a single location, so when they change, a single change on the machine corrects all project at once
- If you need other system credentials, please add them under `/usr/local/share/credentials/`


## 5. Managing versioning :
- By convention, *master* branch is the Production branch. Every deployment should correspond to a commit on that branch
- By convention, *develop* is the Development branch, meaning the branch used to share advancements in the project without any deployment
- Please **configure *develop* branch as the default branch**, which prevents to work directly on master by mistake.
- For Geneva server : a system-wide gitignore has been created under `/etc/gitignore`, which ignore by default log files, swap files, or ipynb_checkpoints. To ignore any other files (expectially **large** files), please add them in your `.gitignore` file.
- For Geneva server : I configured a pre-commit filter to filter-out any cell output for the Jupyter notebook. which means :
  1. If the code does not change but the output changes (think about datetime for example), nothing will be commited, which is the right behavior
  2. You dont have to do anything, the filter detects all `.ipynb` files are apply the filter
  3. In case of very large cell output, you dont overload the git project.


## 6. Managing Dev/Prod variables :
 
Each projects are 4 kind of conf variable :

1. `./etc/local.sh` (SHELL) : this is file is **ignored** by git (already in `.gitignore`). It is used for storing all system-dependent variable (PYTHON_PATH, R_PATH, etc...)
You have to create it yourself using `cp ./etc/local.sh.template ./etc/local.sh`
>  **GOOD PRACTICE**: It is highly recommended to place a template for this file, so anybody could see the required local > > variable for that project. Example `./etc/local.sh.template`, that contains `PYTHON_PATH=...`.

2. `./etc/default.yml` (YAML) : This is the main configuration file.:
  - All values should not impact prod (example, for variable "DB", value should be "..Staging", and not the actual one.)
  - No variable should be system-dependent. (example. no variable like "PYTHON_PATH")
  You can think that file as containing all the default value. Also here to avoid repetition among dev, int, prod, etc...
  
3. `./etc/local.yml` (SHELL) : this is file is **ignored** by git (already in `.gitignore`). It is used for storing all local devlopment variables

4. All other paths in YAML (free to name whatever you want). This should be passed to the script as an argument in any long-running environment. There are not ignored by git and maintained by the team. Examples: 
  - For maintaining all togeteher a file that will contains value used in prod : `conf="prod.yml" ./main.sh`. This file should contains things like `DB="Project" # "Project" instead of "ProjectStaging"` or `Flash_Upload_Folder="SHPM/" # instead of "SHPM/Test/"`
  - Same for int : `conf="int.yml" ./main.sh`
  
> *Note*: This last layer of conf file could seem needless since you could already do one of the following :
>  1. maintaining `default.yml` in  different branches (`develop`, `master`...)
>  2. maintaining `local.yml` locally on your machine, on the prod server, on the dev server, etc...
> The reasons of adding this layer are :
> - Neither of these solutions allow for a safe-guard while working on prod server (on `master` branch). Launching a script in prod while (hot-fixing/debugging/having a look) is unfortunately common and should be prevented.
> - The solution 1 would have required to change `default.sh` after all merge to `master`.
> - The solution 2 would have mean to lose all prod/int variables/values in case of server crash.
> - Having this level of flexibility ensures perinity in the future.

## 7. Coding : good practice :
- Every project are deployed under `/opt/`, meaning:
   1. log are under `/opt/PROJECT/log/`
   2. binaries are under `/opt/PROJECT/bin/`
   3. Conf files are under `/opt/PROJECT/etc/`
   4. Data files are under `/opt/PROJECT/data/`
   Which means : Please do not hard-code any absolute path in the code.
- While working on the notebook, it can be useful to create cells to print or output variable. But while deploying in prod, make sure the script is as simple as possible
- Every project (bash or python) should contains a file named *main*, which is the only file to run to execute the project. Every other files are called directly or undirectly by this main.


