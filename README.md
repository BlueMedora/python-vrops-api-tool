## Installing vropts-api-tool
grab the latest binary from releases

## Contributing
please file an issue or feature request in github issues
PRs are welcome

## Building vrops-api-tool
### Python scripts to collect data from vrops
 - `brew update`
 - `brew install pyenv`
 - `pyenv init 2>> ~/.bash_profile` (or ~/.zshrc)
 - reload shell
 - `pyenv install 3.5.2`
 - `pip install -r requirements.txt`
 - `./suite-api-tool/tool_ui.py`

### Building Redistributable
 After running the above commands run:
 - `pip install git+https://github.com/pyinstaller/pyinstaller.git`
 - `./make_dist.sh`
 in addition, make sure that your .bashrc contains pyenv's init (`eval $(pyenv init -)`)

### Troubleshooting
- pyenv init
```
dyld: Library not loaded: /usr/local/opt/readline/lib/libreadline.6.dylib\
  Referenced from: /usr/local/bin/bash
    Reason: image not found
  Trace/BPT trap: 5
```

  - make sure that `bash` is up to date. 
    - do `brew update` and `brew upgrade`
    - and `which bash` points to `/usr/local/bin/bash`

- pip install -r requirements.txt
```
Collecting PyQt5==5.7 (from -r requirements.txt (line 1))
  Could not find a version that satisfies the requirement PyQt5==5.7 (from -r requirements.txt (line 1))
   (from versions: )
  No matching distribution found for PyQt5==5.7 (from -r requirements.txt (line 1))
```

  - ensure that your `~/.bashrc` or `~/.bash_profile` or `~/.zshrc` includes the line from `pyenv init`
  - Check that `pyenv version` is set by `./python-vrops-monitor/.python-version` and that the version of python is `3.5.2`


![image](https://cloud.githubusercontent.com/assets/9042425/20268344/bde71282-aa4c-11e6-8dd9-6d1254c90a12.png)
![image](https://cloud.githubusercontent.com/assets/9042425/20268347/bfef7ace-aa4c-11e6-9423-d528a150a2cf.png)
