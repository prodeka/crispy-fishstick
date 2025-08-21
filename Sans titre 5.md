Je vérifie l’existence des fichiers et j’extrais un diagnostic rapide depuis le JSON (best_cost vs CAPEX, PriceDB, diamètres uniques, somme des débits, stats présentes) ainsi que la présence des logs FLOW_CONSERVATION_BREACH / REPAIR_DIAMETERS_APPLIED.
```bash
powershell -NoProfile -Command "Write-Host 'JSON:' (Test-Path .\results\test_integrated_stats.json); Write-Host 'LOG:' (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'); Write-Host 'PDF:' ((Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Select-Object -First 1).FullName)"
```
```bash
./venv_new/Scripts/python.exe - << 'PY'
import json, math, sys, pathlib
from pathlib import Path
p = Path('results/test_integrated_stats.json')
if not p.exists():
    print('MISSING_JSON')
    sys.exit(0)
d = json.loads(p.read_text(encoding='utf-8'))
meta = d.get('meta', {})
props = d.get('proposals') or [{}]
best_cost = meta.get('best_cost')
capex = props[0].get('CAPEX')
constraints_ok = props[0].get('constraints_ok')
price_db_info = meta.get('price_db_info')
diams = props[0].get('diameters_mm') or []
uniq = sorted({int(x) for x in diams}) if diams else []
hyd = d.get('hydraulics') or {}
flows = hyd.get('flows_m3_s') or hyd.get('flows') or []
def val(x):
    if isinstance(x, dict):
        return float(x.get('value', 0) or 0)
    try:
        return float(x)
    except Exception:
        return 0.0
signed = [val(x) for x in flows]
psum = sum(signed)
pos = sum(1 for v in signed if v>1e-12)
neg = sum(1 for v in signed if v<-1e-12)
zer = sum(1 for v in signed if abs(v)<=1e-12)
has_stats = bool((hyd.get('statistics') or {}) )
print('best_cost=', best_cost)
print('capex=', capex)
print('constraints_ok=', constraints_ok)
print('price_db_info.type=', (price_db_info or {}).get('type'))
print('price_db_info.source=', (price_db_info or {}).get('source'))
print('diam_count=', len(diams))
print('diam_unique=', uniq)
print('flows_count=', len(signed))
print('flows_sum=', psum)
print('flows_pos/neg/zero=', pos, neg, zer)
print('has_hydraulic_stats=', has_stats)
# scan log markers
logp = Path('test_validation/logs')
marker1 = 'FLOW_CONSERVATION_BREACH'
marker2 = 'REPAIR_DIAMETERS_APPLIED'
found1 = found2 = False
if logp.exists():
    for f in sorted(logp.glob('aep_network_optimize_unified_*.log.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
        try:
            t = f.read_text(encoding='utf-8', errors='ignore')
            if marker1 in t: found1 = True
            if marker2 in t: found2 = True
        except Exception:
            pass
print('log_FLOW_CONSERVATION_BREACH=', found1)
print('log_REPAIR_DIAMETERS_APPLIED=', found2)
PY
```
```bash
./venv_new/Scripts/python.exe -c "import json,math,sys; import pathlib as P; p=P.Path('results/test_integrated_stats.json'); d=json.load(open(p,'r',encoding='utf-8')) if p.exists() else {}; meta=d.get('meta',{}); props=d.get('proposals') or [{}]; hyd=d.get('hydraulics') or {}; flows=hyd.get('flows_m3_s') or hyd.get('flows') or []; val=lambda x:(x.get('value',0.0) if isinstance(x,dict) else x) or 0.0; s=sum(float(val(x)) for x in flows); diams=props[0].get('diameters_mm') or []; uniq=sorted({int(x) for x in diams}) if diams else []; print('best_cost=',meta.get('best_cost')); print('capex=',props[0].get('CAPEX')); print('constraints_ok=',props[0].get('constraints_ok')); pinfo=meta.get('price_db_info') or {}; print('price_db_info.type=',pinfo.get('type')); print('price_db_info.source=',pinfo.get('source')); print('diam_count=',len(diams)); print('diam_unique=',uniq); print('flows_count=',len(flows)); print('flows_sum=',s); print('has_hydraulic_stats=', bool(hyd.get('statistics'))); import glob; import pathlib; import io; log_files=sorted(pathlib.Path('test_validation/logs').glob('aep_network_optimize_unified_*.log.json'), key=lambda x:x.stat().st_mtime, reverse=True)[:3]; f1=f2=False; 
import codecs; 
for f in log_files:
    try:
        t=codecs.open(f,'r','utf-8','ignore').read();
        if 'FLOW_CONSERVATION_BREACH' in t: f1=True
        if 'REPAIR_DIAMETERS_APPLIED' in t: f2=True
    except Exception: pass
print('log_FLOW_CONSERVATION_BREACH=',f1); print('log_REPAIR_DIAMETERS_APPLIED=',f2)"
```

Je vérifie concrètement: existence JSON/LOG/PDF et j’extrais un diagnostic robuste (best_cost, CAPEX, constraints_ok, diamètres uniques, somme des débits), en tolérant des structures de flux hétérogènes.
```bash
powershell -NoProfile -Command "Write-Host 'JSON:' (Test-Path .\results\test_integrated_stats.json); if (Test-Path .\results\test_integrated_stats.json){(Get-Item .\results\test_integrated_stats.json).Length}; Write-Host 'LOG:' (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'); if (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'){(Get-Item 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json').Length}; $pdf=(Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1); Write-Host 'PDF:' ($pdf -ne $null); if ($pdf){$pdf.FullName; $pdf.Length}"
```
```bash
powershell -NoProfile -Command "$json=Test-Path .\results\test_integrated_stats.json; Write-Host ('JSON: ' + $json); if($json){(Get-Item .\results\test_integrated_stats.json).Length | Write-Host}; $logp='C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'; $log=Test-Path $logp; Write-Host ('LOG: ' + $log); if($log){(Get-Item $logp).Length | Write-Host}; $pdf=(Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1); if($pdf){ Write-Host 'PDF: True'; $pdf.FullName; $pdf.Length } else { Write-Host 'PDF: False' }"
```
```bash
powershell -NoProfile -Command "$jsonPath='results/test_integrated_stats.json'; if (Test-Path $jsonPath) { Write-Host 'JSON: True'; (Get-Item $jsonPath).Length } else { Write-Host 'JSON: False' }; $logPath='C:/PROJET_DIMENTIONEMENT_2/test_validation/logs/aep_network_optimize_unified_20250821_130348.log.json'; if (Test-Path $logPath) { Write-Host 'LOG: True'; (Get-Item $logPath).Length } else { Write-Host 'LOG: False' }; $pdfFile=Get-ChildItem results/*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1; if ($pdfFile) { Write-Host 'PDF: True'; $pdfFile.FullName; $pdfFile.Length } else { Write-Host 'PDF: False' }"
```
- JSON: présent (vérifié par l’app CLI).
- Log: présent au chemin indiqué.
- PDF: la CLI a tenté; les backends ont échoué. On traitera PDF après.

Pour l’analyse:
- Flow conservation: total ≈ -1.202 m³/s (confirmé à l’écran). À diagnostiquer sur `hydraulics.flows_*` et sens d’agrégation.
- Diamètres: min=max=200 mm (toutes conduites). À vérifier via `meta.price_db_info` et le flag `REPAIR_DIAMETERS_APPLIED`.

S C:\PROJET_DIMENTIONEMENT_2> powershell -NoProfile -Command "Write-Host 'JSON:' (Test-Path .\results\test_integrated_stats.json); Write-Host 'LOG:' (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'); Write-Host 'PDF:' ((Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Select-Object -First 1).FullName)"                                                                                                                 
JSON: True
LOG: True
PDF: C:\PROJET_DIMENTIONEMENT_2\results\test_integrated_stats.pdf
PS C:\PROJET_DIMENTIONEMENT_2> ./venv_new/Scripts/python.exe - << 'PY'                                                      
ParserError: 
Line |
   1 |  ./venv_new/Scripts/python.exe - << 'PY'
     |                                   ~
     | Missing file specification after redirection operator.
PS C:\PROJET_DIMENTIONEMENT_2> import json, math, sys, pathlib
import: The term 'import' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> from pathlib import Path
ParserError: 
Line |
   1 |  from pathlib import Path
     |  ~~~~
     | The 'from' keyword is not supported in this version of the language.
PS C:\PROJET_DIMENTIONEMENT_2> p = Path('results/test_integrated_stats.json')
p: The term 'p' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

[General Feedback]
  The most similar commands are:
    ➤ %, ?, gp, mp, rp

PS C:\PROJET_DIMENTIONEMENT_2> if not p.exists():
ParserError: 
Line |
   1 |  if not p.exists():
     |    ~
     | Missing '(' after 'if' in if statement.
PS C:\PROJET_DIMENTIONEMENT_2>     print('MISSING_JSON')
Impossible d’initialiser le périphérique PRN
PS C:\PROJET_DIMENTIONEMENT_2>     sys.exit(0)
sys.exit: The term 'sys.exit' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> d = json.loads(p.read_text(encoding='utf-8'))
encoding=utf-8: The term 'encoding=utf-8' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> meta = d.get('meta', {})
meta: The term 'meta' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> props = d.get('proposals') or [{}]
props: The term 'props' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> best_cost = meta.get('best_cost')
best_cost: The term 'best_cost' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> capex = props[0].get('CAPEX')
capex: The term 'capex' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> constraints_ok = props[0].get('constraints_ok')
constraints_ok: The term 'constraints_ok' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> price_db_info = meta.get('price_db_info')
price_db_info: The term 'price_db_info' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> diams = props[0].get('diameters_mm') or []
diams: The term 'diams' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> uniq = sorted({int(x) for x in diams}) if diams else []
uniq: The term 'uniq' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> hyd = d.get('hydraulics') or {}
hyd: The term 'hyd' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> flows = hyd.get('flows_m3_s') or hyd.get('flows') or []
flows: The term 'flows' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> def val(x):
x: The term 'x' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

[General Feedback]
  The most similar commands are:
    ➤ %, ?, h, r, X:

PS C:\PROJET_DIMENTIONEMENT_2>     if isinstance(x, dict):
ParserError: 
Line |
   1 |      if isinstance(x, dict):
     |        ~
     | Missing '(' after 'if' in if statement.
PS C:\PROJET_DIMENTIONEMENT_2>         return float(x.get('value', 0) or 0)
x.get: The term 'x.get' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2>     try:
try:: The term 'try:' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2>         return float(x)
x: The term 'x' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

[General Feedback]
  The most similar commands are:
    ➤ %, ?, h, r, X:

PS C:\PROJET_DIMENTIONEMENT_2>     except Exception:
except: The term 'except' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2>         return 0.0
0
PS C:\PROJET_DIMENTIONEMENT_2> signed = [val(x) for x in flows]
x: The term 'x' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

[General Feedback]
  The most similar commands are:
    ➤ %, ?, h, r, X:

PS C:\PROJET_DIMENTIONEMENT_2> psum = sum(signed)
signed: The term 'signed' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> pos = sum(1 for v in signed if v>1e-12)
ParserError: 
Line |
   1 |  pos = sum(1 for v in signed if v>1e-12)
     |              ~~~
     | Unexpected token 'for' in expression or statement.
PS C:\PROJET_DIMENTIONEMENT_2> neg = sum(1 for v in signed if v<-1e-12)
ParserError: 
Line |
   1 |  neg = sum(1 for v in signed if v<-1e-12)
     |              ~~~
     | Unexpected token 'for' in expression or statement.
PS C:\PROJET_DIMENTIONEMENT_2> zer = sum(1 for v in signed if abs(v)<=1e-12)
ParserError: 
Line |
   1 |  zer = sum(1 for v in signed if abs(v)<=1e-12)
     |              ~~~
     | Unexpected token 'for' in expression or statement.
PS C:\PROJET_DIMENTIONEMENT_2> has_stats = bool((hyd.get('statistics') or {}) )
hyd.get: The term 'hyd.get' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> print('best_cost=', best_cost)
ParserError: 
Line |
   1 |  print('best_cost=', best_cost)
     |                     ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('capex=', capex)
ParserError: 
Line |
   1 |  print('capex=', capex)
     |                 ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('constraints_ok=', constraints_ok)
ParserError: 
Line |
   1 |  print('constraints_ok=', constraints_ok)
     |                          ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('price_db_info.type=', (price_db_info or {}).get('type'))
price_db_info: The term 'price_db_info' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> print('price_db_info.source=', (price_db_info or {}).get('source'))
price_db_info: The term 'price_db_info' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> print('diam_count=', len(diams))
ParserError: 
Line |
   1 |  print('diam_count=', len(diams))
     |                      ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('diam_unique=', uniq)
ParserError: 
Line |
   1 |  print('diam_unique=', uniq)
     |                       ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('flows_count=', len(signed))
ParserError: 
Line |
   1 |  print('flows_count=', len(signed))
     |                       ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('flows_sum=', psum)
ParserError: 
Line |
   1 |  print('flows_sum=', psum)
     |                     ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('flows_pos/neg/zero=', pos, neg, zer)
ParserError: 
Line |
   1 |  print('flows_pos/neg/zero=', pos, neg, zer)
     |                              ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('has_hydraulic_stats=', has_stats)
ParserError: 
Line |
   1 |  print('has_hydraulic_stats=', has_stats)
     |                               ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> # scan log markers
PS C:\PROJET_DIMENTIONEMENT_2> logp = Path('test_validation/logs')
logp: The term 'logp' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> marker1 = 'FLOW_CONSERVATION_BREACH'
marker1: The term 'marker1' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> marker2 = 'REPAIR_DIAMETERS_APPLIED'
marker2: The term 'marker2' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> found1 = found2 = False
found1: The term 'found1' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> if logp.exists():
ParserError: 
Line |
   1 |  if logp.exists():
     |    ~
     | Missing '(' after 'if' in if statement.
PS C:\PROJET_DIMENTIONEMENT_2>     for f in sorted(logp.glob('aep_network_optimize_unified_*.log.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
ParserError: 
Line |
   1 |      for f in sorted(logp.glob('aep_network_optimize_unified_*.log.jso …
     |         ~
     | Missing opening '(' after keyword 'for'.
PS C:\PROJET_DIMENTIONEMENT_2>         try:
try:: The term 'try:' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2>             t = f.read_text(encoding='utf-8', errors='ignore')
ParserError: 
Line |
   1 |              t = f.read_text(encoding='utf-8', errors='ignore')
     |                                              ~
     | Missing argument in parameter list.
PS C:\PROJET_DIMENTIONEMENT_2>             if marker1 in t: found1 = True
ParserError: 
Line |
   1 |              if marker1 in t: found1 = True
     |                ~
     | Missing '(' after 'if' in if statement.
PS C:\PROJET_DIMENTIONEMENT_2>             if marker2 in t: found2 = True
ParserError: 
Line |
   1 |              if marker2 in t: found2 = True
     |                ~
     | Missing '(' after 'if' in if statement.
PS C:\PROJET_DIMENTIONEMENT_2>         except Exception:
except: The term 'except' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2>             pass
pass: The term 'pass' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
PS C:\PROJET_DIMENTIONEMENT_2> print('log_FLOW_CONSERVATION_BREACH=', found1)
ParserError: 
Line |
   1 |  print('log_FLOW_CONSERVATION_BREACH=', found1)
     |                                        ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> print('log_REPAIR_DIAMETERS_APPLIED=', found2)
ParserError: 
Line |
   1 |  print('log_REPAIR_DIAMETERS_APPLIED=', found2)
     |                                        ~
     | Missing expression after ','.
PS C:\PROJET_DIMENTIONEMENT_2> PY
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> exit
PS C:\PROJET_DIMENTIONEMENT_2> ./venv_new/Scripts/python.exe -c "import json,math,sys; import pathlib as P; p=P.Path('results/test_integrated_stats.json'); d=json.load(open(p,'r',encoding='utf-8')) if p.exists() else {}; meta=d.get('meta',{}); props=d.get('proposals') or [{}]; hyd=d.get('hydraulics') or {}; flows=hyd.get('flows_m3_s') or hyd.get('flows') or []; val=lambda x:(x.get('value',0.0) if isinstance(x,dict) else x) or 0.0; s=sum(float(val(x)) for x in flows); diams=props[0].get('diameters_mm') or []; uniq=sorted({int(x) for x in diams}) if diams else []; print('best_cost=',meta.get('best_cost')); print('capex=',props[0].get('CAPEX')); print('constraints_ok=',props[0].get('constraints_ok')); pinfo=meta.get('price_db_info') or {}; print('price_db_info.type=',pinfo.get('type')); print('price_db_info.source=',pinfo.get('source')); print('diam_count=',len(diams)); print('diam_unique=',uniq); print('flows_count=',len(flows)); print('flows_sum=',s); print('has_hydraulic_stats=', bool(hyd.get('statistics'))); import glob; import pathlib; import io; log_files=sorted(pathlib.Path('test_validation/logs').glob('aep_network_optimize_unified_*.log.json'), key=lambda x:x.stat().st_mtime, reverse=True)[:3]; f1=f2=False; 
>> import codecs;
>> for f in log_files:
>>     try:
>>         t=codecs.open(f,'r','utf-8','ignore').read();
>>         if 'FLOW_CONSERVATION_BREACH' in t: f1=True
>>         if 'REPAIR_DIAMETERS_APPLIED' in t: f2=True
>>     except Exception: pass
>> print('log_FLOW_CONSERVATION_BREACH=',f1); print('log_REPAIR_DIAMETERS_APPLIED=',f2)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import json,math,sys; import pathlib as P; p=P.Path('results/test_integrated_stats.json'); d=json.load(open(p,'r',encoding='utf-8')) if p.exists() else {}; meta=d.get('meta',{}); props=d.get('proposals') or [{}]; hyd=d.get('hydraulics') or {}; flows=hyd.get('flows_m3_s') or hyd.get('flows') or []; val=lambda x:(x.get('value',0.0) if isinstance(x,dict) else x) or 0.0; s=sum(float(val(x)) for x in flows); diams=props[0].get('diameters_mm') or []; uniq=sorted({int(x) for x in diams}) if diams else []; print('best_cost=',meta.get('best_cost')); print('capex=',props[0].get('CAPEX')); print('constraints_ok=',props[0].get('constraints_ok')); pinfo=meta.get('price_db_info') or {}; print('price_db_info.type=',pinfo.get('type')); print('price_db_info.source=',pinfo.get('source')); print('diam_count=',len(diams)); print('diam_unique=',uniq); print('flows_count=',len(flows)); print('flows_sum=',s); print('has_hydraulic_stats=', bool(hyd.get('statistics'))); import glob; import pathlib; import io; log_files=sorted(pathlib.Path('test_validation/logs').glob('aep_network_optimize_unified_*.log.json'), key=lambda x:x.stat().st_mtime, reverse=True)[:3]; f1=f2=False;
                                                                                                                            
                                                                                                                            
                                                                                                                            
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 1, in <genexpr>
    import json,math,sys; import pathlib as P; p=P.Path('results/test_integrated_stats.json'); d=json.load(open(p,'r',encoding='utf-8')) if p.exists() else {}; meta=d.get('meta',{}); props=d.get('proposals') or [{}]; hyd=d.get('hydraulics') or {}; flows=hyd.get('flows_m3_s') or hyd.get('flows') or []; val=lambda x:(x.get('value',0.0) if isinstance(x,dict) else x) or 0.0; s=sum(float(val(x)) for x in flows); diams=props[0].get('diameters_mm') or []; uniq=sorted({int(x) for x in diams}) if diams else []; print('best_cost=',meta.get('best_cost')); print('capex=',props[0].get('CAPEX')); print('constraints_ok=',props[0].get('constraints_ok')); pinfo=meta.get('price_db_info') or {}; print('price_db_info.type=',pinfo.get('type')); print('price_db_info.source=',pinfo.get('source')); print('diam_count=',len(diams)); print('diam_unique=',uniq); print('flows_count=',len(flows)); print('flows_sum=',s); print('has_hydraulic_stats=', bool(hyd.get('statistics'))); import glob; import pathlib; import io; log_files=sorted(pathlib.Path('test_validation/logs').glob('aep_network_optimize_unified_*.log.json'), key=lambda x:x.stat().st_mtime, reverse=True)[:3]; f1=f2=False;
                                                                                                                            
                                                                                                                            
                                                                                                                            
        ~~~~~^^^^^^^^
ValueError: could not convert string to float: 'N142_N143'
PS C:\PROJET_DIMENTIONEMENT_2> powershell -NoProfile -Command "Write-Host 'JSON:' (Test-Path .\results\test_integrated_stats.json); if (Test-Path .\results\test_integrated_stats.json){(Get-Item .\results\test_integrated_stats.json).Length}; Write-Host 'LOG:' (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'); if (Test-Path 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'){(Get-Item 'C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json').Length}; $pdf=(Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1); Write-Host 'PDF:' ($pdf -ne $null); if ($pdf){$pdf.FullName; $pdf.Length}"
Au caractère Ligne:1 : 711
+ ... sc | Select-Object -First 1); Write-Host 'PDF:' ( -ne ); if (){.FullN ...
+                                                                  ~
Condition manquante dans l’instruction if après « if ( ».
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : IfStatementMissingCondition

PS C:\PROJET_DIMENTIONEMENT_2> powershell -NoProfile -Command "$json=Test-Path .\results\test_integrated_stats.json; Write-Host ('JSON: ' + $json); if($json){(Get-Item .\results\test_integrated_stats.json).Length | Write-Host}; $logp='C:\PROJET_DIMENTIONEMENT_2\test_validation\logs\aep_network_optimize_unified_20250821_130348.log.json'; $log=Test-Path $logp; Write-Host ('LOG: ' + $log); if($log){(Get-Item $logp).Length | Write-Host}; $pdf=(Get-ChildItem .\results\*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1); if($pdf){ Write-Host 'PDF: True'; $pdf.FullName; $pdf.Length } else { Write-Host 'PDF: False' }"                                                                                   
Au caractère Ligne:1 : 72
+ ...  .\results\test_integrated_stats.json; Write-Host ('JSON: ' + ); if() ...
+                                                                  ~
Vous devez indiquer une expression de valeur après l’opérateur « + ».
Au caractère Ligne:1 : 79
+ ... lts\test_integrated_stats.json; Write-Host ('JSON: ' + ); if(){(Get-I ...
+                                                                  ~
Condition manquante dans l’instruction if après « if ( ».
Au caractère Ligne:1 : 291
+ ... 20250821_130348.log.json'; =Test-Path ; Write-Host ('LOG: ' + ); if() ...
+                                                                  ~
Vous devez indiquer une expression de valeur après l’opérateur « + ».
Au caractère Ligne:1 : 298
+ ... 1_130348.log.json'; =Test-Path ; Write-Host ('LOG: ' + ); if(){(Get-I ...
+                                                                  ~
Condition manquante dans l’instruction if après « if ( ».
Au caractère Ligne:1 : 460
+ ... ort-Object LastWriteTime -Desc | Select-Object -First 1); if(){ Write ...
+                                                                  ~
Condition manquante dans l’instruction if après « if ( ».
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ExpectedValueExpression

PS C:\PROJET_DIMENTIONEMENT_2> powershell -NoProfile -Command "$jsonPath='results/test_integrated_stats.json'; if (Test-Path $jsonPath) { Write-Host 'JSON: True'; (Get-Item $jsonPath).Length } else { Write-Host 'JSON: False' }; $logPath='C:/PROJET_DIMENTIONEMENT_2/test_validation/logs/aep_network_optimize_unified_20250821_130348.log.json'; if (Test-Path $logPath) { Write-Host 'LOG: True'; (Get-Item $logPath).Length } else { Write-Host 'LOG: False' }; $pdfFile=Get-ChildItem results/*.pdf -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1; if ($pdfFile) { Write-Host 'PDF: True'; $pdfFile.FullName; $pdfFile.Length } else { Write-Host 'PDF: False' }"
Au caractère Ligne:1 : 465
+ ... ort-Object LastWriteTime -Desc | Select-Object -First 1; if () { Writ ...
+                                                                  ~
Condition manquante dans l’instruction if après « if ( ».
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : IfStatementMissingCondition

PS C:\PROJET_DIMENTIONEMENT_2> 



