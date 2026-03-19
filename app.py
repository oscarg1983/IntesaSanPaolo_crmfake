from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from datetime import datetime
import uuid

app = FastAPI()

fake_customer = {
    "nome": "Mario Rossi",
    "cognome": "Rossi",
    "data_nascita": "15/05/1980",
    "indirizzo": "Via Example 123, Milano",
    "email": "mario.rossi@email.com",
    "telefono": "+393471234567",
    "conto_corrente": "IT60X0542811101000000123456",
    "saldo": "€5.432,78",
    "ultime_transazioni": [
        {"data": "2026-03-18", "descrizione": "Stipendio", "importo": "+€2.500,00"},
        {"data": "2026-03-15", "descrizione": "Supermercato", "importo": "-€45,20"}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def home(
    id: str = Query(None, description="ID cliente"),
    timestamp: int = Query(None, description="Timestamp Unix")
):
    if timestamp:
        ts_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    else:
        ts_str = "Non fornito"
    
    if id == "12345":
        content = f"""
        <h1>Anagrafica Cliente</h1>
        <p><strong>ID:</strong> {id}</p>
        <p><strong>Timestamp:</strong> {ts_str}</p>
        <ul>
            <li>Nome: {fake_customer['nome']} {fake_customer['cognome']}</li>
            <li>Data nascita: {fake_customer['data_nascita']}</li>
            <li>Indirizzo: {fake_customer['indirizzo']}</li>
            <li>Email: {fake_customer['email']}</li>
            <li>Telefono: {fake_customer['telefono']}</li>
            <li>Conto: {fake_customer['conto_corrente']}</li>
            <li>Saldo: {fake_customer['saldo']}</li>
        </ul>
        <h2>Ultime transazioni</h2>
        <ul>
        """
        for tx in fake_customer['ultime_transazioni']:
            content += f"<li>{tx['data']} - {tx['descrizione']}: {tx['importo']}</li>"
        content += "</ul>"
    else:
        search_query = id or "vuoto"
        content = f"""
        <h1>Custom Search</h1>
        <p><strong>ID ricercato:</strong> {id or 'nessuno'}</p>
        <p><strong>Timestamp:</strong> {ts_str}</p>
        <p>Risultati per: <em>{search_query}</em></p>
        <p>Nessun cliente trovato. Prova con id=12345.</p>
        """
    
    return HTMLResponse(content=f"""
    <html>
        <head><title>App Cliente</title></head>
        <body>{content}</body>
    </html>
    """)
