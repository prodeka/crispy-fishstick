# Bash completion pour LCPI-CLI
# Source: lcpi completion --shell bash

_lcpi_completion() {
    local cur prev opts cmds
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Commandes principales
    cmds="init doctor completion shell plugins aep cm bois beton hydro reporting project"
    
    # Sous-commandes AEP
    if [[ ${prev} == "aep" ]]; then
        opts="population-unified demand-unified network-unified reservoir-unified pumping-unified network-optimize-unified network-analyze-scenarios help"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Sous-commandes project
    if [[ ${prev} == "project" ]]; then
        opts="init list switch cd remove archive sandbox status"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Complétion des commandes principales
    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${cmds}" -- ${cur}) )
        return 0
    fi
}

complete -F _lcpi_completion lcpi
