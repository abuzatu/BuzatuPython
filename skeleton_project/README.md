# General

Created by Adrian Buzatu on 03 Dec 2020, as a skeleton of a python ML project, to be used as a template and save time when setting up new projects.


# Set up the Python environment the first time

Install `virtualenv`, if you do not have it already.
```
pip3 install virtualenv
```

Create a virtual environment
```
virtualenv env_skeleton_project
```

Activate the environment
```
source env_skeleton_project/bin/activate
```

Install the basic packages python packages needed for this project
```
pip install -r requirements.txt
```

When a new package is not here, install it with
```
pip install jupyter
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install sklearn
```

After you finished installing all the new packages, save the current environment status to a `requirements.txt` file with
```
pip freeze > requirements.txt
```
# How to set up after the first time

For all the other times, simply go to the folder and activate the python environment
```
cd env_skeleton_project
source env_skeleton_project/bin/activate
```

# Structure

There are three types of files:

* `.py` util files (helper files) with the common functions to be used in .py and .ipynb
* `.py` files that use the helper functions from the utils
* `.ipynb` files Jupyter Notebook files that also use the helper functions from the utils

There are several folders:

* input folder, empty, to add later data
* output folder, empty, to add later plots, result files

# Run the files

Run the regular `.py` with
```
python skeleton.py
```

Run the Jupyter Notebook
```
jupyter skeleton.ipynb
Kernel -> Restart & Clear Output
Kernel -> Restart & Run All
```
