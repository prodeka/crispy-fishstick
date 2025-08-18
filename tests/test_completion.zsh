# Zsh completion pour LCPI-CLI
# Source: lcpi completion --shell zsh

_lcpi() {
    local curcontext="$curcontext" state line
    typeset -A opt_args
    
    _arguments -C \
        ':command:->command' \
        '*:: :->args'
    
    case "$state" in
        command)
            local -a commands
            commands=(
                'init:Initialiser un projet'
                'doctor:Vérifier l'installation'
                'completion:Générer la complétion'
                'shell:Mode interactif'
                'plugins:Gérer les plugins'
                'aep:Commandes AEP'
                'cm:Commandes CM'
                'bois:Commandes BOIS'
                'beton:Commandes BETON'
                'hydro:Commandes HYDRO'
                'reporting:Générer des rapports'
                'project:Gérer les projets'
            )
            _describe -t commands 'lcpi commands' commands
            ;;
        args)
            case $line[1] in
                aep)
                    local -a aep_commands
                    aep_commands=(
                        'population-unified:Calcul de population'
                        'demand-unified:Calcul de demande'
                        'network-unified:Dimensionnement réseau'
                        'reservoir-unified:Dimensionnement réservoir'
                        'pompage-unified:Dimensionnement pompage'
                        'network-optimize-unified:Optimisation réseau'
                        'network-analyze-scenarios:Analyse de scénarios'
                        'help:Aide AEP'
                    )
                    _describe -t aep_commands 'aep commands' aep_commands
                    ;;
                project)
                    local -a project_commands
                    project_commands=(
                        'init:Initialiser un projet'
                        'list:Lister les projets'
                        'switch:Changer de projet'
                        'cd:Aller au projet'
                        'remove:Supprimer un projet'
                        'archive:Archiver un projet'
                        'sandbox:Mode sandbox'
                        'status:Statut du projet'
                    )
                    _describe -t project_commands 'project commands' project_commands
                    ;;
            esac
            ;;
    esac
}

compdef _lcpi lcpi
