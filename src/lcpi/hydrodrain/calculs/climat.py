import matplotlib.pyplot as plt
import os

def generer_diagramme_ombrothermique(donnees: dict, output_path: str) -> dict:
    donnees_mensuelles = donnees.get("donnees_mensuelles")
    station = donnees.get("station", "Station Inconnue")
    
    mois = [d['mois'] for d in donnees_mensuelles]
    temps = [d['temp_C'] for d in donnees_mensuelles]
    precip = [d['precip_mm'] for d in donnees_mensuelles]
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    ax1.bar(mois, precip, color='cyan', label='Précipitations (mm)')
    ax1.set_ylabel('Précipitations (mm)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax2 = ax1.twinx()
    ax2.plot(mois, temps, color='red', marker='o', linestyle='--', label='Températures (°C)')
    ax2.set_ylabel('Températures (°C)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    ax1.set_ylim(0, max(precip) * 1.1)
    ax2.set_ylim(0, max(precip) * 1.1 / 2)

    mois_secs = [m for m, p, t in zip(mois, precip, temps) if p < 2 * t]
    
    plt.title(f"Diagramme Ombrothermique de Gaussen - {station}")
    fig.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Crée le répertoire de sortie s'il n'existe pas
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"INFO: Le répertoire de sortie '{output_dir}' n'existe pas, création...")
        os.makedirs(output_dir)
    
    plt.savefig(output_path)
    plt.close()
    
    t_max = max(temps)
    t_min = min(temps)
    amplitude = t_max - t_min
    
    return {
        "statut": "OK",
        "fichier_genere": output_path,
        "mois_secs_identifies": mois_secs,
        "amplitude_thermique_C": round(amplitude, 1)
    }
