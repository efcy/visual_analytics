# Berlin United Visual Analytics Tool
The goal of of this tool is to make it possible to quickly view, annotate and analyze all of our RoboCup data. 

## Overview

This repo contains the django backend code in backend/

This repository contains the code for the frontend and backend to run the Tool.
We also included the source code for the sdk and a bunch of utility scripts where some of them
already use the sdk.

## Frontend
Our frontend, which is located in web/, is based on React.
We set up the project using vite and utilize tailwind.css.
Some of our component are from shadcn-ui.

## Backend
In our backend, which is located in backend/, we use django.
We don't utilize the rendering functionality of Django but the 
Django Rest Framework to serve API requests.

## Deployment
Our deployment requieres a k8s platform.
The manifest are located in deployment/.
We use argocd to roll out these manifests.

**WIP**
More about deployment  [deployment](docs/deployment.md) 

## Pipelines
We utilized github actions to 
update our docker images automatically after changes and
update our SDK.

## SDK
Our SDK will be published to pypi: https://pypi.org/project/vaapi/

## Development Setup
Guide on how to setup the development enviroment: [dev setup](docs/dev-setup.md)

## Usage
Check out [usage](docs/usage.md)


