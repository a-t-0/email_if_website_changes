# Sends an email if (part of) website visually changes.
Contains a lot of unused code.
## Usage: do once
Download/clone this repository.

0. If you don't have pip: open Anaconda prompt and browse to the directory of this readme:
```
cd /home/<your path to the repository folder>/
```

1. To use this package, first make a new conda environment and activate (it this automatically installs everything you need)
```
conda env create --file environment.yml
```

## Usage: do every time you start Anaconda:

3. Activate the conda environment you created:
```
conda activate get_gitlab_generation_token
```

## Usage: do every run (Set ssh-deploy key in GitHub for pushing build status icons)
```
python -m code.project1.src
```

You can also create a `email_pwd.txt` file one directory up outside this root dir if you don't want to type your email and pwd everytime. Give it content:
```
sender_email=<your email>
password=<your pwd>
```