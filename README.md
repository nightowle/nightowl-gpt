# 🤖 NightOwl GitHub Manager – Custom GPT Action

**Ein Custom GPT Plugin**, das über die GitHub API auf Repositories und Dateien des Nutzers `nightowle` zugreift.  
Es erlaubt GPT, Dateien zu lesen, zu aktualisieren oder GitHub Actions Workflows auszuführen – direkt in deinem Repository.

---

## 🌐 Live Plugin-URL (für OpenAI GPT)

Manifest (für OpenAI Actions): https://nightowle.github.io/nightowl-gpt/.well-known/ai-plugin.json 


## 🔐 Authentifizierung
Standard: **Bearer‑Token (Fine‑Grained PAT)** via HTTP `Authorization: Bearer <token>`.
Erwartete Scopes: `repo`, `workflow`, optional `pages:write`.
Optionaler Fallback: OAuth (separates Manifest `.well-known/ai-plugin-oauth.json`).

## 🔑 Secrets
- `BLUE_QR_AUTOMATION`: Fine‑Grained PAT nicht im Klartext speichern; nur als Repository‑Secret.

## ⚡️ GitHub ↔ Zapier verbinden

Das Repository enthält eine REST-Route (`POST /repos/<owner>/<repo>/zapier_webhook`) sowie ein CLI-Skript,
um GitHub-Repository-Ereignisse an einen Zapier-Catch-Hook weiterzuleiten.

### Mit dem CLI-Skript

1. Python-Abhängigkeiten installieren (mindestens `requests`).
2. GitHub-Token als Umgebungsvariable setzen (`export GITHUB_TOKEN=...`) oder via `--token` übergeben.
3. Ausführen:

   ```bash
   python scripts/connect_zapier.py <owner> <repo> https://hooks.zapier.com/hooks/catch/.../
   ```

   Optional stehen `--events`, `--secret`, `--inactive` und `--insecure-ssl` zur Verfügung, um Events,
   Secret, Aktivierungsstatus oder SSL-Verhalten anzupassen.

### Über den REST-Endpunkt

```
POST /repos/<owner>/<repo>/zapier_webhook
{
  "zapier_hook_url": "https://hooks.zapier.com/hooks/catch/.../",
  "events": ["push", "pull_request"],
  "secret": "<optional-shared-secret>",
  "active": true
}
```

Antwort: GitHub-WebHook-Objekt (`201 Created`).
