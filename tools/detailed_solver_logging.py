#!/usr/bin/env python3
"""
Script de journalisation détaillée pour solveurs LCPI et EPANET.
Objectif: Capturer tous les paramètres et résultats pour comparaison.
"""

import logging
import json
from datetime import datetime
from pathlib import Path

class DetailedSolverLogger:
    def __init__(self, solver_name: str):
        self.solver_name = solver_name
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        log_dir = Path("logs_solvers")
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger(f"solver_{self.solver_name}")
        logger.setLevel(logging.DEBUG)
        
        # Handler fichier
        fh = logging.FileHandler(
            log_dir / f"{self.solver_name}_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        fh.setLevel(logging.DEBUG)
        
        # Handler console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def log_simulation_parameters(self, params: dict):
        """Log les paramètres de simulation."""
        self.logger.info(f"🔧 PARAMÈTRES DE SIMULATION {self.solver_name.upper()}")
        for key, value in params.items():
            self.logger.info(f"   {key}: {value}")
    
    def log_hydraulic_parameters(self, pipe_id: str, params: dict):
        """Log les paramètres hydrauliques d'une conduite."""
        self.logger.info(f"📏 PARAMÈTRES HYDRAULIQUES - Conduite {pipe_id}")
        for key, value in params.items():
            self.logger.info(f"   {key}: {value}")
    
    def log_solution_status(self, solution_id: str, status: dict):
        """Log le statut d'une solution."""
        self.logger.info(f"🎯 STATUT SOLUTION {solution_id}")
        for key, value in status.items():
            self.logger.info(f"   {key}: {value}")
    
    def log_constraint_violations(self, violations: list):
        """Log les violations de contraintes."""
        if violations:
            self.logger.warning(f"🚨 VIOLATIONS DE CONTRAINTES DÉTECTÉES")
            for violation in violations:
                self.logger.warning(f"   {violation}")
        else:
            self.logger.info("✅ Aucune violation de contrainte")
    
    def log_cost_details(self, cost_breakdown: dict):
        """Log le détail du coût."""
        self.logger.info(f"💰 DÉTAIL DU COÛT")
        for key, value in cost_breakdown.items():
            self.logger.info(f"   {key}: {value}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Logger pour LCPI
    lcpi_logger = DetailedSolverLogger("lcpi")
    lcpi_logger.log_simulation_parameters({
        "solver": "Hardy-Cross",
        "model": "Hazen-Williams",
        "tolerance": 0.001,
        "max_iterations": 100
    })
    
    # Logger pour EPANET
    epanet_logger = DetailedSolverLogger("epanet")
    epanet_logger.log_simulation_parameters({
        "solver": "EPANET",
        "model": "Chezy-Manning",
        "tolerance": 0.001,
        "max_iterations": 40
    })
