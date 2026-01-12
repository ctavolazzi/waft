# Verification Trace: Akasha File Permissions

**Date**: 2026-01-11 16:09:07 PST
**Check ID**: verify-0005
**Status**: ✅ Verified

## Claim
Soul records stored in Akasha (JSON files) need secure file permissions (0600/0700).

## Verification Method
1. Examined soul file creation in `KarmaCollector._transfer_karma_to_soul()`
2. Checked for file permission setting
3. Examined Akasha path structure

## Evidence

### KarmaCollector._transfer_karma_to_soul()
```python
def _transfer_karma_to_soul(...):
    soul_file = self.akasha_path / f"{soul_id}.json"
    
    if soul_file.exists():
        with open(soul_file, "r") as f:
            soul_data = json.load(f)
    else:
        soul_data = {
            "soul_id": soul_id,
            "total_karma": 0.0,
            "lifetimes": [],
            "created_at": datetime.now().isoformat()
        }
    
    # ... modify soul_data ...
    
    # Save soul record
    with open(soul_file, "w") as f:
        json.dump(soul_data, f, indent=2)
    # ⚠️ NO file permission setting
```

### Akasha Path
```python
# From KarmaCollector
self.akasha_path = project_path / "_hidden" / ".truth" / "akasha"
```

## Result

**FINDING**:
- ✅ Soul files are created in `_hidden/.truth/akasha/`
- ❌ **NO file permissions are set** (uses default OS permissions)
- ❌ **NO file locking** during writes
- ❌ **NO integrity validation** on reads
- ⚠️ **SECURITY GAP**: Files are world-readable by default (typically 0644)

**VERIFICATION**: Assumption is **CORRECT**
- We DO need to set file permissions
- We DO need file locking
- We DO need integrity validation

## Recommendation

**Security Hardening Required**:
1. Set file permissions after creation:
   ```python
   soul_file.write_text(json.dumps(soul_data, indent=2))
   soul_file.chmod(0o600)  # Owner read/write only
   ```
2. Set directory permissions:
   ```python
   self.akasha_path.mkdir(parents=True, exist_ok=True)
   self.akasha_path.chmod(0o700)  # Owner access only
   ```
3. Add file locking for concurrent access
4. Add integrity checks (checksums or signatures)

## Next Verification
- Check current file permissions on existing soul files
- Verify if _hidden directory has special permissions
