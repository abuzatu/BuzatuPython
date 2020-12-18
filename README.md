This repo was created by Adrian Buzatu (adrian.buzatu@cern.ch).

This repo contains helper functions, skeleton of projects, instructions to set up python environments. The goal is to serve as a Python tutorial and speed up development of new projects by re-using general code across several projects. For example: statistical calculations, manipulating of numpy arrays, pandas data frames, plots in matplotlib and seaborn, particle physics data analyses, time series, geo-spatial data analyses, predictions for classification or regression.

Below instuctions to set up a Python environment, from the beginning of having a new MacOS laptop up to doing a Machine Learning analysis.

It is a good practice to be able to have several Python versions installed, to choose for each project potentially another version of Python.

# Steps

Follow the steps from [here](https://www.chrisjmendez.com/2017/08/03/installing-multiple-versions-of-python-on-your-mac-using-homebrew/). For me on `MacOS` they look like this. First install [brew](https://brew.sh/)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
If you have it installed, update it to the latest
```
brew update
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