## Minimal CAS20 demo server

### requirements
- python 3.10+

### instructions
- generate virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- generate .env
```bash
cp env.sample .env
```
- initialize database
```bash
python app/cas/models.py
```
a single user is created  in the database (email guest@example.com, password justpassingby)

- run
```bash
flask run --debug
```
open your browser on http://localhost:5000/

