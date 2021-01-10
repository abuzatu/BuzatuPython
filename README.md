This repo was created by Adrian Buzatu (adrian.buzatu@cern.ch).

This repo contains helper functions, skeleton of projects, instructions to set up python environments from the beginning on a new Mac. The goal is to set up a new Mac laptop to be able to do machine learning studies in Python. Also it serve as a Python tutorial and speed up development of new projects by re-using general code across several projects. For example: statistical calculations, manipulating of numpy arrays, pandas data frames, plots in matplotlib and seaborn, particle physics data analyses, time series, geo-spatial data analyses, predictions for classification or regression.

Below instuctions to set up a Python environment, from the beginning of having a new MacOS laptop up to doing a Machine Learning analysis.

It is a good practice to be able to have several Python versions installed, to choose for each project potentially another version of Python.

# Install the general MacOS enviroment

## Shell

Change the shell from `zsh` to `bash`. 
```
echo $SHELL
chsh -s /bin/bash
echo $SHELL
```

Warning, this does not work on a new Mac. Maybe [here](https://itnext.io/upgrading-bash-on-macos-7138bd1066ba) solution.

## Brew

Install `brea` following the steps from [here](https://osxdaily.com/2018/03/07/how-install-homebrew-mac-os/) me on `MacOS` they look like this. First install [brew](https://brew.sh/)

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
This will tell you to add `/opt/homebrew/bin` to your `PATH`, otherwise you will get
```
brew
-bash: brew: command not found
```
So add this to your `~/.profile`
```
export PATH=/opt/homebrew/bin:$PATH
```

But to add to the file, you need emacs, so let's install that first.

## Emacs

I did not find [these instructions](https://wikemacs.org/wiki/Installing_Emacs_on_OS_X) on the latest OS, like `El Sur`, but [these instructions](https://medium.com/really-learn-programming/configuring-emacs-on-macos-a6c5a0a8b9fa) worked. Run
```
brew tap d12frosted/emacs-plus
brew install emacs-plus@28 --with-modern-papirus-icon --with-cocoa
```
The option `--with-cocoa` will allow `Emacs` to open in pop up window, not only in the terminal. If this does not work, install also [XQuartz for MacOS](https://www.xquartz.org/) to have an `X11` system to pop up windows. The option `@28` means it is `Emacs` version `2.8`. You will get the text that `Emacs.app` was installed at `/opt/homebrew/opt/emacs-plus@28`. Now link the this to the main `/Applications` folder.
```
 ln -s /opt/homebrew/opt/emacs-plus@28/Emacs.app /Applications
```
Run in the terminal
```
alias emacs=/Applications/Emacs.app/Contents/MacOS/Emacs
```
Next you can finally modify the `~/.profile` file using
```
emacs -nw ~/.profile
```
and write
```
export PATH=/opt/homebrew/bin:$PATH
alias emacs=/Applications/Emacs.app/Contents/MacOS/Emacs
```

## Other aliases

I find useful to also configure the Mac environment with a few more aliases
```
alias rm='rm -i'
alias ls='ls -C -G -h'
alias grep='grep --color=auto'
alias j="jupyter notebook"
```

Now this will be run every time you open a new terminal.

# Python Environment

There are instructions [here](https://www.chrisjmendez.com/2017/08/03/installing-multiple-versions-of-python-on-your-mac-using-homebrew/) for older ones. For me on `MacOS` they look like this. First install [brew](https://brew.sh/)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
If you have it installed, update it to the latest
```
brew update

Install emacs

```
brew install emacs
```

```
Install `pyenv`
```
brew install pyenv
```
Install also these dependencies
```
brew install zlib
brew install sqlite
brew install bzip2
brew install libiconv
brew install libzip
```

Configure your Mac environment so that it uses `pyenv` to manage your packages and uses the packages from above from the new installed location. So in your `~/.profile` or `~/.bashrc` or equivalent add at the end these lines. It contains also some commented out lines that may be needed in the future.
```
# Configure the Python environments with PyEnv
#export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
# Configure your Mac environment so that it uses `pyenv` to manage your packages.
eval "$(pyenv init -)" #
#eval "$(pyenv virtualenv-init -)"
#
export CPPFLAGS="${CPPFLAGS} -I$(xcrun --show-sdk-path)/usr/include"
export LDFLAGS="${LDFLAGS} -L$(xcrun --show-sdk-path)/usr/lib"
#
export LDFLAGS="${LDFLAGS} -L/usr/local/opt/bzip2/lib"
export CPPFLAGS="${CPPFLAGS} -I/usr/local/opt/bzip2/include"
#
#export LDFLAGS="${LDFLAGS} -L/usr/local/opt/sqlite/lib"
#export CPPFLAGS="${CPPFLAGS} -I/usr/local/opt/sqlite/include"
#
#export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} /usr/local/opt/zlib/lib/pkgconfig"
#export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} /usr/local/opt/sqlite/lib/pkgconfig
```
Start a new terminal. By default it is still the Python 2.7.
```
python --version
```
Let's choose a version of Python `3.x.x` to install. To see all the versions of Python `3.x.x` that exist:
```
pyenv install -l | grep -ow 3.[0-9].[0-9] | sort
```

Let's choose and install the latest, currenty Python `3.9.0`. We can also install others.
```
pyenv install 3.9.0
pyenv install 3.8.6
pyenv install 3.7.9
```
Check the python versions installed
```
pyenv versions
```
You can set up one version as global for all cases. Python 2.x is no longer supported, so we can set as global `3.8.6`.
```
pyenv global 3.8.6
python --version
python
```
You can also set one other version in a particular folder (project, package). Just cd there and set for example `3.9.0`.
```
mkdir test
cd test
pyenv local 3.9.0
python --version
python
```
In either of these, you can later install the packages of Python libraries you need, for example
```
pip install numpy
pip install pandas
pip install matplotlib
```
In the future you only need to go out of the folder and you return to the global Python, or come back to the folder and automatically you are in the Python of that folder.
```
cd ..
python --version
cd test
python --version
```
Now you want to send this project to a friend to run it too, or to put it in production in a containarized environment. You store the list of installed packages in `requirements.txt`, and send this file, along with the Python version.
```
pip freeze > requiements.txt
```
Now in a fresh folder, you set up the same enviroment and libraries with
```
mkdir test2
cd test2
pyenv local 3.9.0
pip install -r requirements.txt
python --version
```
Now you can run the same code as initially.
