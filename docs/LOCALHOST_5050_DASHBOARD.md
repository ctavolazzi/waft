# Localhost 5050 Dashboard

## Purpose

The localhost 5050 dashboard provides a local-first control surface for:
- session context and timeline viewing,
- report generation and PDF download,
- safe command handoff back to Cursor (`copy -> paste -> run`).

## Start

Run:

```bash
waft dashboard-5050 --port 5050 --host localhost --open-browser
```

Open:

- Dashboard: `http://localhost:5050`
- API health: `http://localhost:5050/api/health`
- API docs: `http://localhost:5050/docs`

## Slash Command

Cursor slash command definition:

- `.cursor/commands/5050.md`

Using `/5050` should bootstrap the server + dashboard flow and return continuation guidance.

## API Endpoints

- `GET /api/5050/session`
- `GET /api/5050/timeline`
- `POST /api/5050/report`
- `POST /api/5050/report/pdf`
- `POST /api/5050/continue-command`
- `GET /api/5050/file?path=<relative_report_path>`

## Safe Handoff Loop

1. Click `Continue in Cursor`.
2. Dashboard copies command payload to clipboard.
3. Paste payload into Cursor chat.
4. Run command and continue cycle.

## Notes

- Report/PDF outputs are written under `_work_efforts/reports`.
- File downloads are restricted to `_work_efforts/reports` for safety.
