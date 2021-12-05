export ZSH="/root/.oh-my-zsh"
export PATH="$HOME/.poetry/bin:$PATH"

fpath+=~/.zfunc

autoload -U compinit
compinit

ZSH_THEME="cloud"
source $ZSH/oh-my-zsh.sh