FROM mcr.microsoft.com/vscode/devcontainers/python:3.10-bullseye

# Install poetry build system
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install poetry autocompletions in zsh
RUN mkdir /root/.zfunc
COPY /.devcontainer/.zshrc /root/.zshrc
RUN poetry completions zsh > ~/.zfunc/_poetry
