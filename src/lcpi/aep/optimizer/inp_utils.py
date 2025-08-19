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
				if pid in diameters_mm:
					parts[4] = str(int(diameters_mm[pid]))
					line = ("\t").join(parts)
		out.append(line)
	continue
	return out


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
		continue
	out.append(line)
	continue
	return out


def apply_modifications(inp_path: Path, H_tank_map: Dict[str, float], diameters_mm: Dict[str, int], out_path: Path | None = None) -> Tuple[Path, List[str]]:

	lines = read_inp_lines(inp_path)
	lines = tweak_pipes_diameter(lines, diameters_mm)
	lines = tweak_tanks_levels(lines, H_tank_map)
	out = out_path or Path(inp_path).with_name(Path(inp_path).stem + "_modified.inp")
	return write_inp_lines(lines, out), lines


