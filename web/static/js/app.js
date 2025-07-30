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
        // Assainissement Module Tabs and Forms
        const assainissementFormBatch = document.getElementById('assainissement-form-batch');
        const assainissementFormSingle = document.getElementById('assainissement-form-single');

        // Always try to attach event listeners if forms exist on the page
        if (assainissementFormBatch) {
            assainissementFormBatch.addEventListener('submit', (e) => this.handleAssainissementBatchSubmit(e));

            // Add event listener for methode_calcul to show/hide tc_formule
            const methodeCalculSelectBatch = document.getElementById('assainissement-methode-calcul');
            const tcFormuleGroupBatch = document.getElementById('tc-formule-group');

            if (methodeCalculSelectBatch && tcFormuleGroupBatch) {
                methodeCalculSelectBatch.addEventListener('change', () => {
                    if (methodeCalculSelectBatch.value === 'rationnelle') {
                        tcFormuleGroupBatch.style.display = 'block';
                    } else {
                        tcFormuleGroupBatch.style.display = 'none';
                    }
                });
                // Set initial state
                if (methodeCalculSelectBatch.value !== 'rationnelle') {
                    tcFormuleGroupBatch.style.display = 'none';
                }
            }

            // CSV file input and delimiter handling for batch form
            const csvFileInput = document.getElementById('assainissement-csv-file');
            const delimiterSelect = document.getElementById('assainissement-delimiter');
            const customDelimiterGroup = document.getElementById('custom-delimiter-group');
            const customDelimiterInput = document.getElementById('assainissement-custom-delimiter');

            if (csvFileInput && delimiterSelect) {
                csvFileInput.addEventListener('change', () => this.readAndPreviewCsv());
                delimiterSelect.addEventListener('change', () => {
                    if (delimiterSelect.value === 'other') {
                        customDelimiterGroup.style.display = 'block';
                    } else {
                        customDelimiterGroup.style.display = 'none';
                    }
                    this.readAndPreviewCsv(); // Re-read with new delimiter
                });
                customDelimiterInput.addEventListener('input', () => this.readAndPreviewCsv());
            }

            // Set initial state for custom delimiter group
            if (delimiterSelect && customDelimiterGroup) {
                if (delimiterSelect.value !== 'other') {
                    customDelimiterGroup.style.display = 'none';
                }
            }
        }

        if (assainissementFormSingle) {
            assainissementFormSingle.addEventListener('submit', (e) => this.handleAssainissementSingleSubmit(e));

            // Add event listener for methode_calcul to show/hide tc_formule for single troncon
            const singleMethodeCalculSelect = document.getElementById('single-methode-calcul');
            const singleTcFormuleGroup = document.getElementById('single-tc-formule-group');

            if (singleMethodeCalculSelect && singleTcFormuleGroup) {
                singleMethodeCalculSelect.addEventListener('change', () => {
                    if (singleMethodeCalculSelect.value === 'rationnelle') {
                        singleTcFormuleGroup.style.display = 'block';
                    } else {
                        singleTcFormuleGroup.style.display = 'none';
                    }
                });
                // Set initial state
                if (singleMethodeCalculSelect.value !== 'rationnelle') {
                    singleTcFormuleGroup.style.display = 'none';
                }
            }
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

    // Read and preview CSV file
    async readAndPreviewCsv() {
        const csvFileInput = document.getElementById('assainissement-csv-file');
        const csvPreviewSection = document.getElementById('csv-preview-section');
        const csvPreviewTable = document.getElementById('csv-preview-table');
        const delimiterSelect = document.getElementById('assainissement-delimiter');
        const customDelimiterInput = document.getElementById('assainissement-custom-delimiter');

        if (!csvFileInput || !csvFileInput.files || csvFileInput.files.length === 0) {
            csvPreviewSection.style.display = 'none';
            return;
        }

        const file = csvFileInput.files[0];
        let delimiter = delimiterSelect.value;
        if (delimiter === 'other') {
            delimiter = customDelimiterInput.value;
        }
        if (delimiter === '\t') delimiter = '\t'; // Handle tab character

        if (!delimiter) {
            csvPreviewSection.style.display = 'none';
            return;
        }

        try {
            const csvContent = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = (e) => resolve(e.target.result);
                reader.onerror = (e) => reject(e);
                reader.readAsText(file);
            });

            const lines = csvContent.split(/\r\n|\n/).filter(line => line.trim() !== '');
            if (lines.length === 0) {
                csvPreviewTable.innerHTML = '<p class="text-muted">Fichier CSV vide.</p>';
                csvPreviewSection.style.display = 'block';
                return;
            }

            const headers = lines[0].split(delimiter).map(h => h.trim());
            let tableHtml = '<thead><tr>';
            headers.forEach(header => {
                tableHtml += `<th>${header}</th>`;
            });
            tableHtml += '</tr></thead><tbody>';

            lines.slice(1).forEach(line => {
                const values = line.split(delimiter).map(v => v.trim());
                tableHtml += '<tr>';
                values.forEach(value => {
                    tableHtml += `<td>${value}</td>`;
                });
                tableHtml += '</tr>';
            });
            tableHtml += '</tbody>';

            csvPreviewTable.innerHTML = tableHtml;
            csvPreviewSection.style.display = 'block';

        } catch (error) {
            console.error('Erreur lors de la lecture ou de l\'analyse du CSV:', error);
            csvPreviewTable.innerHTML = '<p class="text-danger">Erreur lors de la lecture ou de l\'analyse du fichier CSV.</p>';
            csvPreviewSection.style.display = 'block';
        }
    }

    // Gestion du formulaire Assainissement (Batch Mode)
    async handleAssainissementBatchSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const csvFileInput = document.getElementById('assainissement-csv-file');
        if (!csvFileInput || !csvFileInput.files || csvFileInput.files.length === 0) {
            this.showNotification('Veuillez charger un fichier CSV de tronçons.', 'error');
            return;
        }

        const csvFile = csvFileInput.files[0];
        const delimiterSelect = document.getElementById('assainissement-delimiter');
        const customDelimiterInput = document.getElementById('assainissement-custom-delimiter');

        let delimiter = delimiterSelect.value;
        if (delimiter === 'other') {
            delimiter = customDelimiterInput.value;
        }
        if (delimiter === '\t') delimiter = '\t'; // Handle tab character

        if (!delimiter) {
            this.showNotification('Veuillez spécifier un délimiteur CSV.', 'error');
            return;
        }

        const formData = new FormData(form);
        const methode_calcul = formData.get('methode_calcul');
        const tc_formule_name = methode_calcul === 'rationnelle' ? formData.get('tc_formule') : 'kirpich';
        const v_min = parseFloat(formData.get('v_min'));
        const v_max = parseFloat(formData.get('v_max'));
        const idf_a = parseFloat(formData.get('idf_a'));
        const idf_b = parseFloat(formData.get('idf_b'));
        const periode_retour = parseInt(formData.get('periode_retour'));
        const verbose = formData.get('verbose') === 'on';

        const params_pluie = {
            "formula": "montana",
            "periode_retour": periode_retour,
            "nom": `Manuel T=${periode_retour} ans`,
            "a": idf_a,
            "b": idf_b
        };

        // Create FormData object for multipart/form-data
        const dataToSend = new FormData();
        dataToSend.append('csv_file', csvFile);
        dataToSend.append('delimiter', delimiter);
        dataToSend.append('methode_calcul', methode_calcul);
        dataToSend.append('tc_formule_name', tc_formule_name);
        dataToSend.append('v_min', v_min);
        dataToSend.append('v_max', v_max);
        dataToSend.append('idf_a', idf_a);
        dataToSend.append('idf_b', idf_b);
        dataToSend.append('periode_retour', periode_retour);
        dataToSend.append('verbose', verbose);

        await this.performCalculation('/api/assainissement/calcul_complet', dataToSend, 'assainissement-results', submitButton, true); // Pass true for isFormData
    }

    // Gestion du formulaire Assainissement (Single Troncon Mode)
    async handleAssainissementSingleSubmit(event) {
        event.preventDefault();

        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const formData = new FormData(form);
        const methode_calcul = formData.get('methode_calcul');
        const tc_formule_name = methode_calcul === 'rationnelle' ? formData.get('tc_formule') : 'kirpich';
        const v_min = parseFloat(formData.get('v_min'));
        const v_max = parseFloat(formData.get('v_max'));
        const idf_a = parseFloat(formData.get('idf_a'));
        const idf_b = parseFloat(formData.get('idf_b'));
        const periode_retour = parseInt(formData.get('periode_retour'));
        const verbose = formData.get('verbose') === 'on';

        const params_pluie = {
            "formula": "montana",
            "periode_retour": periode_retour,
            "nom": `Manuel T=${periode_retour} ans`,
            "a": idf_a,
            "b": idf_b
        };

        // Collect single troncon data
        const troncon_data = {
            id_troncon: formData.get('id_troncon'),
            type_section: formData.get('type_section'),
            largeur_fond_m: parseFloat(formData.get('largeur_fond_m')),
            fruit_z: parseFloat(formData.get('fruit_z')),
            surface_ha: parseFloat(formData.get('surface_ha')),
            coeff_ruissellement: parseFloat(formData.get('coeff_ruissellement')),
            longueur_parcours_surface_m: parseFloat(formData.get('longueur_parcours_surface_m')),
            pente_parcours_surface: parseFloat(formData.get('pente_parcours_surface')),
            longueur_troncon_m: parseFloat(formData.get('longueur_troncon_m')),
            pente_troncon: parseFloat(formData.get('pente_troncon')),
            ks_manning_strickler: parseFloat(formData.get('ks_manning_strickler')),
            troncon_amont: formData.get('troncon_amont'),
            z_start: parseFloat(formData.get('z_start')),
            z_end: parseFloat(formData.get('z_end'))
        };

        const payload = {
            troncons_data: [troncon_data], // Send as an array with one troncon
            methode_calcul: methode_calcul,
            tc_formule_name: tc_formule_name,
            params_pluie: params_pluie,
            v_min: v_min,
            v_max: v_max,
            verbose: verbose
        };

        await this.performCalculation('/api/assainissement/calcul_complet', payload, 'assainissement-results', submitButton);
    }

    // Gestion du formulaire Poteau Béton Armé
    async handlePoteauBASubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const formData = new FormData(form);
        const data = {
            b: parseFloat(formData.get('b')),
            h: parseFloat(formData.get('h')),
            height: parseFloat(formData.get('height')),
            Nu: parseFloat(formData.get('Nu')),
            Mu: parseFloat(formData.get('Mu')),
            fc28: parseFloat(formData.get('fc28')),
            fe: parseFloat(formData.get('fe')),
            k_factor: parseFloat(formData.get('k_factor'))
        };

        await this.performCalculation('/api/beton_arme/poteau', data, 'beton-arme-results', submitButton);
    }

    // Gestion du formulaire Poutre Béton Armé
    async handlePoutreBASubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const formData = new FormData(form);
        const data = {
            portee: parseFloat(formData.get('portee')),
            largeur: parseFloat(formData.get('largeur')),
            hauteur: parseFloat(formData.get('hauteur')),
            charge_uniforme: parseFloat(formData.get('charge_uniforme')),
            resistance_beton: parseFloat(formData.get('resistance_beton')),
            resistance_acier: parseFloat(formData.get('resistance_acier'))
        };

        await this.performCalculation('/api/beton_arme/poutre', data, 'beton-arme-results', submitButton);
    }

    // Gestion du formulaire Poteau Bois
    async handlePoteauBoisSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const formData = new FormData(form);
        const data = {
            b: parseFloat(formData.get('b')),
            h: parseFloat(formData.get('h')),
            effort_N_daN: parseFloat(formData.get('effort_N_daN')),
            classe_bois: formData.get('classe_bois'),
            classe_service: formData.get('classe_service'),
            duree_charge: formData.get('duree_charge')
        };

        await this.performCalculation('/api/bois/poteau', data, 'bois-results', submitButton);
    }

    // Gestion du formulaire Poutre Bois
    async handlePoutreBoisSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        if (!this.validateForm(form)) return;

        const submitButton = form.querySelector('button[type="submit"]');

        const formData = new FormData(form);
        const data = {
            b: parseFloat(formData.get('b')),
            h: parseFloat(formData.get('h')),
            longueur: parseFloat(formData.get('longueur')),
            charge_G: parseFloat(formData.get('charge_G')),
            charge_Q: parseFloat(formData.get('charge_Q')),
            charge_W: parseFloat(formData.get('charge_W')),
            charge_S: parseFloat(formData.get('charge_S')),
            classe_bois: formData.get('classe_bois'),
            classe_service: formData.get('classe_service'),
            duree_charge: formData.get('duree_charge'),
            categorie_usage: formData.get('categorie_usage')
        };

        await this.performCalculation('/api/bois/poutre', data, 'bois-results', submitButton);
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
    async performCalculation(endpoint, data, resultsContainerId, submitButton, isFormData = false) {
        const resultsContainer = document.getElementById(resultsContainerId);
        const originalText = submitButton.innerHTML;

        try {
            // Afficher le spinner
            submitButton.innerHTML = '<span class="spinner me-2"></span>Lancement du calcul...';
            submitButton.disabled = true;
            resultsContainer.innerHTML = ''; // Clear previous results

            // Appel à l'API
            const fetchOptions = {
                method: 'POST',
            };

            if (isFormData) {
                fetchOptions.body = data; // FormData object
            } else {
                fetchOptions.headers = {
                    'Content-Type': 'application/json',
                };
                fetchOptions.body = JSON.stringify(data);
            }

            const response = await fetch(`${API_BASE_URL}${endpoint}`, fetchOptions);
            const initialResult = await response.json();

            if (response.ok && initialResult.task_id) {
                // Si on reçoit un task_id, c'est un calcul asynchrone (Assainissement)
                this.showNotification(initialResult.message, 'info');
                // On commence à surveiller l'état de la tâche
                await this.pollTaskStatus(initialResult.task_id, resultsContainerId, submitButton, originalText);
            } else if (initialResult.success) {
                // Pour les calculs synchrones (BA, Bois)
                this.displayResults(resultsContainer, initialResult.resultat, initialResult.message, initialResult.verbose_log);
                this.showNotification(initialResult.message, 'success');
                // Restaurer le bouton ici pour les tâches synchrones
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            } else {
                // Gérer les erreurs directes de l'API
                this.displayError(resultsContainer, initialResult.error || 'Erreur lors du calcul');
                this.showNotification(initialResult.error || 'Erreur lors du calcul', 'error');
                // Restaurer le bouton en cas d'erreur
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }

        } catch (error) {
            console.error('Erreur API:', error);
            this.displayError(resultsContainer, 'Erreur de connexion à l\'API');
            this.showNotification('Erreur de connexion à l\'API', 'error');
            // Restaurer le bouton en cas d'erreur
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    // Surveillance de l'état d'une tâche Celery
    async pollTaskStatus(taskId, resultsContainerId, submitButton, originalButtonText) {
        const resultsContainer = document.getElementById(resultsContainerId);
        const maxRetries = 60; // Max 2 minutes (60 * 2000ms)
        let retries = 0;

        const intervalId = setInterval(async () => {
            if (retries >= maxRetries) {
                clearInterval(intervalId);
                this.displayError(resultsContainer, "Le calcul a pris trop de temps à répondre. Veuillez réessayer.");
                this.showNotification("Le calcul a expiré.", "error");
                submitButton.innerHTML = originalButtonText;
                submitButton.disabled = false;
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/calcul/status/${taskId}`);
                const task = await response.json();

                // Mettre à jour le message du bouton
                submitButton.innerHTML = `<span class="spinner me-2"></span>${task.message || 'Calcul en cours...'}`;

                if (task.state === 'SUCCESS') {
                    clearInterval(intervalId);
                    const finalResult = task.result; // Le résultat est dans la propriété 'result' de la tâche
                    this.displayResults(resultsContainer, finalResult.resultat, finalResult.message, finalResult.verbose_log);
                    this.showNotification(finalResult.message, 'success');
                    submitButton.innerHTML = originalButtonText;
                    submitButton.disabled = false;
                } else if (task.state === 'FAILURE') {
                    clearInterval(intervalId);
                    this.displayError(resultsContainer, task.error || 'La tâche a échoué sans message d\'erreur.');
                    this.showNotification(task.message || 'La tâche a échoué', 'error');
                    submitButton.innerHTML = originalButtonText;
                    submitButton.disabled = false;
                }
                // Si PENDING ou PROGRESS, on continue de boucler
            } catch (error) {
                clearInterval(intervalId);
                console.error('Erreur lors de la surveillance de la tâche:', error);
                this.displayError(resultsContainer, 'Erreur de communication avec le serveur pour le statut de la tâche.');
                this.showNotification('Erreur de communication.', 'error');
                submitButton.innerHTML = originalButtonText;
                submitButton.disabled = false;
            }

            retries++;
        }, 2000); // Interroger toutes les 2 secondes
    }

    // Affichage des résultats
    displayResults(container, results, message, verboseLog = null) {
        let htmlContent = `
            <div class="result-item success fade-in">
                <h5 class="text-success mb-3">
                    <i class="fas fa-check-circle me-2"></i>${message}
                </h5>
        `;

        if (Array.isArray(results) && results.length > 0) {
            // Assume results is an array of objects (DataFrame rows)
            htmlContent += '<h6 class="mt-4">Tableau des Résultats:</h6>';
            htmlContent += '<div class="table-responsive"><table class="table table-striped table-sm"><thead><tr>';
            // Get headers from the first object keys
            const headers = Object.keys(results[0]);
            headers.forEach(header => {
                htmlContent += `<th>${header}</th>`;
            });
            htmlContent += '</tr></thead><tbody>';
            results.forEach(row => {
                htmlContent += '<tr>';
                headers.forEach(header => {
                    htmlContent += `<td>${this.formatValue(row[header])}</td>`;
                });
                htmlContent += '</tr>';
            });
            htmlContent += '</tbody></table></div>';
        } else if (typeof results === 'object' && results !== null) {
            // If it's a single object (like for BA/Bois poteau/poutre)
            htmlContent += this.formatResults(results); // Reuse existing formatResults for single object
        } else {
            htmlContent += `<p class="mb-0"><strong>Résultat:</strong> <span class="badge bg-primary">${results}</span></p>`;
        }

        if (verboseLog) {
            htmlContent += `
                <h6 class="mt-4">Log Détaillé:</h6>
                <pre class="bg-light p-3 rounded" style="max-height: 300px; overflow-y: scroll; font-size: 0.85em;"><code>${verboseLog}</code></pre>
            `;
        }

        htmlContent += '</div>'; // Close result-item success fade-in
        container.innerHTML = htmlContent;
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
            'verification': 'Vérification',
            'diametre_retenu_mm': 'Diamètre Retenu (mm)',
            'hauteur_retenue_m': 'Hauteur Retenue (m)',
            'vitesse_ms': 'Vitesse (m/s)',
            'statut': 'Statut',
            'id_troncon': 'ID Tronçon',
            'q_max_m3s': 'Q Max (m³/s)'
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
async function apiRequest(endpoint, method = 'GET', data = null, isFormData = false) {
    const options = {
        method,
    };

    if (isFormData) {
        options.body = data; // FormData object
    } else {
        options.headers = {
            'Content-Type': 'application/json',
        };
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