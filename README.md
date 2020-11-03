# covid19-tracker

This is a project for DSDI560 hw5, a local bokeh server application for visualizing covid19 data in California.

## Requirements installation
1. Create a virtual environment.  
```
python3 -m venv dsdi560H5
source ./dsdi560H5/bin/activate 
. ./dsdi560H5/bin/activate 
```
2. Installing requirements from file or one by one.  
```
pip install -r requirements.txt
```
## Bokeh
Use bokeh serve to start the application
```
bokeh serve --show resulting.py
```
## Docker
Firstly build the docker using the Dockerfile.  
```
docker build -t covidtracker .
```
Run the docker image and the bokeh application will run automatically.  
```
docker run --publish 5006:5006 --name ct covidtracker
```
Copy the url into your browser for the visualization.  
http://localhost:5006/resulting  

if using other ports other than 5006(like 5000), need to 'use --allow-websocket-origin=localhost:5000 or set BOKEH_ALLOW_WS_ORIGIN=localhost:5000' 
