## Create  and activate Python virtual environment with powershell (Windows)
```
python3 -m venv .venv

.venv\Scripts\Activate.ps1 
```
## Install required python libraries
```
pip install -r requirements.txt
```

## Save python packages in powershell
```
python -m pip freeze > requirements.txt
```

python main.py