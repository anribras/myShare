### Backends Debug
In root path,run
```
export FLASK_APP=./backends/app.py
python -m flask run
```
### DB Migration
Check db commands:
```
export FLASK_APP=./backends/app.py
python -m flask db init 
python -m flask db migrate
python -m flask db upgrade
```
