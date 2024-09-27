# Berlin United Visual Analytics Tool
The goal of of this tool is to make it possible to quickly view, annotate and analyze all of our RoboCup data. This tool is inspired by V7Labs Darwin Tool but we will also add a lot of other features to it as well.
Access to the V7 tool for inspiration can be given on request.

## Overview

This repo contains the django backend code in backend/

This repository contains the code for the frontend and backend to run the Tool.
We also included the source code for the sdk and a bunch of utility scripts where some of them
already use the sdk.

TODO: mention frontend based on react code in web/
TODO: backend django based
TODO: mention deployment - expects k8s platform - k8s manifests are in deployment/ rolling out of k8s manifests is done via argocd
TODO: mention github pipelines - updaten docker images / sdk


## SDK
Our SDK will be published to pypi: https://pypi.org/project/BU-VAT/

## Development Setup
Guide on how to setup the development enviroment: [dev setup](docs/dev-setup.md)

## Usage
Check out [usage](docs/usage.md)

## Deployment
Learn how to deploy the tool [deployment](docs/deployment.md)


### Old
Labelstudio Implementation for RoboCup SPL Data

start backend and frontend locally:
```bash
python manage.py runserver
```


```



created the web folder like this:
npm create vite@latest web -- --template react

installed node with whatever version ubuntu 22.04 could install 

testing frontend with
npm run dev


Notes:
- all the routes should be viewable by logged in users, maybe?
    - not sure how we can restrict it to more fine grained selection of users
