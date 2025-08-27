CASE 
    -- Catégorie 1: Risque Très Élevé (Vertisols sur les pires roches mères)
    WHEN "TYPE_SOL" LIKE '%Vertisols%' AND ("TYPE_SOLS" LIKE '%Shales%' OR "TYPE_SOLS" LIKE '%Migmatites%' OR "TYPE_SOLS" LIKE '%Micaschistes%' OR "TYPE_SOLS" LIKE '%Gneiss%' OR "TYPE_SOLS" LIKE '%Axe%' OR "TYPE_SOLS" LIKE '%Azé%')
        THEN 'Risque Très Élevé'

    -- Catégorie 2: Risque Élevé (Autres Vertisols, ou pires roches mères avec sols argileux/hydromorphes)
    WHEN "TYPE_SOL" LIKE '%Vertisols%'
        THEN 'Risque Élevé'
    WHEN ("TYPE_SOLS" LIKE '%Shales%' OR "TYPE_SOLS" LIKE '%Schistes%' OR "TYPE_SOLS" LIKE '%Migmatites%' OR "TYPE_SOLS" LIKE '%Micaschistes%') AND ("TYPE_SOL" LIKE '%hydromorphes%' OR "TYPE_SOL" LIKE '%ferralitiques%')
        THEN 'Risque Élevé'
    
    -- Catégorie 3: Risque Moyen (Roches moyennement propices avec sols argileux/hydromorphes, ou pires roches mères avec sols ferrugineux)
    WHEN ("TYPE_SOLS" LIKE '%Gneiss%' OR "TYPE_SOLS" LIKE '%Orthogneiss%' OR "TYPE_SOLS" LIKE '%Granodiorites%' OR "TYPE_SOLS" LIKE '%Metadiorites%' OR "TYPE_SOLS" LIKE '%Axe%' OR "TYPE_SOLS" LIKE '%Azé%') AND ("TYPE_SOL" LIKE '%hydromorphes%' OR "TYPE_SOL" LIKE '%ferralitiques%')
        THEN 'Risque Moyen'
    WHEN ("TYPE_SOLS" LIKE '%Alluvionnaires%' OR "TYPE_SOLS" LIKE '%Sédimentaire%') AND ("TYPE_SOL" LIKE '%hydromorphes%' OR "TYPE_SOL" LIKE '%ferralitiques%')
        THEN 'Risque Moyen'
    WHEN ("TYPE_SOLS" LIKE '%Shales%' OR "TYPE_SOLS" LIKE '%Schistes%' OR "TYPE_SOLS" LIKE '%Migmatites%' OR "TYPE_SOLS" LIKE '%Micaschistes%') AND "TYPE_SOL" LIKE '%ferrugineux%'
        THEN 'Risque Moyen'

    -- Catégorie 4: Risque Très Faible (Sols peu développés et cuirasses, conditions prioritaires qui annulent le reste)
    WHEN "TYPE_SOLS" LIKE '%Cuirasses%'
        THEN 'Risque Très Faible'
    WHEN "TYPE_SOL" LIKE '%peu évolués%' -- Typo 'érrosion' incluse
        THEN 'Risque Très Faible'

    -- Catégorie 5: Risque Faible (Roches résistantes et autres cas par défaut)
    WHEN "TYPE_SOLS" LIKE '%Grès%' OR "TYPE_SOLS" LIKE '%Gres%' OR "TYPE_SOLS" LIKE '%Quartzites%' OR "TYPE_SOLS" LIKE '%Granites%' OR "TYPE_SOLS" LIKE '%Silexites%'
        THEN 'Risque Faible'
    
    -- Catégorie finale par défaut pour toutes les autres combinaisons (qui sont majoritairement à faible risque)
    ELSE 'Risque Faible'
END