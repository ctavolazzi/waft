# Realm-Port System: Gamified Service Mesh

**Every Realm is a Port. Every Being is a Microservice.**

## Architecture

Each Realm runs as an active PocketBase server on its own port:
- `daily_learning_realm` → Port 8090 (Packrat's home)
- `library_realm` → Port 8091 (Librarian's domain, lazy-loaded)
- `security_realm` → Port 8080 (Gatekeeper, future)

## Critical Implementation Details

### 1. Bootstrap (CRITICAL)

**Problem:** PocketBase doesn't allow anonymous API writes. Admin must exist before API calls.

**Solution:** `RealmServer.bootstrap()` uses `pocketbase superuser upsert` command to create admin **BEFORE** server starts accepting API calls.

**First Run:**
1. Server downloads PocketBase binary
2. Bootstrap creates admin user via CLI
3. Server starts
4. API client authenticates successfully

**If Bootstrap Fails:**
- Check console output for errors
- Manually open `http://localhost:8090/_/` and create admin
- Check `_realms/{realm_name}/pocketbase.log` for details

### 2. Zombie Process Prevention

**Problem:** If Python script crashes, PocketBase subprocess stays alive, blocking port.

**Solution:** `atexit` handler ensures child processes are killed on exit.

**If Port is Blocked:**
```bash
# Kill all PocketBase processes
pkill pocketbase

# Or kill specific port
lsof -ti:8090 | xargs kill
```

### 3. Lazy Loading

**Library Realm** (Port 8091) only starts when Packrat visits Librarian:
- Saves memory (Scale-to-Zero pattern)
- Mimics Serverless architecture
- Stops automatically after report generation

**Daily Learning Realm** (Port 8090) stays alive all day (Packrat's home).

## Usage

### Start Packrat
```bash
waft packrat
```

### View Packrat's Backpack
Open browser: `http://localhost:8090/_/`

You'll see:
- Admin UI
- `inventory` collection
- Real-time data as Packrat collects

### Debugging

**Check if server is running:**
```bash
curl http://localhost:8090/api/health
```

**View logs:**
```bash
tail -f _realms/daily_learning_realm/pocketbase.log
```

**Check port registry:**
```bash
cat src/waft/core/realms/port_registry.json
```

## Troubleshooting

### "Address already in use"
- Zombie process detected
- Run: `pkill pocketbase`

### "403 Forbidden" on API calls
- Admin user doesn't exist
- Check bootstrap logs
- Manually create admin at `http://localhost:8090/_/`

### "Failed to authenticate"
- Server may not be ready yet
- Wait 2-3 seconds after server start
- Check server logs for errors

## Future Enhancements

- **Gatekeeper Being** (Port 8080): Reverse proxy for security
- **Core Database Realm**: The One's main database
- **Backup Scheduling**: Automated backups of Realm data
- **Service Discovery**: Automatic port assignment and health checks
