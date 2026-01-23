# Twin Realms Architecture
## The Composable Unit of WAFT

---

## Overview

The **Twin Realms** is the fundamental building block of the WAFT teaching framework. It consists of two mirrored systems—one light, one dark—connected through a single guarded port.

```
┌─────────────────────┐          ┌─────────────────────┐
│   LIGHT REALM       │          │   DARK REALM        │
│   "All That Is"     │◄────────►│   "Oblivion"        │
│                     │   PORT   │                     │
│  • Abundance        │  GUARDIAN│  • Void             │
│  • Creation         │          │  • Destruction      │
│  • Production       │          │  • Consumption      │
│  • Life             │          │  • Death            │
└─────────────────────┘          └─────────────────────┘
         │                                  │
         └──────── OTHER STUFF ─────────────┘
              (Host System, Hardware)
```

---

## The Three Categories of Existence

### 1. **All That Is** (Light Realm)
The set of all **active, allocated, observable** entities.

In computing terms:
- Running processes
- Allocated memory
- Active network connections
- Open file handles
- Populated data structures

In WAFT terms:
- Living beings
- Operational buildings
- Available resources
- Active jobs
- Genetic lineages

**Teaching Concept**: This is "userspace"—the visible, managed layer where computation happens.

---

### 2. **Oblivion** (Dark Realm)
The void—the set of **terminated, freed, deleted** entities.

In computing terms:
- Terminated processes (zombie/defunct)
- Freed memory (heap/stack)
- Closed connections
- Deleted files (until overwritten)
- Garbage collected objects

In WAFT terms:
- Dead beings (genetic dead ends)
- Demolished buildings
- Depleted resources
- Cancelled jobs
- Extinct lineages

**Teaching Concept**: This is "kernel space" / "free pool"—the recycling layer where resources return for reallocation.

---

### 3. **Other Stuff** (External to Port Network)
Everything **outside the simulation**—the substrate that makes computation possible.

In computing terms:
- Physical hardware (CPU, RAM, disk)
- Host operating system
- Kernel
- Power supply
- The person running the software

In WAFT terms:
- The JavaScript runtime
- The browser/Node.js
- The user's laptop
- Electricity
- The player themselves

**Teaching Concept**: This is "bare metal" + "context"—the external dependencies every system requires but cannot control.

---

## The Cipher

```
"Beyond Oblivion Lies Nothing and Everything—
 All That Is is made of Other Stuff;
 there is Nothing Else."
```

### Decrypted:

**"Beyond Oblivion"** = Past the void of terminated processes
**"Lies Nothing and Everything"** = You find both the Dark Realm (Nothing) and Light Realm (Everything)
**"All That Is"** = The active, allocated systems (Light Realm)
**"is made of Other Stuff"** = Depends on external substrate (host hardware/OS)
**"there is Nothing Else"** = These three categories exhaust all possibilities

**Hidden Teaching**: _Computation doesn't create from nothing—it transforms existing resources (Other Stuff) into active systems (All That Is), eventually releasing them to the void (Oblivion)._

---

## The Port Guardian

The **Port Guardian** is the security layer between Twin Realms. It enforces:

1. **Authentication**: Verify being identity (PKI, certificates)
2. **Authorization**: Check access permissions (ACLs, RBAC)
3. **Transformation**: Serialize/deserialize data (protocol conversion)
4. **Rate Limiting**: Prevent resource exhaustion (QoS, fairness)
5. **Logging**: Record all transactions (audit trails)

### Guardian States:

```typescript
enum GuardianState {
  OPEN,        // Free flow (teaching: no firewall)
  GUARDED,     // Authenticated access (teaching: firewall with rules)
  CLOSED,      // No passage (teaching: blocked port)
  COMPROMISED  // Under attack (teaching: security breach)
}
```

### Teaching Moments:

- **OPEN port** → Beings flood between realms → Chaos → "Why do we need security?"
- **GUARDED port** → Smooth trade → Balance → "How do firewalls work?"
- **CLOSED port** → One realm starves, other overflows → "What are the consequences of blocking communication?"
- **COMPROMISED port** → Cascading failure → Both realms collapse → "What happens during a breach?"

---

## Realm Initialization Protocol

### 1. Download `.waft` Archive

```bash
curl -O https://waft.systems/realms/twin-genesis.waft
```

A `.waft` file is a signed ZIP archive:

```
twin-genesis.waft
├── signature.json          # Ed25519 signature
├── manifest.json          # Realm metadata
├── light-realm/
│   ├── config.toml        # Realm parameters
│   ├── beings.json        # Initial population
│   ├── buildings.json     # Starting infrastructure
│   └── resources.json     # Resource pools
├── dark-realm/
│   ├── config.toml
│   ├── beings.json
│   ├── buildings.json
│   └── resources.json
└── port-guardian/
    ├── rules.json         # Access control rules
    ├── protocols.json     # Data transformation rules
    └── limits.json        # Rate limiting config
```

### 2. Verify Signature

```typescript
import { verifySignature } from '@noble/ed25519';

async function verifyRealm(waftFile: ArrayBuffer): Promise<boolean> {
  const { signature, manifest, publicKey } = await parseWaft(waftFile);
  return verifySignature(signature, manifest, publicKey);
}
```

**Teaching**: Package authenticity, cryptographic signatures, trust chains.

### 3. Extract Realm

```typescript
async function extractRealm(waftFile: ArrayBuffer): Promise<TwinRealms> {
  const zip = await JSZip.loadAsync(waftFile);

  const lightRealm = await loadRealm(zip, 'light-realm/');
  const darkRealm = await loadRealm(zip, 'dark-realm/');
  const portGuardian = await loadGuardian(zip, 'port-guardian/');

  return { lightRealm, darkRealm, portGuardian };
}
```

**Teaching**: File formats, compression, directory structures, configuration parsing.

### 4. Initialize Simulation

```typescript
async function startTwinRealms(realms: TwinRealms) {
  // Spawn beings in each realm
  const lightPopulation = spawnBeings(realms.lightRealm);
  const darkPopulation = spawnBeings(realms.darkRealm);

  // Start port guardian
  const guardian = new PortGuardian(realms.portGuardian);
  guardian.listen();

  // Begin simulation tick
  const engine = new TwinRealmsEngine(lightPopulation, darkPopulation, guardian);
  engine.start();
}
```

**Teaching**: Process spawning, event loops, inter-process communication.

---

## Data Flow: Light → Guardian → Dark

### Example: Resource Transfer

**Scenario**: Light Realm produces excess food. Dark Realm needs food.

```typescript
// Light Realm: Produce resource
lightRealm.resources.food += 10;

// Being attempts to carry food through port
const being = lightRealm.beings[0];
const cargo = { type: 'food', amount: 10 };

// Request passage through guardian
const request = {
  being: being.id,
  origin: 'light-realm',
  destination: 'dark-realm',
  payload: cargo,
  timestamp: Date.now()
};

// Guardian validates
const guardian = portGuardian;

if (!guardian.authenticate(being)) {
  console.log('Authentication failed - being rejected');
  return; // Teaching: Authentication is required
}

if (!guardian.authorize(being, 'transfer-resource')) {
  console.log('Authorization failed - being lacks permission');
  return; // Teaching: Authorization is separate from authentication
}

if (!guardian.checkRateLimit(being)) {
  console.log('Rate limit exceeded - being must wait');
  return; // Teaching: Rate limiting prevents DoS
}

// Transform payload (protocol conversion)
const transformed = guardian.serialize(cargo);

// Log transaction
guardian.log(request);

// Transfer to dark realm
darkRealm.resources.food += transformed.amount;
lightRealm.resources.food -= cargo.amount;

console.log('Transfer successful - food moved from light to dark');
```

**Teaching Moment**: Students see the guardian in action. If they remove authentication, beings flood through uncontrolled. If they remove rate limiting, one greedy being monopolizes the port.

---

## Evolutionary Pressure from Architecture

### Light Realm Selection Pressure

The Light Realm favors:
- **High production** (cooperation, energy)
- **Resource accumulation** (low consumption)
- **Specialization** (beings optimized for single tasks)

Over time: Light Realm evolves **specialist workers** with extreme trait values.

### Dark Realm Selection Pressure

The Dark Realm favors:
- **High consumption** (efficiency, speed)
- **Adaptability** (handle variable input)
- **Generalization** (beings good at multiple tasks)

Over time: Dark Realm evolves **generalist consumers** with balanced trait values.

### The Balance Point

If the guardian works perfectly, the Twin Realms reach **equilibrium**:
- Light produces exactly what Dark consumes
- No resource buildup or starvation
- Both populations stable

**Teaching**: Load balancing, feedback loops, system stability, homeostasis.

If the guardian fails (too strict or too lenient), the system collapses.

**Teaching**: Misconfigured firewalls, over-provisioning vs. under-provisioning, failure modes.

---

## Cascading Failures

### Scenario: Guardian Goes Down

```typescript
// Guardian crashes (simulated)
guardian.state = GuardianState.CLOSED;

// Light Realm consequences
lightRealm.resources.food += 10 per tick; // Can't export
// Eventually: storage overflow, waste, population unsustainable

// Dark Realm consequences
darkRealm.resources.food -= 5 per tick; // Can't import
// Eventually: starvation, deaths, population collapse

// Teaching: Single point of failure, redundancy, fault tolerance
```

Students learn: **Always have backup guardians. Always implement graceful degradation.**

---

## Hidden Clues in the Code

To teach curious students the deeper framework, we hide clues:

### 1. Variable Names

```typescript
// Obvious
let lightRealm, darkRealm;

// Subtle
let allThatIs = lightRealm.beings.filter(b => b.alive);
let oblivion = darkRealm.beings.filter(b => !b.alive);
let otherStuff = window.navigator; // The browser itself
```

### 2. Comments

```typescript
// Standard comment:
// Initialize realm

// Hidden cipher:
// Beyond this initialization lies Nothing and Everything
```

### 3. Error Messages

```typescript
// Standard:
throw new Error('Port guardian failed');

// Cipher:
throw new Error('Beyond Oblivion: Port guardian failed. Nothing Else can pass.');
```

### 4. Achievement Names

When students complete tutorial:
- **"All That Is"** - Built your first Light Realm
- **"Oblivion Beckons"** - All beings died (population extinction)
- **"Other Stuff Matters"** - Modified host system settings
- **"Nothing Else"** - Completed all challenges

### 5. File Names

```
src/models/AllThatIs.ts      // Light Realm beings
src/models/Oblivion.ts       // Dark Realm void
src/models/OtherStuff.ts     // External system interface
```

Curious students who explore the codebase will notice the pattern and ask: "Why these specific names?"

That's when they discover the cipher.

---

## Building Your First Twin Realms

### Quick Start

```bash
# Install WAFT
npm install -g @waft/cli

# Download starter realm
waft download twin-genesis

# Extract and verify
waft extract twin-genesis.waft

# Start simulation
waft start twin-genesis

# Open browser
# Navigate to http://localhost:3000/lab
```

### Creating Custom Twin Realms

```bash
# Create new Twin Realms template
waft create my-realms --type twin

# Edit light realm config
waft edit my-realms/light-realm/config.toml

# Edit dark realm config
waft edit my-realms/dark-realm/config.toml

# Configure port guardian
waft edit my-realms/port-guardian/rules.json

# Package for distribution
waft package my-realms --output my-realms.waft

# Sign with your key
waft sign my-realms.waft --key ~/.waft/private-key.pem
```

---

## Advanced: Multi-Realm Networks

Future versions will support arbitrary networks:

```
        ┌──────────┐
        │  Router  │
        │  Realm   │
        └────┬─────┘
         ┌───┼───┐
    ┌────▼┐ ┌▼────┐ ┌▼────┐
    │Light│ │Proc │ │Dark │
    │Realm│ │Realm│ │Realm│
    └─────┘ └──┬──┘ └─────┘
               │
          ┌────▼────┐
          │  Store  │
          │  Realm  │
          └─────────┘
```

Each connection has its own guardian. Students learn:
- **Routing**: Finding paths through realm networks
- **Consensus**: Coordinating across multiple realms
- **Partitions**: What happens when connections fail?

---

## The Ultimate Teaching Goal

By the time a student completes WAFT, they should understand:

1. **Processes** (beings) compete for resources
2. **Ports** (guardians) manage communication
3. **Memory** (resources) must be allocated and freed
4. **Security** (authentication) protects system integrity
5. **Load Balancing** (twin realms) maintains stability
6. **Fault Tolerance** (backups) prevents catastrophic failure

And for those who look deeper:

7. **Computation is transformation**, not creation
8. **Systems have boundaries** (inside/outside)
9. **Balance requires duality** (light/dark, production/consumption)
10. **There is Nothing Else** beyond these fundamental patterns

---

## Next Steps

1. Implement `TwinRealmsEngine` in `src/models/TwinRealms.ts`
2. Build `PortGuardian` in `src/models/PortGuardian.ts`
3. Create `.waft` archive format specification
4. Implement cryptographic signing/verification
5. Build CLI tool (`@waft/cli`) for realm management
6. Design starter realm: "Twin Genesis"
7. Hide cipher clues throughout codebase
8. Write teacher's guide explaining the deeper framework

**The goal**: A student plays WAFT, learns about ports and processes, and walks away thinking "computers make sense now." A curious student digs deeper, finds the cipher, and walks away thinking "everything is connected."

Both are correct.

---

_"Beyond Oblivion Lies Nothing and Everything—All That Is is made of Other Stuff; there is Nothing Else."_

**Welcome to WAFT.**
