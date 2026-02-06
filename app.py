from flask import Flask, render_template_string, request, send_file
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

app = Flask(__name__)

DATA_FILE = "donnees_sondage.xlsx"

HTML_FORM = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Sondage FESTICAD 5</title>
</head>
<body>
    <h2>Sondage de taux de satisfaction du FESTICAD 5</h2>
    <form method="post">
        <label>Nom :</label><br>
        <input type="text" name="nom" required><br><br>

        <label>Prénoms :</label><br>
        <input type="text" name="prenoms" required><br><br>

        <label>Provenance :</label><br>
        <input type="text" name="provenance" required><br><br>

        <label>Téléphone :</label><br>
        <input type="text" name="tel" required><br><br>

        <label>WhatsApp :</label><br>
        <input type="text" name="whatsapp" required><br><br>

        <label>Avis de satisfaction :</label><br>
        <input type="radio" name="avis" value="Très satisfait" required> Très satisfait<br>
        <input type="radio" name="avis" value="Satisfaction moyenne"> Satisfaction moyenne<br>
        <input type="radio" name="avis" value="Pas satisfait"> Pas satisfait<br><br>

        <button type="submit">Envoyer</button>
    </form>
    <br>
    <a href="/export/excel">📥 Télécharger Excel</a> |
    <a href="/export/pdf">📄 Télécharger PDF</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "Nom": request.form['nom'],
            "Prénoms": request.form['prenoms'],
            "Provenance": request.form['provenance'],
            "Date": datetime.now().strftime("%d/%m/%Y"),
            "Téléphone": request.form['tel'],
            "WhatsApp": request.form['whatsapp'],
            "Avis": request.form['avis']
        }

        if os.path.exists(DATA_FILE):
            df = pd.read_excel(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])

        df.to_excel(DATA_FILE, index=False)

    return render_template_string(HTML_FORM)

@app.route('/export/excel')
def export_excel():
    return send_file(DATA_FILE, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    df = pd.read_excel(DATA_FILE)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, "Sondage de taux de satisfaction du FESTICAD 5", ln=True)

    for _, row in df.iterrows():
        for col in df.columns:
            pdf.cell(0, 8, f"{col} : {row[col]}", ln=True)
        pdf.ln(3)

    pdf_file = "donnees_sondage.pdf"
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run()
