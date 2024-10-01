## Setup Node.js
We currently use node.js 18.
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt-get install -y nodejs
```

In the web folder run:
```bash
npm install
npm run dev
```