// Configuration de l'API
const API_BASE_URL = window.location.origin;

// Classe principale de l'application
class NanostructApp {
    constructor() {
        this.initializeEventListeners();
        this.checkApiHealth();
    }

    // Initialisation des écouteurs d'événements
    initializeEventListeners() {
        // Formulaire Assainissement
        const assainissementForm = document.getElementById('assainissement-form');
        if (assainissementForm) {
            assainissementForm.addEventListener('submit', (e) => this.handleAssainissementSubmit(e));
        }

        // Formulaires Béton Armé
        const poteauForm = document.getElementById('poteau-form');
        if (poteauForm) {
            poteauForm.addEventListener('submit', (e) => this.handlePoteauBASubmit(e));
        }

        const poutreForm = document.getElementById('poutre-form');
        if (poutreForm) {
            poutreForm.addEventListener('submit', (e) => this.handlePoutreBASubmit(e));
        }

        // Formulaires Bois
        const poteauBoisForm = document.getElementById('poteau-bois-form');
        if (poteauBoisForm) {
            poteauBoisForm.addEventListener('submit', (e) => this.handlePoteauBoisSubmit(e));
        }

        const poutreBoisForm = document.getElementById('poutre-bois-form');
        if (poutreBoisForm) {
            poutreBoisForm.addEventListener('submit', (e) => this.handlePoutreBoisSubmit(e));
        }

        // Validation des formulaires
        this.initializeFormValidation();
    }

    // Vérification de la santé de l'API
    async checkApiHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                console.log('✅ API Nanostruct opérationnelle');
                this.showNotification('API connectée avec succès', 'success');
            }
        } catch (error) {
            console.error('❌ Erreur de connexion à l\'API:', error);
            this.showNotification('Erreur de connexion à l\'API', 'error');
        }
    }

    // Gestion du formulaire Assainissement
    async handleAssainissementSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const formData = new FormData(form);
        const data = {
            surface: parseFloat(formData.get('surface')),
            coefficient_ruissellement: parseFloat(formData.get('coefficient_ruissellement')),
            intensite_pluie: parseFloat(formData.get('intensite_pluie'))
        };

        await this.performCalculation('/api/assainissement/calcul', data, 'assainissement-results');
    }

    // Gestion du formulaire Poteau Béton Armé
    async handlePoteauBASubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const formData = new FormData(form);
        const data = {
            hauteur: parseFloat(formData.get('hauteur')),
            section: parseFloat(formData.get('section')),
            charge_axiale: parseFloat(formData.get('charge_axiale')),
            resistance_beton: parseFloat(formData.get('resistance_beton'))
        };

        await this.performCalculation('/api/beton_arme/poteau', data, 'beton-arme-results');
    }

    // Gestion du formulaire Poutre Béton Armé
    async handlePoutreBASubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const formData = new FormData(form);
        const data = {
            portee: parseFloat(formData.get('portee')),
            largeur: parseFloat(formData.get('largeur')),
            hauteur: parseFloat(formData.get('hauteur')),
            charge_uniforme: parseFloat(formData.get('charge_uniforme'))
        };

        await this.performCalculation('/api/beton_arme/poutre', data, 'beton-arme-results');
    }

    // Gestion du formulaire Poteau Bois
    async handlePoteauBoisSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const formData = new FormData(form);
        const data = {
            hauteur: parseFloat(formData.get('hauteur')),
            section: parseFloat(formData.get('section')),
            charge_axiale: parseFloat(formData.get('charge_axiale')),
            classe_bois: formData.get('classe_bois')
        };

        await this.performCalculation('/api/bois/poteau', data, 'bois-results');
    }

    // Gestion du formulaire Poutre Bois
    async handlePoutreBoisSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const formData = new FormData(form);
        const data = {
            portee: parseFloat(formData.get('portee')),
            largeur: parseFloat(formData.get('largeur')),
            hauteur: parseFloat(formData.get('hauteur')),
            charge_uniforme: parseFloat(formData.get('charge_uniforme')),
            classe_bois: formData.get('classe_bois')
        };

        await this.performCalculation('/api/bois/poutre', data, 'bois-results');
    }

    // Validation des formulaires
    validateForm(form) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
            return false;
        }
        return true;
    }

    // Initialisation de la validation des formulaires
    initializeFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    // Exécution d'un calcul via l'API
    async performCalculation(endpoint, data, resultsContainerId) {
        const resultsContainer = document.getElementById(resultsContainerId);
        const submitButton = event.target.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;

        try {
            // Afficher le spinner
            submitButton.innerHTML = '<span class="spinner me-2"></span>Calcul en cours...';
            submitButton.disabled = true;

            // Appel à l'API
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(resultsContainer, result.resultat, result.message);
                this.showNotification(result.message, 'success');
            } else {
                this.displayError(resultsContainer, result.error || 'Erreur lors du calcul');
                this.showNotification(result.error || 'Erreur lors du calcul', 'error');
            }

        } catch (error) {
            console.error('Erreur API:', error);
            this.displayError(resultsContainer, 'Erreur de connexion à l\'API');
            this.showNotification('Erreur de connexion à l\'API', 'error');
        } finally {
            // Restaurer le bouton
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    // Affichage des résultats
    displayResults(container, results, message) {
        container.innerHTML = `
            <div class="result-item success fade-in">
                <h5 class="text-success mb-3">
                    <i class="fas fa-check-circle me-2"></i>${message}
                </h5>
                ${this.formatResults(results)}
            </div>
        `;
    }

    // Affichage des erreurs
    displayError(container, error) {
        container.innerHTML = `
            <div class="result-item error fade-in">
                <h5 class="text-danger mb-3">
                    <i class="fas fa-exclamation-triangle me-2"></i>Erreur
                </h5>
                <p class="text-danger mb-0">${error}</p>
            </div>
        `;
    }

    // Formatage des résultats
    formatResults(results) {
        if (typeof results === 'object') {
            let html = '<div class="row">';
            for (const [key, value] of Object.entries(results)) {
                const formattedKey = this.formatKey(key);
                const formattedValue = this.formatValue(value);
                html += `
                    <div class="col-md-6 mb-2">
                        <strong>${formattedKey}:</strong>
                        <span class="badge bg-primary ms-2">${formattedValue}</span>
                    </div>
                `;
            }
            html += '</div>';
            return html;
        } else {
            return `<p class="mb-0"><strong>Résultat:</strong> <span class="badge bg-primary">${results}</span></p>`;
        }
    }

    // Formatage des clés
    formatKey(key) {
        const keyMap = {
            'debit': 'Débit',
            'diametre': 'Diamètre',
            'pente': 'Pente',
            'vitesse': 'Vitesse',
            'moment_flechissant': 'Moment fléchissant',
            'effort_tranchant': 'Effort tranchant',
            'contrainte': 'Contrainte',
            'armature': 'Armature',
            'section_armature': 'Section d\'armature',
            'resistance': 'Résistance',
            'verification': 'Vérification'
        };
        return keyMap[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    // Formatage des valeurs
    formatValue(value) {
        if (typeof value === 'number') {
            return value.toFixed(3);
        }
        return value;
    }

    // Affichage des notifications
    showNotification(message, type = 'info') {
        // Créer la notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Ajouter à la page
        document.body.appendChild(notification);

        // Supprimer automatiquement après 5 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialisation de l'application quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    new NanostructApp();
});

// Fonction utilitaire pour les requêtes API
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

// Fonction pour charger les données de référence
async function loadReferenceData() {
    try {
        const [coefficients, classesBeton, classesBois] = await Promise.all([
            apiRequest('/api/assainissement/coefficients'),
            apiRequest('/api/beton_arme/classes'),
            apiRequest('/api/bois/classes')
        ]);

        console.log('Données de référence chargées:', {
            coefficients,
            classesBeton,
            classesBois
        });
    } catch (error) {
        console.error('Erreur lors du chargement des données de référence:', error);
    }
}

// Charger les données de référence au démarrage
loadReferenceData(); 