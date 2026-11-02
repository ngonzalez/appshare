# API-Leitfaden

Lesen Sie die Daten Ihres Kontos als JSON mit HTTPS-Anfragen

### Themenliste

- Holen Sie sich einen API-Token
- Senden Sie Ihre Anfragen ein
- Die Ressourcen deines Kontos
- Probier es mal mit Postboten

#### Holen Sie sich einen API-Token

Öffne im Webadministrator den **Tab Zugangsdaten** und aktiviere die API: Dein Token wird dort angezeigt. Es ist persönlich: Es liest die Daten deines Kontos als du. Es läuft nach einem Jahr ab, und du kannst jederzeit ein neues Konto erstellen (das vorherige funktioniert dann nicht mehr).

#### Senden Sie Ihre Anfragen ein

Senden Sie das Token in den `Authorization` -Header jeder Anfrage:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" https://api.appshare.site/api/v1/accounts.json
```

Eine Anfrage ohne gültiges Token wird mit 401-Status abgelehnt.

#### Die Ressourcen deines Kontos

Jede Ressource ist unter `https://api.appshare.site/api/v1/<resource>.json`aufgeführt, und eine davon unter `/api/v1/<resource>/<id>.json`:

| Ressource | Was |
|---------------------|------------------------------------------------|
| `accounts` | Ihr Konto |
| `users` | seine Nutzer |
| `folders` | seine Ordner und deren Dateien |
| `uploads` | die Uploads |
| `html_files` | die Logos und HTML-Blöcke Ihrer Website |
| `meta_tags` | die Meta-Tags deiner Seiten |
| `links` | die Links in deinem Footer |
| `settings` | die Farben Ihrer Website |
| `csv_files` | die CSV exportiert |
| `excel_files` | exportiert Excel |
| `events` | die Events (Besuche, Downloads) Ihrer Seiten |
| `daily_events` | die Ereignisse, Tag für Tag |
| `url_daily_events` | die Ereignisse, Tag für Tag und für Seite |

#### Probier es mal mit Postboten

Laden Sie den Postman-HTTP-Client unter [postman.com](https://www.postman.com) herunter, fügen Sie Ihr **Token im Autorisierungstab der Anfrage** hinzu (tippen *Sie Bearer Token*) und fordern Sie Ihr Konto unter [api/v1/accounts](https://api.appshare.site/api/v1/accounts.json) an.
