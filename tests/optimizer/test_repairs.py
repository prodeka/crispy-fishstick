import pytest
from src.lcpi.aep.optimization.repairs import soft_repair_solution

def test_soft_repair_increases_most_problematic_pipe():
    # Arrange
    diameters_map = {"P1": 110, "P2": 90, "P3": 110}
    # P2 a la plus grosse perte de charge, P3 la deuxième
    sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1}}
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act: réparer 20% des conduites (donc la plus problématique, 1 conduite)
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters, max_changes_fraction=0.20
    )
    
    # Assert
    assert changes["total_changes"] == 1
    assert changes["repaired_pipes"][0]["pipe_id"] == "P2"
    assert changes["repaired_pipes"][0]["from_dn_mm"] == 90
    assert changes["repaired_pipes"][0]["to_dn_mm"] == 110 # 1 cran de plus
    assert "selected_problematic_pipes" in changes
    assert "P2" in changes["selected_problematic_pipes"]
    
    # Vérifier que les autres conduites n'ont pas changé
    assert repaired_map["P1"] == 110
    assert repaired_map["P3"] == 110

def test_soft_repair_no_headlosses_data():
    # Arrange
    diameters_map = {"P1": 110, "P2": 90, "P3": 110}
    sim_metrics = {}  # Pas de données de perte de charge
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters
    )
    
    # Assert: aucune réparation effectuée
    assert changes["total_changes"] == 0
    assert changes["repaired_pipes"] == []
    assert repaired_map is None  # Retourne None si aucune réparation

def test_soft_repair_maximum_diameter_reached():
    # Arrange
    diameters_map = {"P1": 160, "P2": 160, "P3": 160}  # Tous au maximum
    sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1}}
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters
    )
    
    # Assert: aucune réparation possible car déjà au maximum
    assert changes["total_changes"] == 0
    assert repaired_map is None  # Retourne None si aucune réparation

def test_soft_repair_multiple_pipes():
    # Arrange
    diameters_map = {"P1": 90, "P2": 90, "P3": 90, "P4": 90, "P5": 90}
    sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1, "P4": 8.5, "P5": 3.2}}
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act: réparer 40% des conduites (2 conduites)
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters, max_changes_fraction=0.40
    )
    
    # Assert: les 2 conduites les plus problématiques ont été réparées
    assert changes["total_changes"] == 2
    assert changes["repaired_pipes"][0]["pipe_id"] == "P2"  # Plus grosse perte de charge
    assert changes["repaired_pipes"][1]["pipe_id"] == "P3"  # Deuxième plus grosse perte de charge
    assert changes["repaired_pipes"][0]["from_dn_mm"] == 90
    assert changes["repaired_pipes"][0]["to_dn_mm"] == 110
    assert changes["repaired_pipes"][1]["from_dn_mm"] == 90
    assert changes["repaired_pipes"][1]["to_dn_mm"] == 110

def test_soft_repair_invalid_diameter():
    # Arrange
    diameters_map = {"P1": 110, "P2": 95, "P3": 110}  # P2 a un diamètre invalide
    sim_metrics = {"headlosses_m": {"P1": 5.2, "P2": 15.8, "P3": 10.1}}
    candidate_diameters = [75, 90, 110, 125, 160]
    
    # Act
    repaired_map, changes = soft_repair_solution(
        diameters_map, sim_metrics, candidate_diameters
    )
    
    # Assert: P2 ne peut pas être réparé car son diamètre n'est pas dans la liste des candidats
    assert changes["total_changes"] == 0
    assert repaired_map is None  # Retourne None si aucune réparation
