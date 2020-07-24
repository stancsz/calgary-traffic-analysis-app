# How to run this program

Our project is a flask app. The main program is located at:

```
app/main.py
```


```
python3.8 /home/stan/ensf/calgary-traffic-analysis-app/app/main.py
```
# Dependencies
```
pandas==0.25.3
numpy==1.19.0
dash==1.13.4
dash_bootstrap_components==0.10.3
dash_core_components==1.10.1
dash_html_components==1.0.3
dash_table==4.8.1
folium==0.11.0
geojson==2.5.0
matplotlib==3.3.0
plotly==4.9.0
pymongo==3.10.1
```


# Setup
Install runtime requirements
```shell script
pip install -r requirements.txt
```
Install MongoDb
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y mongodb-org
```

Start MongoDb
```
sudo systemctl start mongod
```
make sure mongo db is running
```
sudo systemctl status mongod
```



# Other tools
Pyenv
```
# Get pyenv
curl https://pyenv.run | bash

# Get a list a avaliable python
pyenv install -l

# install a specific version
pyenv install 3.8.5

# Use Pyenv
eval "$(pyenv init -)"
pyenv versions
pyenv shell 3.8.5
python --version
virtualenv venv3.8.5
``` 

