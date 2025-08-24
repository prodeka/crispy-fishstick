from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple


def read_inp_lines(inp_path: Path) -> List[str]:

	try:
		return Path(inp_path).read_text(encoding="utf-8", errors="ignore").splitlines()
	except Exception:
		return []


def write_inp_lines(lines: List[str], out_path: Path) -> Path:

	out_path.parent.mkdir(parents=True, exist_ok=True)
	out_path.write_text("\n".join(lines), encoding="utf-8")
	return out_path


def tweak_pipes_diameter(lines: List[str], diameters_mm: Dict[str, int]) -> List[str]:

	if not lines or not diameters_mm:
		return lines
	section = None
	out: List[str] = []
	for raw in lines:

		line = raw.rstrip("\n")
		stripd = line.strip()
		if not stripd or stripd.startswith(";"):
			out.append(line)
			continue
		if stripd.startswith("[") and stripd.endswith("]"):
			section = stripd.upper()
			out.append(line)
			continue
		if section == "[PIPES]":
			parts = stripd.split()
			if len(parts) >= 5:
				pid = parts[0]
				if pid in diameters_mm:  # Assurez-vous que le PID existe bien
					parts[4] = str(int(diameters_mm[pid]))
					line = ("\t").join(parts)
		out.append(line)
		# Correction: Cette ligne était mal indentée et ajoutait la dernière ligne en double
	return out


def count_pipes(inp_path: Path) -> int:
 """
 Counts the number of data lines in the [PIPES] section of an EPANET .inp file (excluding comments and section headers).
 """
 lines = read_inp_lines(inp_path)
 section = None
 pipe_count = 0
 for raw in lines:
  line = raw.strip()
  if not line or line.startswith(";"):
   continue
  if line.startswith("[") and line.endswith("]"):
   section = line.upper()
   continue
  if section == "[PIPES]":
   pipe_count += 1
 return pipe_count
# Correction: La fonction doit retourner 'pipe_count' après la boucle.
def tweak_tanks_levels(lines: List[str], H_tank_map: Dict[str, float]) -> List[str]:

	if not lines or not H_tank_map:
		return lines
	section = None
	out: List[str] = []
	for raw in lines:
		line = raw.rstrip("\n")
		stripd = line.strip()
		if not stripd or stripd.startswith(";"):
			out.append(line)
			continue
		if stripd.startswith("[") and stripd.endswith("]"):
			section = stripd.upper()
			out.append(line)
			continue
		if section == "[TANKS]":
			parts = stripd.split()
			if len(parts) >= 6:
				nid = parts[0]
				if nid in H_tank_map:
					try:
						elevation = float(parts[1])
						H = float(H_tank_map[nid])
						init_level = max(0.0, H - elevation)
						parts[2] = f"{init_level:.3f}"
						line = ("\t").join(parts)
					except Exception:
						pass
		out.append(line)
	# Correction: Supprimé la ligne qui ajoutait la dernière ligne en double
	return out


def apply_modifications(inp_path: Path, H_tank_map: Dict[str, float], diameters_mm: Dict[str, int], out_path: Path | None = None) -> Tuple[Path, List[str]]:

	lines = read_inp_lines(inp_path)
	lines = tweak_pipes_diameter(lines, diameters_mm)
	lines = tweak_tanks_levels(lines, H_tank_map)
	out = out_path or Path(inp_path).with_name(Path(inp_path).stem + "_modified.inp")
	return write_inp_lines(lines, out), lines


