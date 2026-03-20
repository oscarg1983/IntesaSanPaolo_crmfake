from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

fake_customer = {
    "first_name": "Mario",
    "last_name": "Rossi",
    "birth_date": "05/15/1980",
    "address": "Via Example 123, Milan",
    "email": "mario.rossi@email.com",
    "phone": "+39 347 1234567",
    "current_account": "IT60X0542811101000000123456",
    "balance": "€ 5,432.78",
    "recent_transactions": [
        {"date": "2026-03-18", "description": "Salary", "amount": "+ € 2,500.00"},
        {"date": "2026-03-15", "description": "Supermarket", "amount": "- € 45.20"},
        {"date": "2026-03-10", "description": "POS Restaurant", "amount": "- € 67.90"},
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
        return "Not provided"
    try:
        return datetime.fromtimestamp(ts).strftime("%m/%d/%Y %H:%M:%S")
    except Exception:
        return "Invalid"

@app.get("/", response_class=HTMLResponse)
async def home(
    id: str | None = Query(None, description="Customer ID"),
    timestamp: int | None = Query(None, description="Unix timestamp")
):
    ts_str = format_timestamp(timestamp)

    if id == "12345":
        # Customer profile view
        full_name = f"{fake_customer['first_name']} {fake_customer['last_name']}"
        balance = fake_customer["balance"]
        tx_rows = ""
        for tx in fake_customer["recent_transactions"]:
            amount_cls = "amount-pos" if "+" in tx["amount"] else "amount-neg"
            tx_rows += f"""
                <tr>
                    <td>{tx['date']}</td>
                    <td>{tx['description']}</td>
                    <td class="{amount_cls}">{tx['amount']}</td>
                </tr>
            """

        main_html = f"""
        <div class="main-inner">
            <section class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Customer Profile</div>
                        <div class="card-meta">Customer details and account summary</div>
                    </div>
                    <div class="pill">
                        <span class="pill-dot"></span>
                        Customer identified
                    </div>
                </div>

                <div class="details-grid">
                    <div>
                        <div class="label">Account holder</div>
                        <div class="value">{full_name}</div>
                    </div>
                    <div>
                        <div class="label">Customer ID</div>
                        <div class="value">
                            <span class="badge-id">
                                ID <span>{id}</span>
                            </span>
                        </div>
                    </div>
                    <div>
                        <div class="label">Birth date</div>
                        <div class="value">{fake_customer['birth_date']}</div>
                    </div>
                    <div>
                        <div class="label">Address</div>
                        <div class="value">{fake_customer['address']}</div>
                    </div>
                    <div>
                        <div class="label">Email</div>
                        <div class="value">{fake_customer['email']}</div>
                    </div>
                    <div>
                        <div class="label">Phone</div>
                        <div class="value">{fake_customer['phone']}</div>
                    </div>
                    <div>
                        <div class="label">Current account</div>
                        <div class="value">{fake_customer['current_account']}</div>
                    </div>
                    <div>
                        <div class="label">Available balance</div>
                        <div class="value">{balance}</div>
                    </div>
                    <div>
                        <div class="label">Request timestamp</div>
                        <div class="value">{ts_str}</div>
                    </div>
                </div>

                <div style="margin-top:16px;">
                    <div class="label">Recent transactions</div>
                    <table class="tx">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Amount</th>
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
                    <div class="card-title" style="font-size:14px;">Quick actions</div>
                    <div class="hint">Select an option to simulate typical banking operations.</div>
                </div>
                <div class="sidebar-section" style="font-size:13px;">
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; margin-top:6px;">
                        <li>• Simulate SEPA transfer</li>
                        <li>• View credit card exposure</li>
                        <li>• Verify customer contacts</li>
                        <li>• Open investment position</li>
                    </ul>
                </div>
                <div class="sidebar-section">
                    <div class="label">Search parameter</div>
                    <div class="value">id=12345 · {ts_str}</div>
                    <p class="hint">Change the ID in the URL to see the "Customer search" view.</p>
                </div>
            </aside>
        </div>
        """
        page_title = "Customers · Demo Bank"
        hero_title = "Customer Profile"
        hero_sub = "You are viewing the synthetic data of the identified customer."

    else:
        # Customer search view
        display_id = id or "—"
        main_html = f"""
        <div class="main-inner">
            <section class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">Customer Search</div>
                        <div class="card-meta">Enter an identifier to simulate customer lookup</div>
                    </div>
                    <div class="pill" style="background:rgba(1,102,155,0.06);border-color:rgba(1,102,155,0.28);color:var(--blue);">
                        <span class="pill-dot" style="background:var(--blue);"></span>
                        No customer selected
                    </div>
                </div>

                <div style="max-width:420px; margin-top:4px;">
                    <div class="label">Current customer ID</div>
                    <div class="value" style="margin-bottom:8px;">{display_id}</div>
                    <form onsubmit="event.preventDefault(); var v=document.getElementById('id-input').value; var ts={timestamp or ''}; var qs='?id='+encodeURIComponent(v); if(ts){{qs+='&timestamp='+ts;}} window.location.search = qs;">
                        <input id="id-input" class="search-input" placeholder="Enter customer ID (e.g. 12345)" />
                    </form>
                    <p class="hint">Tip: try <strong>12345</strong> to load Mario Rossi's profile.</p>
                </div>

                <div style="margin-top:18px;">
                    <div class="label">Simulated result</div>
                    <p class="value" style="margin-top:4px;">
                        No records found for the entered ID. This view represents a typical CRM customer search screen to connect to real systems.
                    </p>
                </div>
            </section>

            <aside class="card">
                <div class="sidebar-section">
                    <div class="card-title" style="font-size:14px;">Session status</div>
                    <div class="value" style="margin-top:4px;">
                        <span class="status-pill">Timestamp: {ts_str}</span>
                    </div>
                    <p class="hint">If no timestamp is passed, it shows "Not provided".</p>
                </div>
                <div class="sidebar-section">
                    <div class="card-title" style="font-size:14px;">URL parameters</div>
                    <p class="hint">
                        Example: <code>?id=12345&amp;timestamp=1742478300</code><br>
                        You can use these parameters from Genesys, CRM, or any other system.
                    </p>
                </div>
            </aside>
        </div>
        """
        page_title = "Customer Search · Demo Bank"
        hero_title = "Online Banking Area"
        hero_sub = "Banking interface simulation for customer search and profile display."

    html = f"""
    <html lang="en">
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
                <div class="brand-text">DEMO BANK</div>
              </div>
              <nav class="nav">
                <a href="/" class="active">Customers</a>
                <a href="#">Products</a>
                <a href="#">Support</a>
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
              <div>Demo interface inspired by Italian banking portals.</div>
              <div>Test environment · Do not use real customer data.</div>
            </div>
          </footer>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
