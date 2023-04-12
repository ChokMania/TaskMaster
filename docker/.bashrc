
# ALIAS

# Git alias
alias gpf="git push --force-with-lease"

# Python alias
alias vactive="source venv/bin/activate"
alias vactiv="source venv/bin/activate"

# Bash alias
alias ls="ls --color -F"
alias ..="cd .."
alias ll="ls -l"
alias la="ls -a"

# Dir alias
alias shareddir='cd /shared'

# END OF ALIAS

# Define some color codes
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_BLUE='\033[0;34m'
COLOR_PURPLE='\033[0;35m'
COLOR_CYAN='\033[0;36m'
COLOR_WHITE='\033[0;37m'
COLOR_RESET='\033[0m'

# Define function to show git branch name in prompt
parse_git_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null | sed 's/^//'
}

# Set the prompt
PS1="${COLOR_GREEN}Container: ${COLOR_WHITE}\u@\h in ${COLOR_YELLOW}\w ${COLOR_CYAN}\$(parse_git_branch)${COLOR_RESET} $ "
