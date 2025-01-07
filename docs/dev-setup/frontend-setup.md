# Setup Frontend

## Install Node.js

We currently use Node.js 22.x On Ubuntu it can be installed like this:

```bash
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

export NODE_MAJOR=22
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install -y nodejs
```

## Setup Project

This project is meant to be run with VS Code. Please install the recommended VS Code extensions.

Setup and run the frontend locally with:

```bash
npm install # only needs to be run once / or when dependencies change
npm run dev # starts a webserver serving the react frontend
```

We set up prettier and eslint with npm as well to use it in our CI pipelines. Make sure you run `npm run format` and `npm run lint` before creating a merge request.
If you have installed the recommended VS Code extensions as mentioned above all files will be formated on save.

You can update the packages by running:

```bash
npm outdated # shows outdated packages
npm update # actually updates the packages
```

## Browser Plugins

For developing the frontend you might find the react and redux dev tools helpful:

- https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en
- https://chromewebstore.google.com/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en
