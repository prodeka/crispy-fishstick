import streamlit as st
import pandas as pd
import requests # Import requests
import matplotlib.pyplot as plt # Import matplotlib for plotting

st.title("NanoStruct Web App")

# --- Début de l'onglet Assainissement ---
st.header("Dimensionnement de Réseau d'Assainissement Pluvial")

# ÉTAPE 1 : CHARGEMENT DES DONNÉES
st.subheader("1. Données des Tronçons")
fichier_csv = st.file_uploader("Chargez votre fichier CSV de tronçons", type=["csv"])

if fichier_csv is not None:
    # Lire le fichier CSV
    try:
        df_troncons = pd.read_csv(fichier_csv)
        st.success("Fichier CSV chargé avec succès !")
        st.dataframe(df_troncons.head())
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier CSV : {e}")
        df_troncons = None

    if df_troncons is not None:
        # ÉTAPE 2 : PARAMÈTRES
        st.subheader("2. Paramètres du Calcul")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Méthode de Calcul")
            methode_calcul = st.selectbox("Méthode de calcul", ["Rationnelle", "Caquot"], key="ass_methode")

            tc_formule_name = "kirpich" # Valeur par défaut
            if methode_calcul == 'Rationnelle':
                tc_formule_name = st.selectbox(
                    "Formule de Tc de surface",
                    ["Kirpich", "Californienne"],
                    key="ass_tc"
                ).lower()

            st.markdown("#### Paramètres de Validation")
            v_min = st.number_input("Vitesse minimale (m/s)", value=0.6, step=0.1, key="ass_vmin")
            v_max = st.number_input("Vitesse maximale (m/s)", value=2.0, step=0.1, key="ass_vmax")

        with col2:
            st.markdown("#### Pluviométrie (Paramètres IDF)")
            # Ici, nous allons simplifier pour commencer. Nous ferons un menu dynamique plus tard.
            # Pour l'instant, saisie manuelle :
            st.write("Saisie manuelle des paramètres de pluie (Montana)")
            idf_a = st.number_input("Coefficient 'a' (Montana)", value=411.0, format="%.2f")
            idf_b = st.number_input("Coefficient 'b' (Montana)", value=-0.48, format="%.2f")
            periode_retour = st.number_input("Période de retour T (ans)", value=10, step=5)

            params_pluie = {
                "formula": "montana",
                "periode_retour": periode_retour,
                "nom": f"Manuel T={periode_retour} ans",
                "a": idf_a,
                "b": idf_b
            }

        # ÉTAPE 3 : LANCEMENT
        st.subheader("3. Lancer la Simulation")
        verbose = st.toggle("Activer le mode verbeux (logs détaillés)", value=False)

        if st.button("Lancer le Dimensionnement", use_container_width=True):
            # Préparer le payload pour l'API
            payload = {
                "troncons_data": df_troncons.to_dict(orient='records'),
                "methode_calcul": methode_calcul.lower(),
                "tc_formule_name": tc_formule_name,
                "params_pluie": params_pluie,
                "v_min": v_min,
                "v_max": v_max,
                "verbose": verbose
            }

            # Appel à l'API Flask
            try:
                response = requests.post("http://localhost:5000/api/assainissement/calcul", json=payload)
                result = response.json()

                if result.get("success"):
                    st.success("Calcul effectué avec succès !")
                    st.write("### Résultats du Dimensionnement")
                    df_results = pd.DataFrame(result.get("resultat"))
                    st.dataframe(df_results)

                    # Afficher le log verbeux si activé
                    if verbose and result.get("verbose_log"):
                        st.write("### Log Détaillé")
                        st.text(result.get("verbose_log"))

                    # Exemple de graphique simple (peut être amélioré)
                    st.write("### Visualisation des Vitesses")
                    fig, ax = plt.subplots()
                    ax.bar(df_results["id_troncon"], df_results["vitesse_ms"])
                    ax.set_xlabel("ID Tronçon")
                    ax.set_ylabel("Vitesse (m/s)")
                    ax.set_title("Vitesses calculées par tronçon")
                    st.pyplot(fig)

                else:
                    st.error(f"Erreur lors du calcul : {result.get('message', 'Erreur inconnue')}")
                    if result.get("error"):
                        st.error(f"Détails de l'erreur : {result.get('error')}")
                    st.json(result) # Afficher la réponse complète pour le débogage

            except requests.exceptions.ConnectionError:
                st.error("Impossible de se connecter à l'API Flask. Assurez-vous que le serveur Flask est en cours d'exécution (python web/app.py).")
            except Exception as e:
                st.error(f"Une erreur inattendue est survenue lors de l'appel API : {e}")

# --- Fin de l'onglet Assainissement ---
