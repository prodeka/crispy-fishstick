from pathlib import Path

def test_convert_inp_minimal(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import convert_inp_to_unified_model  # type: ignore
    dummy = tmp_path / "dummy.inp"
    dummy.write_text("[JUNCTIONS]\n; none\n[PIPES]\nP1 N1 N2 100 110\n")
    out = convert_inp_to_unified_model(dummy)
    assert "meta" in out
    assert isinstance(out.get("links", {}), dict)


