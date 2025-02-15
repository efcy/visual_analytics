## Demos for the Berlin United Visual Analytics Tool

## Setup

```bash
python3 -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt
```

You need to the environment variables for the URL and the API token. 
```
export VAT_API_URL=<http://127.0.0.1:8000/ or https://vat.berlin-united.com/>
export VAT_API_TOKEN=<your token>
```

If you are using vat.berlin-united.com you should have received a token from the admin. If you are using the self hosted version you can get the token by login to the django admin panel. 