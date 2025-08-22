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
