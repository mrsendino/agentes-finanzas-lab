"""Verifica el análisis de una empresa.

Uso:  python herramientas/verificar.py <empresa>     (p. ej. tesla)

1. Copia empresas/<empresa>/ a una carpeta temporal y ejecuta allí, en orden, los scripts
   fase2*, fase3* y fase4* (sin tocar los ficheros del repo). Falla si alguno termina con error.
2. Si existe un comprobador de cifras (scripts/fase5*_cifras.py), lo ejecuta y falla si su línea
   TOTAL informa de algún MISMATCH o DOBLE REDONDEO.

Devuelve 0 si todo cuadra y 1 si no, para poder usarlo en GitHub Actions o antes de un commit.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ejecutar(script, cwd, env):
    print(f"▶ {os.path.relpath(script, cwd)}")
    r = subprocess.run([sys.executable, script], cwd=cwd, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout[-2000:])
        print(r.stderr[-2000:])
    return r


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    empresa = sys.argv[1].lower()
    origen = os.path.join(RAIZ, "empresas", empresa)
    if not os.path.isdir(origen):
        print(f"No existe empresas/{empresa}")
        return 2

    env = dict(os.environ, DCF_NO_RECALC="1", PYTHONIOENCODING="utf-8")
    fallos = []

    tmp = tempfile.mkdtemp(prefix=f"verificar_{empresa}_")
    try:
        copia = os.path.join(tmp, empresa)
        shutil.copytree(origen, copia)
        for patron in ("fase2*.py", "fase3*.py", "fase4*.py"):
            for script in sorted(glob.glob(os.path.join(copia, "scripts", patron))):
                if ejecutar(script, copia, env).returncode != 0:
                    fallos.append(f"{os.path.basename(script)} terminó con error")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for script in sorted(glob.glob(os.path.join(origen, "scripts", "fase5*_cifras.py"))):
        r = ejecutar(script, origen, env)
        total = [l for l in r.stdout.splitlines() if l.startswith("TOTAL")]
        if r.returncode != 0:
            fallos.append(f"{os.path.basename(script)} terminó con error")
        elif total:
            print("  " + total[-1])
            for etiqueta in ("MISMATCH", "DOBLE REDONDEO"):
                m = re.search(rf"{etiqueta} (\d+)", total[-1])
                if m and int(m.group(1)) > 0:
                    fallos.append(f"{m.group(1)} cifras con {etiqueta}")

    if fallos:
        print("\n✗ NECESITA TRABAJO:\n  - " + "\n  - ".join(fallos))
        return 1
    print("\n✓ Todo cuadra")
    return 0


if __name__ == "__main__":
    sys.exit(main())
