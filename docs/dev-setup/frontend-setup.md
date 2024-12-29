# Setup Frontend

This project is meant to be run with VS Code. Please install the recommended VS Code extensions.

Setup and run the frontend locally with:

```bash
npm install # only needs to be run once / or when dependencies change
npm run dev # starts a webserver serving the react frontend
```

We set up prettier and eslint with npm as well to use it in our CI pipelines. Make sure you run `npm run format` and `npm run lint` before creating a merge request.
If you have installed the recommended VS Code extensions as mentioned above all files will be formated on save.

# Old Notes

created the web folder like this:
npm create vite@latest web -- --template react

installed node with whatever version ubuntu 22.04 could install
