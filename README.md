# RoboCup-Labelstudio
Labelstudio Implementation for RoboCup SPL Data



```

Now roughly following: https://www.youtube.com/watch?v=c-QsfbznSXI&t=1s
- this uses jwt instead of token based auth -> see where problems might be later on

created the web folder like this:
npm create vite@latest web -- --template react

installed node with whatever version ubuntu 22.04 could install 

testing frontend with
npm run dev

npm install react-bootstrap bootstrap

Notes:
- all the routes should be viewable by logged in users, maybe?
    - not sure how we can restrict it to more fine grained selection of users