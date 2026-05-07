import csv
import json
import re
import warnings
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = Path(__file__).parent / "mundial_2026.json"


# ---------------------------------------------------------------------------
# Fuente 1: HTML (Europa) // Se utilizo HTMLPARSER
# ---------------------------------------------------------------------------

class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headers = []
        self.rows = []
        self._cur_row = []
        self._cur_cell = ""
        self._in_cell = False
        self._in_header = False

    def handle_starttag(self, tag, attrs):
        if tag == "th":
            self._in_header = True
            self._cur_cell = ""
        elif tag == "td":
            self._in_cell = True
            self._cur_cell = ""

    def handle_endtag(self, tag):
        if tag == "th":
            self._in_header = False
            self.headers.append(self._cur_cell.strip())
        elif tag == "td":
            self._in_cell = False
            self._cur_row.append(self._cur_cell.strip())
        elif tag == "tr" and self._cur_row:
            self.rows.append(self._cur_row)
            self._cur_row = []

    def handle_data(self, data):
        if self._in_cell or self._in_header:
            self._cur_cell += data


def leer_html():
    """Lee fuente_html_europa.html → lista de dicts con club_actual."""
    parser = _TableParser()
    parser.feed((DATA_DIR / "fuente_html_europa.html").read_text(encoding="utf-8"))

    jugadores = []
    for row in parser.rows:
        if len(row) != 5:
            continue
        jugadores.append({
            "nombre":     row[0],
            "seleccion":  row[1],
            "posicion":   row[2],
            "edad":       int(row[3]),
            "club_actual": row[4],
            "fuente":     "europa",
        })
    return jugadores


# ---------------------------------------------------------------------------
# Fuente 2: CSV (Sudamérica) //
# ---------------------------------------------------------------------------

def leer_csv():
    """Lee fuente_csv_sudamerica.csv → lista de dicts con partidos."""
    jugadores = []
    with open(DATA_DIR / "fuente_csv_sudamerica.csv", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            jugadores.append({
                "nombre":    row["nombre"],
                "seleccion": row["seleccion"],
                "posicion":  row["posicion"],
                "edad":      int(row["edad"]),
                "partidos":  int(row["partidos"]),
                "fuente":    "sudamerica",
            })
    return jugadores


# ---------------------------------------------------------------------------
# Fuente 3: PDF (Norteamérica / Asia) // Se utilizo PdfReader
# ---------------------------------------------------------------------------

# Mapping for characters that lose their encoding in this PDF
_PDF_FIXES = {
    "M�xico": "México",
    "Mïxico": "México",
}

def _fix_pdf_text(text: str) -> str:
    for bad, good in _PDF_FIXES.items():
        text = text.replace(bad, good)
    # Catch any remaining "M?xico" pattern
    text = re.sub(r"M.xico", "México", text)
    return text


def leer_pdf():
    """Lee fuente_pdf_norteamerica_asia.pdf → lista de dicts con goles.

    pypdf extrae el texto con un valor por línea; el encabezado aparece solo
    en la primera página (Nombre / Seleccion / Posicion / Edad / Goles).
    """
    pdf_path = DATA_DIR / "fuente_pdf_norteamerica_asia.pdf"
    HEADER_FIELDS = {"nombre", "seleccion", "posicion", "edad", "goles"}
    FIELDS_ORDER = ["nombre", "seleccion", "posicion", "edad", "goles"]

    all_lines = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                line = _fix_pdf_text(line.strip())
                if line:
                    all_lines.append(line)

    # Skip header row (the 5 field-name lines that open page 0)
    data_lines = [l for l in all_lines if l.lower() not in HEADER_FIELDS]

    jugadores = []
    for i in range(0, len(data_lines) - 4, 5):
        chunk = data_lines[i:i + 5]
        if len(chunk) < 5:
            break
        nombre, seleccion, posicion, edad, goles = chunk
        jugadores.append({
            "nombre":    nombre,
            "seleccion": seleccion,
            "posicion":  posicion,
            "edad":      int(edad) if edad.isdigit() else None,
            "goles":     int(goles) if goles.isdigit() else None,
            "fuente":    "norteamerica_asia",
        })
    return jugadores


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    jugadores = leer_html() + leer_csv() + leer_pdf()

    output = {"docs": jugadores}
    OUTPUT_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Total de jugadores: {len(jugadores)}")
    print(f"  Europa (HTML):            {sum(1 for j in jugadores if j['fuente'] == 'europa')}")
    print(f"  Sudamérica (CSV):         {sum(1 for j in jugadores if j['fuente'] == 'sudamerica')}")
    print(f"  Norteamérica/Asia (PDF):  {sum(1 for j in jugadores if j['fuente'] == 'norteamerica_asia')}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
