from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

fake_customer = {
    "nome": "Mario",
    "cognome": "Rossi",
    "data_nascita": "15/05/1980",
    "indirizzo": "Via Example 123, Milano",
    "email": "mario.rossi@email.com",
    "telefono": "+39 347 1234567",
    "conto_corrente": "IT60X0542811101000000123456",
    "saldo": "€ 5.432,78",
    "ultime_transazioni": [
        {"data": "2026-03-18", "descrizione": "Stipendio", "importo": "+ € 2.500,00"},
        {"data": "2026-03-15", "descrizione": "Supermercato", "importo": "- € 45,20"},
        {"data": "2026-03-10", "descrizione": "POS Ristorante", "importo": "- € 67,90"},
    ]
}

BASE_CSS = """
    <style>
        :root {
            --green: #008652;
            --orange: #E98A42;
            --yellow: #DEB630;
            --blue: #01669B;
            --bg: #f5f6f7;
            --text: #1f2933;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
        }
        .layout {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: white;
            border-bottom: 3px solid var(--green);
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }
        .topbar {
            max-width: 1100px;
            margin: 0 auto;
            padding: 14px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand-mark {
            width: 32px;
            height: 32px;
            border-radius: 4px;
            border: 2px solid var(--green);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
            color: var(--green);
        }
        .brand-text {
            font-size: 20px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--green);
        }
        .nav {
            display: flex;
            gap: 18px;
            font-size: 14px;
        }
        .nav a {
            text-decoration: none;
            color: #4b5563;
        }
        .nav a.active {
            color: var(--blue);
            font-weight: 600;
        }
        .hero-bar {
            background: linear-gradient(90deg, #ffffff 0%, #f0f7f4 40%, #e7f2ff 100%);
            border-top: 1px solid #e5e7eb;
        }
        .hero-inner {
            max-width: 1100px;
            margin: 0 auto;
            padding: 18px 20px 14px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .hero-title {
            font-size: 20px;
            font-weight: 600;
            color: var(--blue);
        }
        .hero-sub {
            font-size: 13px;
            color: #6b7280;
        }
        main {
            flex: 1;
        }
        .main-inner {
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px 20px 40px;
            display: grid;
            grid-template-columns: 2.2fr 1.3fr;
            gap: 20px;
        }
        @media (max-width: 900px) {
            .main-inner {
                grid-template-columns: 1fr;
            }
        }
        .card {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(15,23,42,0.06);
            border: 1px solid #e5e7eb;
            padding: 18px 20px 16px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 10px;
        }
        .card-title {
            font-size: 15px;
            font-weight: 600;
            color: #111827;
        }
        .card-meta {
            font-size: 11px;
            color: #9ca3af;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 11px;
            background: rgba(0,134,82,0.06);
            color: var(--green);
            border: 1px solid rgba(0,134,82,0.28);
        }
        .pill-dot {
            width: 6px;
            height: 6px;
            border-radius: 999px;
            background: var(--green);
        }
        .details-grid {
            display: grid;
            grid-template-columns: 1.2fr 1.8fr;
            gap: 10px 24px;
            font-size: 13px;
        }
        .label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #9ca3af;
        }
        .value {
            font-size: 13px;
            color: #111827;
        }
        .badge-id {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 9px;
            border-radius: 999px;
            background: #eff6ff;
            color: var(--blue);
            font-size: 11px;
        }
        .badge-id span {
            font-weight: 600;
        }
        table.tx {
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
            font-size: 12px;
        }
        table.tx thead {
            background: #f3f4f6;
        }
        table.tx th, table.tx td {
            padding: 6px 8px;
            text-align: left;
        }
        table.tx th {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #6b7280;
        }
        table.tx tbody tr:nth-child(even) {
            background: #f9fafb;
        }
        .amount-pos { color: #059669; font-weight: 600; }
        .amount-neg { color: #b91c1c; font-weight: 600; }
        .sidebar-section + .sidebar-section {
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px dashed #e5e7eb;
        }
        .search-input {
            width: 100%;
            padding: 8px 10px;
            font-size: 13px;
            border-radius: 999px;
            border: 1px solid #d1d5db;
            outline: none;
        }
        .search-input:focus {
            border-color: var(--green);
            box-shadow: 0 0 0 1px rgba(0,134,82,0.2);
        }
        .hint {
            font-size: 11px;
            color: #9ca3af;
            margin-top: 6px;
        }
        footer {
            border-top: 1px solid #e5e7eb;
            background: white;
        }
        .footer-inner {
            max-width: 1100px;
            margin: 0 auto;
            padding: 10px 20px 14px;
            font-size: 11px;
            color: #9ca3af;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }
        .status-pill {
            padding: 2px 8px;
            border-radius: 999px;
            border: 1px solid #e5e7eb;
        }
    </style>
"""

def format_timestamp(ts: int | None) -> str:
    if not ts:
        return "Non fornito"
    try:
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return "Non valido"


@app.get("/", response_class=HTMLResponse)
async def home(
    id: str | None = Query(None, description="ID cliente"),
    timestamp: int | None = Query(None, description="Timestamp Unix")
):
    ts_str = format_timestamp(timestamp)

    if id == "12345":
        # Vista anagrafica cliente
        full_name = f"{fake_customer['nome']} {fake_customer['cognome']}"
        saldo = fake_customer["saldo"]
        tx_rows = ""
        for tx in fake_customer["ultime_transazioni"]:
            amount_cls = "amount-pos" if "+" in tx["importo"] else "amount-neg"
            tx_rows += f"""
                <tr>
                    <td>{tx['data']}</td>
                    <td>{tx['descrizione']}</td>
                    <td class="{amount_cls}">{tx['importo']}</td>
                </tr>
            """

        main_html = f"""
        <div class="main-inner">
            <section class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Profilo cliente</div>
                        <div class="card-meta">Vista sintetica anagrafica e rapporti</div>
                    </div>
                    <div class="pill">
                        <span class="pill-dot"></span>
                        Cliente identificato
                    </div>
                </div>

                <div class="details-grid">
                    <div>
                        <div class="label">Intestatario</div>
                        <div class="value">{full_name}</div>
                    </div>
                    <div>
                        <div class="label">ID cliente</div>
                        <div class="value">
                            <span class="badge-id">
                                ID <span>{id}</span>
                            </span>
                        </div>
                    </div>
                    <div>
                        <div class="label">Data di nascita</div>
                        <div class="value">{fake_customer['data_nascita']}</div>
                    </div>
                    <div>
                        <div class="label">Indirizzo</div>
                        <div class="value">{fake_customer['indirizzo']}</div>
                    </div>
                    <div>
                        <div class="label">Email</div>
                        <div class="value">{fake_customer['email']}</div>
                    </div>
                    <div>
                        <div class="label">Telefono</div>
                        <div class="value">{fake_customer['telefono']}</div>
                    </div>
                    <div>
                        <div class="label">Conto corrente</div>
                        <div class="value">{fake_customer['conto_corrente']}</div>
                    </div>
                    <div>
                        <div class="label">Saldo disponibile</div>
                        <div class="value">{saldo}</div>
                    </div>
                    <div>
                        <div class="label">Timestamp richiesta</div>
                        <div class="value">{ts_str}</div>
                    </div>
                </div>

                <div style="margin-top:16px;">
                    <div class="label">Ultime operazioni</div>
                    <table class="tx">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Descrizione</th>
                                <th>Importo</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tx_rows}
                        </tbody>
                    </table>
                </div>
            </section>

            <aside class="card">
                <div class="sidebar-section">
                    <div class="card-title" style="font-size:14px;">Azioni rapide</div>
                    <div class="hint">Seleziona una voce per simulare le operazioni tipiche di sportello.</div>
                </div>
                <div class="sidebar-section" style="font-size:13px;">
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; margin-top:6px;">
                        <li>• Simula bonifico SEPA</li>
                        <li>• Visualizza esposizione carte</li>
                        <li>• Verifica recapiti cliente</li>
                        <li>• Apri posizione investimenti</li>
                    </ul>
                </div>
                <div class="sidebar-section">
                    <div class="label">Parametro di ricerca</div>
                    <div class="value">id=12345 · {ts_str}</div>
                    <p class="hint">Modifica l'ID nella URL per vedere la vista “Ricerca clienti”.</p>
                </div>
            </aside>
        </div>
        """
        page_title = "Area clienti · Banca Demo"
        hero_title = "Profilo cliente"
        hero_sub = "Stai visualizzando i dati sintetici del cliente identificato."

    else:
        # Vista customSearch
        display_id = id or "—"
        main_html = f"""
        <div class="main-inner">
            <section class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Ricerca clienti</div>
                        <div class="card-meta">Inserisci un identificativo per simulare la ricerca anagrafica</div>
                    </div>
                    <div class="pill" style="background:rgba(1,102,155,0.06);border-color:rgba(1,102,155,0.28);color:var(--blue);">
                        <span class="pill-dot" style="background:var(--blue);"></span>
                        Nessun cliente selezionato
                    </div>
                </div>

                <div style="max-width:420px; margin-top:4px;">
                    <div class="label">ID cliente attuale</div>
                    <div class="value" style="margin-bottom:8px;">{display_id}</div>
                    <form onsubmit="event.preventDefault(); var v=document.getElementById('id-input').value; var ts={timestamp or ''}; var qs='?id='+encodeURIComponent(v); if(ts){{qs+='&timestamp='+ts;}} window.location.search = qs;">
                        <input id="id-input" class="search-input" placeholder="Inserisci un ID cliente (es. 12345)" />
                    </form>
                    <p class="hint">Suggerimento: prova con <strong>12345</strong> per caricare l'anagrafica di Mario Rossi.</p>
                </div>

                <div style="margin-top:18px;">
                    <div class="label">Esito simulato</div>
                    <p class="value" style="margin-top:4px;">
                        Nessun record trovato per l'ID inserito. Questa vista rappresenta una
                        schermata di ricerca anagrafica “tipo CRM” da agganciare a sistemi reali.
                    </p>
                </div>
            </section>

            <aside class="card">
                <div class="sidebar-section">
                    <div class="card-title" style="font-size:14px;">Stato sessione</div>
                    <div class="value" style="margin-top:4px;">
                        <span class="status-pill">Timestamp: {ts_str}</span>
                    </div>
                    <p class="hint">Se non passi alcun timestamp, viene mostrato “Non fornito”.</p>
                </div>
                <div class="sidebar-section">
                    <div class="card-title" style="font-size:14px;">Parametri URL</div>
                    <p class="hint">
                        Esempio: <code>?id=12345&amp;timestamp=1742478300</code><br>
                        Puoi usare questi parametri da Genesys, da un CRM o da qualsiasi altro sistema.
                    </p>
                </div>
            </aside>
        </div>
        """
        page_title = "Ricerca clienti · Banca Demo"
        hero_title = "Area clienti online"
        hero_sub = "Simulazione di interfaccia bancaria per ricerca e visualizzazione profilo."

    html = f"""
    <html lang="it">
      <head>
        <meta charset="utf-8" />
        <title>{page_title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        {BASE_CSS}
      </head>
      <body>
        <div class="layout">
          <header>
            <div class="topbar">
              <div class="brand">
                <div class="brand-mark">BD</div>
                <div class="brand-text">BANCA DEMO</div>
              </div>
              <nav class="nav">
                <a href="/" class="active">Clienti</a>
                <a href="#">Prodotti</a>
                <a href="#">Supporto</a>
              </nav>
            </div>
            <div class="hero-bar">
              <div class="hero-inner">
                <div class="hero-title">{hero_title}</div>
                <div class="hero-sub">{hero_sub}</div>
              </div>
            </div>
          </header>

          <main>
            {main_html}
          </main>

          <footer>
            <div class="footer-inner">
              <div>Interfaccia demo ispirata a portali bancari italiani.</div>
              <div>Ambiente di test · Non utilizzare dati reali di clienti.</div>
            </div>
          </footer>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
