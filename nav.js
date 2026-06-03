/**
 * nav.js — shared top navigation bar
 * Include in any page with: <script src="nav.js"></script>
 * Place just before </body>. Detects the current page for the active link.
 */
(function () {
    const page = location.pathname.split('/').pop() || 'index.html';

    const style = document.createElement('style');
    style.textContent = `
        #site-nav {
            background: #1e293b;
            border-bottom: 1px solid #334155;
            padding: 0 20px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .snav-inner {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 52px;
        }
        .snav-brand {
            font-weight: 700;
            color: #f1f5f9;
            font-size: 1.05em;
            text-decoration: none;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        .snav-links {
            display: flex;
            gap: 4px;
        }
        .snav-links a {
            padding: 6px 14px;
            border-radius: 8px;
            color: #94a3b8;
            text-decoration: none;
            font-size: 0.9em;
            font-weight: 500;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            transition: background 0.15s, color 0.15s;
        }
        .snav-links a:hover { background: #334155; color: #f1f5f9; }
        .snav-links a.snav-active { background: #3b82f6; color: #fff; }
        @media (max-width: 480px) {
            .snav-brand-text { display: none; }
            .snav-links a { padding: 6px 10px; font-size: 0.85em; }
        }
    `;
    document.head.appendChild(style);

    const nav = document.createElement('nav');
    nav.id = 'site-nav';
    nav.innerHTML = `
        <div class="snav-inner">
            <a href="index.html" class="snav-brand">📊 <span class="snav-brand-text">투자 대시보드</span></a>
            <div class="snav-links">
                <a href="index.html" class="${(page === 'index.html' || page === '') ? 'snav-active' : ''}">📈 한국 주식</a>
                <a href="crypto.html" class="${page === 'crypto.html' ? 'snav-active' : ''}">₿ 암호화폐</a>
            </div>
        </div>
    `;

    document.body.insertBefore(nav, document.body.firstChild);
})();
