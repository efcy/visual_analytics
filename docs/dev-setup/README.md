# Dev Setup
In order to setup everything correctly you need to set up a bunch of environment variables before you can run the backend, database, frontend or the logcrawler

## Setup direnv
https://direnv.net/

```bash
sudo apt install direnv
```

Add this to the .bashrc file
```bash
eval "$(direnv hook bash)"
```

you need to run `direnv allow` in every folder you have an .envrc file

https://direnv.net/man/direnv.toml.1.html#whitelist
https://www.digitalocean.com/community/tutorials/how-to-manage-python-with-pyenv-and-direnv