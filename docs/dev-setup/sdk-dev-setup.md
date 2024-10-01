## Install sdk locally
TODO: how to develop the sdk further

In the repo folder install the sdk with
```bash
python -m pip install -e sdk
```
then log in to django admin page on http://localhost:8000/admin/ and get the API Token for use with the sdk. If you plan to use the predefined functions for inserting data you need to expose the API Key as an environment variable:
```bash
export VAT_API_TOKEN=<your api token>
```
### Labelstudio API as Inspiration (how to develop)
https://labelstud.io/sdk/index.html
https://github.com/HumanSignal/label-studio-sdk/tree/release/0.0.34
