# BerlinUnited Visual Analytics

The goal of of this tool is to make it possible to quickly view, annotate and analyze all of our RoboCup data. This tool is inspired by V7Labs Darwin Tool but we will also add a lot of other features to it as well.
Access to the V7 tool for inspiration can be given on request.


### Old
Labelstudio Implementation for RoboCup SPL Data

start backend and frontend locally:
```bash
python manage.py runserver
```


```

Now roughly following: https://www.youtube.com/watch?v=c-QsfbznSXI&t=1s
- this uses jwt instead of token based auth -> see where problems might be later on

created the web folder like this:
npm create vite@latest web -- --template react

installed node with whatever version ubuntu 22.04 could install 

testing frontend with
npm run dev


Notes:
- all the routes should be viewable by logged in users, maybe?
    - not sure how we can restrict it to more fine grained selection of users