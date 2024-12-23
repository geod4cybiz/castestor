## Minimal CAS v2.0 demo server

This application is only a demontration, for education purpose, of a possible implementation of a CAS Server.
It is only limited to login, logout and serviceValidate enpoints of the CAS protocol
[https://jasigcas.readthedocs.io/en/latest/cas-server-documentation/protocol/CAS-Protocol-Specification.html]

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

To test the CAS protocol flow call http://locahost:5000/cas/login
See also tests/cas.py



