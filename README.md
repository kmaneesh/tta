# tta

## Launch
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kmaneesh/tta/master)

## Description
Trade Transparency Analysis provide python interface to access UN Trade Comm Data and analyse in jupyter notebooks.

## About
The project is self contained and run online on https://mybinder.org/ in a browser. To run the project click on the
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kmaneesh/tta/master) icon.


## Data
All the data is pulled from the UN Com Trade (https://comtrade.un.org/) website in real time and made available for analysis.
The public api has rate limit of 1 request per second and 100 request per hours.
In case a user exceed the rate limit the data will not be retrived.

## Organisation
The project is organised in folders. The folder comtrade contains the python classes to access the comtrade api.
The folder web contains the python classes for accessing the country specific public data.
The folder notebook contains the jupyter notebook which actually runs the analysis.
Inside the notebook folder there are country specific folder which further branch into partner country folder.
Inside the partner country folder there is three notebook: compare, export and import.

## Compare
The compare notebook provides the comparison of export and import figure reported (TOTAL) month wise to give a
over all picture of trade.

## Export
The export notebook provide analysis at 2, 4, 6 digit level of the product exported by one country in comparison with data of import of the partner country.

## Import
The import notebook provide analysis at 2, 4, 6 digit level of the product imported by one country in comparison with data of export of the partner country.

## Run
* Click on Launce Binder Icon [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kmaneesh/tta/master) icon.
* Wait for the image to be build and uploaded. The first time it will take some time then it will be cached.
* Navigate to tta > notebook > in > jp folder ( Or any other notebook inside the tta > notebook.
* Click on the notebook, once notebook is loaded, click Kernel Menu and select Restart and Run All.
* All the analysis will be run and you can see and play with the results if you have basic knowledge of data analysis.



## Local Install
* Install docker on your machine
* Clone the repository
* Navigate to the root folder
* docker-compose build
* docker-compose up
* Copy paste the URL in browser



