# Reisi Eestis

1. Clone this repo to your local machine somewhere
2. Create venv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the script:

```bash
flask --app main run --debug
```

It uses a in-memory sqlite database, so you can just run it, and it will create the database for you, for convenience.

Once running, you can access the app at http://127.0.0.1:5000/.