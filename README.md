### Context
* Created: July 2021
* Author: Renier Kramer, renier.kramer@hdsr.nl
* Python version: 3.7

### Description
MWM: edit .xml:
- edit event field 'comment' was used for a link to .jpg as MWM-app did not facilitate comments, but does now. So change it to comment=""
- add event field 'flagsource': flagsource="UR" --> points to template so FEWS can show peilschaal .jpg
MWM .xml orig:
``
<?xml version="1.0" ?>
<TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
	<series>
		<header>
			<type>instantaneous</type>
			<locationId>PS1045</locationId>
			<parameterId>h</parameterId>
			<qualifierId>mcc</qualifierId>
			<timeStep unit="nonequidistant" />
			<startDate date="2016-10-17" time="08:31:44" />
			<endDate date="2016-10-17" time="08:31:44" />
			<missVal>NaN</missVal>
			<sourceOrganisation>Mobile Water Management</sourceOrganisation>
			<sourceSystem>DEV</sourceSystem>
			<creationDate>2016-10-17</creationDate>
			<creationTime>08:36:42</creationTime>
		</header>
		<event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2016-10/20161017083144_HDSR_PS1045_Waterlevel.jpg" date="2016-10-17" flag="3" time="08:31:44" value="-0.090" />
	</series>
</TimeSeries>
```
MWM .xml new:
```
<?xml version='1.0' encoding='UTF-8'?>
<TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
	<series>
		<header>
			<type>instantaneous</type>
			<locationId>PS1045</locationId>
			<parameterId>h</parameterId>
			<qualifierId>mcc</qualifierId>
			<timeStep unit="nonequidistant" />
			<startDate date="2016-10-17" time="08:31:44" />
			<endDate date="2016-10-17" time="08:31:44" />
			<missVal>NaN</missVal>
			<sourceOrganisation>Mobile Water Management</sourceOrganisation>
			<sourceSystem>DEV</sourceSystem>
			<creationDate>2016-10-17</creationDate>
			<creationTime>08:36:42</creationTime>
		</header>
		<event comment="" date="2016-10-17" flag="3" flagsource="UR" time="08:31:44" value="-0.090" />
	</series>
</TimeSeries>
```

### Usage
1. build conda environment from file if you don't have environment already
```
> conda env create --name xml_editor --file <path_to_project>/environment.yml
```
2. run project:
```
> conda activate xml_editor
> python <path_to_project>/main.py
```

### License 
[MIT][mit]

[mit]: https://github.com/hdsr-mid/xml_editor/blob/main/LICENSE.txt

### Releases
None

### Contributions
All contributions, bug reports, bug fixes, documentation improvements, enhancements 
and ideas are welcome on https://github.com/hdsr-mid/xml_editor/issues

### Test Coverage 
Project holds no tests
```
---------- coverage: platform win32, python 3.7.12-final-0 -----
Name                   Stmts   Miss  Cover
------------------------------------------
editors\constants.py       6      0   100%
editors\mwm_xmls.py       64     14    78%
editors\utils.py           7      0   100%
main.py                   18     18     0%
------------------------------------------
TOTAL                     95     32    66%
```

### Conda general tips
#### Build conda environment (on Windows) from any directory using environment.yml:
```
> conda env create --name <conda_env_name> --file <path_to_project>/environment.yml python=<python_version>
> conda info --envs  # verify that <conda_env_name> is in this list 
```
#### Start the application from any directory:
```
> conda activate <conda_env_name>
At any location:
> (<conda_env_name>) python <path_to_project>/main.py
```
#### Test the application:
```
> conda activate <conda_env_name>
> cd <path_to_project>
> pytest  # make sure pytest is installed (conda install pytest)
```
#### List all conda environments on your machine:
```
At any location:
> conda info --envs
```
#### Delete a conda environment:
```
Get directory where environment is located 
> conda info --envs
Remove the enviroment
> conda env remove --name <conda_env_name>
Finally, remove the left-over directory by hand
```
#### Write dependencies to environment.yml:
The goal is to keep the .yml as short as possible (not include sub-dependencies), yet make the environment 
reproducible. Why? If you do 'conda install matplotlib' you also install sub-dependencies like pyqt, qt 
icu, and sip. You should not include these sub-dependencies in your .yml as:
- including sub-dependencies result in an unnecessary strict environment (difficult to solve when conflicting)
- sub-dependencies will be installed when dependencies are being installed
```
> conda activate <conda_env_name>

Recommended:
> conda env export --from-history --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml   

Alternative:
> conda env export --no-builds | findstr -v "prefix" > --file <path_to_project>/environment_new.yml 

--from-history: 
    Only include packages that you have explicitly asked for, as opposed to including every package in the 
    environment. This flag works regardless how you created the environment (through CMD or Anaconda Navigator).
--no-builds:
    By default, the YAML includes platform-specific build constraints. If you transfer across platforms (e.g. 
    win32 to 64) omit the build info with '--no-builds'.
```
#### Pip and Conda:
If a package is not available on all conda channels, but available as pip package, one can install pip as a dependency.
Note that mixing packages from conda and pip is always a potential problem: conda calls pip, but pip does not know 
how to satisfy missing dependencies with packages from Anaconda repositories. 
```
> conda activate <conda_env_name>
> conda install pip
> pip install <pip_package>
```
The environment.yml might look like:
```
channels:
  - defaults
dependencies:
  - <a conda package>=<version>
  - pip
  - pip:
    - <a pip package>==<version>
```
You can also write a requirements.txt file:
```
> pip list --format=freeze > <path_to_project>/requirements.txt
```
