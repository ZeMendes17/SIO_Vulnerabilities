# PROJECT 1 SIO

## How to run

Create a virtual environment and install the requirements:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the program:

```bash
export FLASK_APP=__init__.py
export FLASK_DEBUG=1
flask run
```

Run the bash file:

```bash
chmod +x run.sh
./run.sh
```

Generate the example database:

http://127.0.0.1:5000/generate/database

Open the browser and go to http://127.0.0.1:5000/
