# Sample .bashrc for SuSE Linux
# Copyright (c) SuSE GmbH Nuernberg

# There are 3 different types of shells in bash: the login shell, normal shell
# and interactive shell. Login shells read ~/.profile and interactive shells
# read ~/.bashrc; in our setup, /etc/profile sources ~/.bashrc - thus all
# settings made here will also take effect in a login shell.
#
# NOTE: It is recommended to make language settings in ~/.profile rather than
# here, since multilingual X sessions would not work properly if LANG is over-
# ridden in every subshell.

# Some applications read the EDITOR variable to determine your favourite text
# editor. So uncomment the line below and enter the editor of your choice :-)
#export EDITOR=/usr/bin/vim
#export EDITOR=/usr/bin/mcedit

# For some news readers it makes sense to specify the NEWSSERVER variable here
#export NEWSSERVER=your.news.server

# If you want to use a Palm device with Linux, uncomment the two lines below.
# For some (older) Palm Pilots, you might need to set a lower baud rate
# e.g. 57600 or 38400; lowest is 9600 (very slow!)
#
#export PILOTPORT=/dev/pilot
#export PILOTRATE=115200

#If fortune exists 
#and running interactively ($PS1, fixes the fail with scp)
#test -s ~/.alias && . ~/.alias || true

if [ -x /usr/bin/fortune ]  && [ "$PS1" ]; then
    echo
    /usr/bin/fortune all -a ru off fr
    echo
fi

shopt -s cdspell
shopt -s autocd
shopt -s globstar
shopt -s extglob
complete -cf sudo

_bgreen="$(tput bold 2> /dev/null; tput setaf 2 2> /dev/null)"
_bblue="$(tput bold 2> /dev/null; tput setaf 4 2> /dev/null)"
_bred="$(tput bold 2> /dev/null; tput setaf 1 2> /dev/null)"
_red="$(tput setaf 1 2> /dev/null)"
_sgr0="$(tput sgr0 2> /dev/null)"
if [[ $UID == 0 ]]; then
    PS1="\[$_bred\]\h:\w#\[$_sgr0\] "
else
    PS1="\[$_bgreen\]\u\$(if [[ \$? == 0 ]]; then echo \"\[$_sgr0\]\"; else echo  \"\[$_red\]\"; fi;)@\[$_bblue\]\h\[$_sgr0\]:\w> "
fi
export TEXMFCONFIG=$HOME/.texmf
export LESS="-R"
export EDITOR=vim
export PATH=$HOME/bin/:$PATH
export HISTCONTROL=ignoredups
#export LANG="ru_RU.UTF-8"

alias св='cd'
alias ды='ls'
alias ьс='mc'
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias l='ls -l'
alias ll='ls -la'
alias md='mkdir'
alias gcc='gcc -fdiagnostics-color=auto'
alias g++='g++ -fdiagnostics-color=auto'
alias fuck='$(thefuck $(fc -ln -1))'
