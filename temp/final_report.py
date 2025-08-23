import json
from pathlib import Path
import matplotlib.pyplot as plt

def load_json(path):
    with open(path) as f:
        return json.load(f)

print("="*60)
print("📊 RAPPORT COMPARATIF D'OPTIMISATION HYDRAULIQUE")
print("="*60)

# Charger les données
sim_500 = load_json(Path("temp/sim_500.json"))
sim_600 = load_json(Path("temp/sim_600.json"))

# Extraire les propositions
proposal_500 = sim_500.get("proposals", [{}])[0]
proposal_600 = sim_600.get("proposals", [{}])[0]

# Extraire les métadonnées
meta_500 = sim_500.get("meta", {})
meta_600 = sim_600.get("meta", {})

print(f"\n🔍 ANALYSE DES SCÉNARIOS")
print(f"{'='*40}")

print(f"\n📈 SCÉNARIO 1: Demande 500 m³/h")
print(f"   • Coût total (CAPEX): {proposal_500.get('CAPEX', 'N/A'):,.0f} FCFA")
print(f"   • Hauteur réservoir: {proposal_500.get('H_tank_m', 'N/A')} m")
print(f"   • Contraintes respectées: {proposal_500.get('constraints_ok', 'N/A')}")
print(f"   • Violations: {proposal_500.get('constraints_violations', 'N/A')}")

print(f"\n📈 SCÉNARIO 2: Demande 600 m³/h")
print(f"   • Coût total (CAPEX): {proposal_600.get('CAPEX', 'N/A'):,.0f} FCFA")
print(f"   • Hauteur réservoir: {proposal_600.get('H_tank_m', 'N/A')} m")
print(f"   • Contraintes respectées: {proposal_600.get('constraints_ok', 'N/A')}")
print(f"   • Violations: {proposal_600.get('constraints_violations', 'N/A')}")

# Comparaison des coûts
cost_500 = proposal_500.get("CAPEX", 0)
cost_600 = proposal_600.get("CAPEX", 0)

print(f"\n💰 ANALYSE ÉCONOMIQUE")
print(f"{'='*40}")
print(f"   • Différence de coût: {cost_600 - cost_500:,.0f} FCFA")
if cost_500 > 0:
    print(f"   • Pourcentage d'augmentation: {((cost_600 - cost_500) / cost_500 * 100):.1f}%")
else:
    print(f"   • Pourcentage d'augmentation: N/A")

# Comparaison des hauteurs de réservoir
h_500 = proposal_500.get("H_tank_m", 0)
h_600 = proposal_600.get("H_tank_m", 0)

print(f"\n🏗️ ANALYSE TECHNIQUE")
print(f"{'='*40}")
print(f"   • Hauteur réservoir 500 m³/h: {h_500 if h_500 is not None else 'N/A'} m")
print(f"   • Hauteur réservoir 600 m³/h: {h_600 if h_600 is not None else 'N/A'} m")
if h_500 is not None and h_600 is not None:
    print(f"   • Différence de hauteur: {h_600 - h_500:.2f} m")
else:
    print(f"   • Différence de hauteur: N/A")

# Analyser les diamètres
diameters_500 = proposal_500.get("diameters_mm", {})
diameters_600 = proposal_600.get("diameters_mm", {})

if diameters_500 and diameters_600:
    print(f"\n🔧 ANALYSE DES DIAMÈTRES")
    print(f"{'='*40}")
    
    # Compter les diamètres par taille
    def count_diameters(diam_dict):
        counts = {}
        for diam in diam_dict.values():
            counts[diam] = counts.get(diam, 0) + 1
        return counts
    
    counts_500 = count_diameters(diameters_500)
    counts_600 = count_diameters(diameters_600)
    
    print(f"   • Diamètres 500 m³/h: {counts_500}")
    print(f"   • Diamètres 600 m³/h: {counts_600}")
    
    # Comparer les diamètres
    all_diams = set(diameters_500.values()) | set(diameters_600.values())
    print(f"   • Diamètres utilisés: {sorted(all_diams)} mm")

# Créer un graphique de comparaison des coûts
plt.figure(figsize=(10, 6))
scenarios = ['500 m³/h', '600 m³/h']
costs = [cost_500, cost_600]

bars = plt.bar(scenarios, costs, color=['#2E86AB', '#A23B72'], alpha=0.8)
plt.ylabel('Coût (FCFA)')
plt.title('Comparaison des coûts d\'optimisation')
plt.grid(True, alpha=0.3)

# Ajouter les valeurs sur les barres
for bar, cost in zip(bars, costs):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
             f'{cost:,.0f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig("temp/plots/cost_comparison.png", dpi=300, bbox_inches='tight')
plt.close()

print(f"\n📊 GRAPHIQUES GÉNÉRÉS")
print(f"{'='*40}")
print(f"   • temp/plots/comparison_analysis.png - Comparaison pressions/débits")
print(f"   • temp/plots/cost_comparison.png - Comparaison des coûts")

# Recommandations
print(f"\n💡 RECOMMANDATIONS")
print(f"{'='*40}")

if cost_600 == cost_500:
    print(f"   ✅ Les deux scénarios ont le même coût d'optimisation")
    print(f"   ✅ La demande de 600 m³/h est économiquement équivalente")
    print(f"   ✅ Recommandation: Choisir selon les besoins en capacité")
else:
    if cost_600 > cost_500:
        print(f"   ⚠️ Le scénario 600 m³/h coûte {((cost_600 - cost_500) / cost_500 * 100):.1f}% de plus")
        print(f"   💡 Évaluer si l'augmentation de capacité justifie le surcoût")
    else:
        print(f"   ✅ Le scénario 600 m³/h est plus économique")
        print(f"   💡 Recommandation: Privilégier le scénario 600 m³/h")

if h_500 is not None and h_600 is not None and h_600 > h_500:
    print(f"   🏗️ Le réservoir 600 m³/h nécessite {h_600 - h_500:.2f} m de hauteur supplémentaire")
    print(f"   💡 Vérifier la faisabilité technique et les contraintes de site")

print(f"\n✅ Rapport terminé!")
print(f"📁 Fichiers générés dans: temp/plots/")
