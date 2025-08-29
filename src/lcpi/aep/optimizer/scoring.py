from __future__ import annotations

from typing import Dict, Any, Optional

# Source des prix (SQLite)
try:
    # Import paresseux pour éviter les erreurs dans des contextes minimaux
    from .db_dao import prices_dao  # type: ignore
except Exception:  # pragma: no cover
    prices_dao = None  # type: ignore

RHO = 1000.0  # Densité de l'eau en kg/m³
G = 9.81  # Accélération gravitationnelle en m/s²

class CostScorer:
    """Calcule les coûts d'investissement (CAPEX) et d'exploitation (OPEX) d'un réseau."""

    def __init__(
        self,
        diameter_cost_db: Optional[Dict[int, float]] = None,
        energy_price_kwh: float = 0.15,
        pump_efficiency: float = 0.75,
        discount_rate: float = 0.05,
        horizon_years: int = 20,
    ):
        # Utiliser le gestionnaire centralisé des diamètres si aucun coût fourni
        if diameter_cost_db is None:
            try:
                from .diameter_manager import get_diameter_manager
                manager = get_diameter_manager()
                # Créer un mapping diamètre -> prix
                candidates = manager.get_candidate_diameters()
                diameter_cost_db = {c.diameter_mm: c.cost_per_m for c in candidates}
            except Exception as e:
                logger.warning(f"Impossible de charger les prix depuis le gestionnaire centralisé: {e}")
                diameter_cost_db = {}
        
        self.diameter_costs = diameter_cost_db or {}
        self.energy_price = energy_price_kwh
        self.pump_efficiency = pump_efficiency
        self.discount_rate = discount_rate
        self.horizon_years = horizon_years

    def compute_capex(self, network: Any, diameters: Dict[str, int]) -> float:
        """Calcule le coût d'investissement (CAPEX) basé sur le coût des conduites."""
        links = getattr(network, "links", None)
        if links is None and isinstance(network, dict):
            links = network.get("links", {})
        
        total_cost = 0.0
        for link_id, link_data in (links or {}).items():
            length = float(link_data.get("length_m", 0.0))
            diameter_mm = diameters.get(link_id, link_data.get("diameter_mm"))
            if diameter_mm is None:
                continue
            
            # Priorité: coûts fournis à l'initialisation, sinon lecture DB (avec fallback DN proche)
            cost_per_meter = self.diameter_costs.get(int(diameter_mm)) if self.diameter_costs else None
            if (cost_per_meter is None or float(cost_per_meter) == 0.0) and prices_dao is not None:
                try:
                    # 1) Essai exact
                    db_price = prices_dao.get_diameter_price(int(diameter_mm), "PVC-U")
                    if db_price is None:
                        # 2) Fallback: DN le plus proche disponible (prend le DN supérieur si possible)
                        avail = prices_dao.get_available_diameters("PVC-U") or []
                        dn_list = sorted(int(x.get("d_mm")) for x in avail if x.get("d_mm") is not None)
                        chosen_dn = None
                        for dn in dn_list:
                            if dn >= int(diameter_mm):
                                chosen_dn = dn
                                break
                        if chosen_dn is None and dn_list:
                            chosen_dn = dn_list[-1]
                        if chosen_dn is not None:
                            db_price = prices_dao.get_diameter_price(int(chosen_dn), "PVC-U")
                    cost_per_meter = float(db_price) if db_price is not None else 0.0
                except Exception:
                    cost_per_meter = 0.0
            if cost_per_meter is None:
                cost_per_meter = 0.0
            cost_per_meter = float(cost_per_meter)
            pipe_cost = length * cost_per_meter

            # Ajouter le coût des accessoires si fourni par conduite
            accessories_total = 0.0
            try:
                accessories_list = link_data.get("accessories") or []
                if isinstance(accessories_list, list):
                    for acc in accessories_list:
                        if not isinstance(acc, dict):
                            continue
                        code = acc.get("accessory_code") or acc.get("code")
                        if not code:
                            continue
                        dn = acc.get("dn_mm") or int(diameter_mm)
                        qty = acc.get("qty") or acc.get("quantity") or 1
                        unit_price = acc.get("unit_fcfa")
                        if unit_price is None and prices_dao is not None:
                            try:
                                p = prices_dao.get_accessory_price(str(code), int(dn))
                                unit_price = float(p) if p is not None else 0.0
                            except Exception:
                                unit_price = 0.0
                        unit_price = float(unit_price or 0.0)
                        try:
                            qty_val = float(qty)
                        except Exception:
                            qty_val = 1.0
                        accessories_total += qty_val * unit_price
            except Exception:
                accessories_total = accessories_total  # no-op, robust fallback

            total_cost += pipe_cost + accessories_total
            
        return float(total_cost)

    def compute_capex_with_breakdown(self, network: Any, diameters: Dict[str, int]) -> Dict[str, Any]:
        """Retourne un détail par conduite (tuyau + accessoires) et le total CAPEX.

        Structure:
        {
          "total_capex": float,
          "items": [
            {
              "link_id": str,
              "length_m": float,
              "dn_mm": int,
              "unit_cost_per_m": float,
              "pipe_cost": float,
              "accessories": [ {"code": str, "dn_mm": int, "qty": float, "unit_fcfa": float, "cost": float} ],
              "accessories_cost": float,
              "total": float
            }, ...
          ]
        }
        """
        links = getattr(network, "links", None)
        if links is None and isinstance(network, dict):
            links = network.get("links", {})

        items = []
        total_capex = 0.0
        for link_id, link_data in (links or {}).items():
            length = float(link_data.get("length_m", 0.0))
            dn_val = diameters.get(link_id, link_data.get("diameter_mm"))
            if dn_val is None:
                continue
            # prix par mètre
            unit = self.diameter_costs.get(int(dn_val)) if self.diameter_costs else None
            if (unit is None or float(unit) == 0.0) and prices_dao is not None:
                try:
                    db_price = prices_dao.get_diameter_price(int(dn_val), "PVC-U")
                    if db_price is None:
                        avail = prices_dao.get_available_diameters("PVC-U") or []
                        dn_list = sorted(int(x.get("d_mm")) for x in avail if x.get("d_mm") is not None)
                        chosen = next((dn for dn in dn_list if dn >= int(dn_val)), (dn_list[-1] if dn_list else None))
                        if chosen is not None:
                            db_price = prices_dao.get_diameter_price(int(chosen), "PVC-U")
                    unit = float(db_price) if db_price is not None else 0.0
                except Exception:
                    unit = 0.0
            unit = float(unit or 0.0)
            pipe_cost = unit * length

            # accessoires
            accessories_total = 0.0
            accessories_out = []
            try:
                accessories_list = link_data.get("accessories") or []
                if isinstance(accessories_list, list):
                    for acc in accessories_list:
                        if not isinstance(acc, dict):
                            continue
                        code = acc.get("accessory_code") or acc.get("code")
                        dn_acc = acc.get("dn_mm") or int(dn_val)
                        qty = acc.get("qty") or acc.get("quantity") or 1
                        unit_price = acc.get("unit_fcfa")
                        if unit_price is None and prices_dao is not None and code:
                            try:
                                p = prices_dao.get_accessory_price(str(code), int(dn_acc))
                                unit_price = float(p) if p is not None else 0.0
                            except Exception:
                                unit_price = 0.0
                        unit_price = float(unit_price or 0.0)
                        try:
                            qty_val = float(qty)
                        except Exception:
                            qty_val = 1.0
                        cost = qty_val * unit_price
                        accessories_total += cost
                        accessories_out.append({
                            "code": code,
                            "dn_mm": int(dn_acc),
                            "qty": qty_val,
                            "unit_fcfa": unit_price,
                            "cost": cost,
                        })
            except Exception:
                accessories_total = accessories_total

            total_item = pipe_cost + accessories_total
            total_capex += total_item
            items.append({
                "link_id": link_id,
                "length_m": length,
                "dn_mm": int(dn_val),
                "unit_cost_per_m": unit,
                "pipe_cost": pipe_cost,
                "accessories": accessories_out,
                "accessories_cost": accessories_total,
                "total": total_item,
            })

        return {"total_capex": float(total_capex), "items": items}

    def compute_total_cost(self, network: Any, diameters: Dict[str, int], sim_results: Optional[Dict[str, Any]] = None, lambda_opex: float = 1.0) -> float:
        """Calcule le coût total pondéré (CAPEX + λ*OPEX)."""
        capex = self.compute_capex(network, diameters)
        opex_npv = self.compute_opex_npv(sim_results) if sim_results else 0.0
        return self.compute_weighted_score(capex, opex_npv, lambda_opex)

    def compute_opex_npv(self, sim_results: Optional[Dict[str, Any]]) -> float:
        """
        Calcule la Valeur Actuelle Nette (NPV) de l'OPEX sur un horizon donné.
        L'OPEX est principalement basé sur le coût énergétique du pompage.
        """
        if not sim_results:
            return 0.0
            
        # sim_results doit contenir les débits (flow) et hauteurs (head) des pompes
        pump_flow_df = sim_results.get("pump_flow")  # Doit être un DataFrame pandas
        pump_head_df = sim_results.get("pump_head")
        
        if pump_flow_df is None or pump_head_df is None or (hasattr(pump_flow_df, 'empty') and pump_flow_df.empty):
            return 0.0

        # Calcul de la puissance (W) pour chaque pas de temps
        power_df = (RHO * G * pump_flow_df * pump_head_df) / self.pump_efficiency
        
        # Énergie totale sur la durée de la simulation (en kWh)
        # dt est la durée d'un pas de temps en secondes
        dt_seconds = sim_results.get("simulation_timestep_s", 3600)
        total_energy_kwh = power_df.sum().sum() * (dt_seconds / 3600.0)
        
        # Extrapolation à une année complète
        sim_duration_days = sim_results.get("simulation_duration_h", 24) / 24.0
        annual_energy_kwh = total_energy_kwh * (365.0 / sim_duration_days)
        annual_cost = annual_energy_kwh * self.energy_price

        # Calcul de la NPV
        opex_npv = sum(
            annual_cost / ((1 + self.discount_rate) ** year)
            for year in range(1, self.horizon_years + 1)
        )
        return float(opex_npv)

    def compute_weighted_score(self, capex: float, opex_npv: float, lambda_opex: float = 1.0) -> float:
        """Calcule un score pondéré combinant CAPEX et OPEX."""
        return capex + lambda_opex * opex_npv

    def evaluate_solution(
        self, network: Any, diameters: Dict[str, int], sim_results: Dict[str, Any], lambda_opex: float = 1.0
    ) -> Dict[str, float]:
        """Évalue une solution complète et retourne tous les scores pertinents."""
        capex = self.compute_capex(network, diameters)
        opex_npv = self.compute_opex_npv(sim_results)
        weighted_score = self.compute_weighted_score(capex, opex_npv, lambda_opex)
        
        return {
            "capex": capex,
            "opex_npv": opex_npv,
            "weighted_score": weighted_score,
        }


