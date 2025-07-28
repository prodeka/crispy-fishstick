BAR_LIBRARY = {
    6: 0.28, 8: 0.50, 10: 0.79, 12: 1.13, 14: 1.54,
    16: 2.01, 20: 3.14, 25: 4.91, 32: 8.04, 40: 12.57,
}

def get_rebar_proposals(required_area_cm2, num_proposals=4, min_bars=4):
    """
    Trouve les meilleures combinaisons (uniques ou mixtes) pour une section d'acier.
    """
    proposals = []

    # --- 1. Générer les propositions à DIAMÈTRE UNIQUE ---
    for diameter_mm, area_cm2 in BAR_LIBRARY.items():
        if diameter_mm < 8:
            continue
        for num_bars in range(min_bars, 17, 2): # [4, 6, ..., 16]
            provided_area = num_bars * area_cm2
            if provided_area >= required_area_cm2:
                proposals.append({
                    "type": "single",
                    "score": provided_area - required_area_cm2,
                    "num_bars": num_bars,
                    "diameter": diameter_mm,
                    "provided_area": provided_area,
                    "text": f"{num_bars} x Φ{diameter_mm}"
                })

    # --- 2. Générer les propositions à DIAMÈTRES MIXTES ---
    # Règle : 4 grosses barres dans les coins + N petites barres sur les faces.
    for corner_diam, corner_area in BAR_LIBRARY.items():
        if corner_diam < 12:
            continue # Les barres de coin doivent être assez grosses

        for face_diam, face_area in BAR_LIBRARY.items():
            # Règle : les barres de face sont plus petites ou égales aux barres de coin
            if face_diam > corner_diam:
                continue
            # Règle : on ne mélange pas des diamètres trop différents
            if face_diam < corner_diam / 2:
                continue

            # On commence avec 4 barres de coin
            current_area = 4 * corner_area
            # On teste l'ajout de 2, 4, 6 ou 8 barres de face
            for num_face_bars in [2, 4, 6, 8]:
                provided_area = current_area + (num_face_bars * face_area)
                if provided_area >= required_area_cm2:
                    proposals.append({
                        "type": "mixed",
                        "score": provided_area - required_area_cm2,
                        "num_bars": 4 + num_face_bars,
                        "corner_config": (4, corner_diam),
                        "face_config": (num_face_bars, face_diam),
                        "provided_area": provided_area,
                        "text": f"4xΦ{corner_diam} + {num_face_bars}xΦ{face_diam}"
                    })

    # --- 3. Trier toutes les propositions et retourner les meilleures ---
    if not proposals:
        return []

    sorted_proposals = sorted(proposals, key=lambda p: p['score'])
    
    # On enlève les doublons textuels pour ne pas avoir 2 fois la même proposition
    final_proposals = []
    seen_texts = set()
    for p in sorted_proposals:
        if p['text'] not in seen_texts:
            final_proposals.append(p)
            seen_texts.add(p['text'])
    
    return final_proposals[:num_proposals]