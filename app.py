from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

fake_customer = {
    "first_name": "Mario",
    "last_name": "Rossi",
    "birth_date": "05/15/1980",
    "address": "Via Example 123, Milan",
    "email": "mario.rossi@example.com",
    "phone": "+393666742138",
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
