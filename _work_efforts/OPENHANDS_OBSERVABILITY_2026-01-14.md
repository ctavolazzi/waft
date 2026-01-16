# OpenHands Observability & Tracing with OpenTelemetry

**Date**: 2026-01-14 20:50:00
**Context**: Using OpenTelemetry tracing to monitor and debug agent execution
**Status**: 📊 OBSERVABILITY ENABLED

---

## What Is Observability?

OpenHands SDK provides **built-in OpenTelemetry (OTEL) tracing support**, allowing you to monitor and debug your agent's execution in real-time.

**Key Benefits**:
- ✅ **Real-Time Monitoring**: See agent execution as it happens
- ✅ **Debugging**: Trace tool calls, LLM requests, and agent steps
- ✅ **Performance Analysis**: Identify bottlenecks and slow operations
- ✅ **Session Replay**: Browser automation replays (Laminar only)
- ✅ **Zero Code Changes**: Enabled via environment variables

---

## Supported Platforms

The SDK supports any OTLP-compatible observability platform:

* **[Laminar](https://laminar.sh/)** - AI-focused observability with browser session replay
* **[Honeycomb](https://www.honeycomb.io/)** - High-performance distributed tracing
* **[Jaeger](https://www.jaegertracing.io/)** - Open-source distributed tracing
* **Any OTLP-compatible backend** - Datadog, New Relic, and more

---

## Quick Start

### Using Laminar (Recommended for AI Agents)

**Setup**:
1. Sign up at [laminar.sh](https://laminar.sh/)
2. Create a project and copy your API key
3. Set environment variable:

```bash
export LMNR_PROJECT_API_KEY="your-laminar-api-key"
```

**That's it!** Run your agent code normally and traces will be sent to Laminar automatically.

**Special Features**:
- Browser session replays when using browser-use tools
- AI-focused trace visualization
- Conversation grouping by session ID

---

### Using Honeycomb

**Setup**:
1. Sign up at [honeycomb.io](https://www.honeycomb.io/)
2. Get your API key from account settings
3. Configure environment:

```bash
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://api.honeycomb.io:443/v1/traces"
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="x-honeycomb-team=YOUR_API_KEY"
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL="http/protobuf"
```

---

### Using Jaeger (Local Development)

**Setup**:
1. Start Jaeger all-in-one container:

```bash
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

2. Configure SDK:

```bash
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL="grpc"
```

3. Access Jaeger UI at [http://localhost:16686](http://localhost:16686)

---

## How It Works

### Automatic Instrumentation

The SDK automatically instruments these components:

* **`agent.step`** - Each iteration of the agent's execution loop
* **Tool Executions** - Individual tool calls with input/output capture
* **LLM Calls** - API requests to language models via LiteLLM
* **Conversation Lifecycle** - Message sending, conversation runs, and title generation
* **Browser Sessions** - When using browser-use, captures session replays (Laminar only)

### Trace Hierarchy

Traces are organized hierarchically:

```
conversation (session_id: conversation-uuid)
└── conversation.run
    ├── agent.step
    │   ├── llm.completion
    │   └── tool.execute (e.g., "bash", "file_editor")
    └── agent.step
        └── llm.completion
```

**Session ID**: Each conversation gets its own session ID (the conversation UUID), allowing you to group all traces from a single conversation together in your observability platform.

---

## Configuration Reference

### Environment Variables

The SDK checks for these environment variables (in order of precedence):

| Variable                             | Description                               | Example                                  |
| ------------------------------------ | ----------------------------------------- | ---------------------------------------- |
| `LMNR_PROJECT_API_KEY`               | Laminar project API key                   | `your-laminar-api-key`                   |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Full OTLP traces endpoint URL             | `https://api.honeycomb.io:443/v1/traces` |
| `OTEL_EXPORTER_OTLP_ENDPOINT`        | Base OTLP endpoint (traces path appended) | `http://localhost:4317`                  |
| `OTEL_ENDPOINT`                      | Short form endpoint                       | `http://localhost:4317`                  |
| `OTEL_EXPORTER_OTLP_TRACES_HEADERS`  | Authentication headers for traces         | `x-honeycomb-team=YOUR_API_KEY`          |
| `OTEL_EXPORTER_OTLP_HEADERS`         | General authentication headers            | `Authorization=Bearer%20TOKEN`           |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | Protocol for traces endpoint              | `http/protobuf`, `grpc`                  |
| `OTEL_EXPORTER`                      | Short form protocol                       | `otlp_http`, `otlp_grpc`                 |

### Header Format

Headers should be comma-separated `key=value` pairs with URL encoding:

```bash
# Single header
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="x-honeycomb-team=abc123"

# Multiple headers
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="Authorization=Bearer%20abc123,X-Custom-Header=value"
```

### Protocol Options

* **`http/protobuf`** or **`otlp_http`** - HTTP with protobuf encoding (recommended for most backends)
* **`grpc`** or **`otlp_grpc`** - gRPC with protobuf encoding (use only if your backend supports gRPC)

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Automatic observability detection
- ✅ Displays observability status on startup
- ✅ Shows session ID (conversation UUID) for trace lookup
- ✅ No code changes needed - just environment variables

**Usage**:

```bash
# Enable Laminar observability
export LMNR_PROJECT_API_KEY="your-laminar-api-key"
python scripts/generate_tavern_game_with_skills.py

# Enable Honeycomb observability
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://api.honeycomb.io:443/v1/traces"
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="x-honeycomb-team=YOUR_API_KEY"
python scripts/generate_tavern_game_with_skills.py
```

**Output**:
```
🚀 Generating Electron Tavern Game with OpenHands SDK + MCP + Skills + Persistence
   Model: anthropic/claude-sonnet-4-5-20250929
   Conversation ID: abc123-def456-...
   Persistence dir: /path/to/.conversations
   📊 Observability: Enabled (Laminar)
   Session ID: abc123-def456-... (use this to find traces in your dashboard)
```

---

## What Gets Traced

### Agent Execution

**Traced Events**:
- Agent step iterations
- Decision-making process
- Tool selection
- LLM reasoning

**Trace Attributes**:
- `conversation_id`: UUID of the conversation
- `session_id`: Groups all traces from one conversation
- `action.kind`: Type of action being performed

---

### Tool Calls

**Traced Events**:
- Tool execution start/end
- Tool input parameters
- Tool output results
- Tool errors

**Trace Attributes**:
- `tool_name`: Name of the tool being executed
- `tool_input`: Input parameters (may be sanitized)
- `tool_output`: Output results (may be truncated)

---

### LLM API Calls

**Traced Events**:
- API request/response
- Token usage
- Latency
- Errors

**Trace Attributes**:
- `llm.model`: Model name
- `llm.provider`: Provider (Anthropic, OpenAI, etc.)
- `llm.tokens`: Token counts
- `llm.latency`: Response latency

---

### Conversation Lifecycle

**Traced Events**:
- Message sending
- Conversation runs
- Title generation
- State persistence

**Trace Attributes**:
- `conversation_id`: Conversation UUID
- `message_count`: Number of messages
- `phase`: Current phase (if applicable)

---

## Use Cases

### 1. Debugging Agent Behavior

**Problem**: Agent not working as expected

**Solution**: Use traces to see:
- What tools were called
- What LLM responses were received
- What decisions were made
- Where errors occurred

**Example**:
```
conversation.run()
# Check Laminar/Honeycomb dashboard
# Filter by session_id (conversation UUID)
# See full execution trace
```

---

### 2. Performance Optimization

**Problem**: Agent is slow

**Solution**: Use traces to identify:
- Slow LLM calls
- Tool execution bottlenecks
- Network latency issues
- Inefficient agent loops

**Example**:
```
# In observability dashboard:
# - Sort by latency
# - Identify slow spans
# - Optimize based on findings
```

---

### 3. Cost Analysis

**Problem**: High API costs

**Solution**: Use traces to analyze:
- LLM call frequency
- Token usage per call
- Tool call patterns
- Optimization opportunities

**Example**:
```
# Combine traces with metrics:
# - Traces show what happened
# - Metrics show costs
# - Together: understand cost drivers
```

---

### 4. Session Replay (Laminar)

**Problem**: Need to see browser automation

**Solution**: Laminar provides browser session replays:
- See exactly what browser did
- Watch automation in action
- Debug browser-use issues

**Example**:
```
# Using browser-use tool with Laminar:
# - Traces show tool calls
# - Session replay shows browser actions
# - Full visibility into automation
```

---

## Integration with Other Features

### Observability + Metrics

**Combined Benefits**:
- Traces show what happened
- Metrics show costs and performance
- Together: complete picture

**Example**:
```python
# Traces: See execution flow
# Metrics: See costs and tokens
# Together: Understand cost drivers
```

---

### Observability + Persistence

**Combined Benefits**:
- Traces persist across sessions
- Session ID matches conversation ID
- Resume with full trace history

**Example**:
```python
# Session 1: Generate with traces
# Session 2: Resume with same session ID
# Traces: See full history across sessions
```

---

### Observability + Delegation

**Combined Benefits**:
- Traces show sub-agent execution
- See parallel execution in action
- Debug sub-agent issues

**Example**:
```python
# Main agent traces
# Sub-agent traces (separate spans)
# See parallel execution timeline
```

---

### Observability + Condenser

**Combined Benefits**:
- Traces show condensation events
- See when condensation triggers
- Understand context management

**Example**:
```python
# Agent traces: Main conversation
# Condenser traces: Summarization events
# Together: See context management
```

---

## Best Practices

### 1. Use Session IDs

**Always use conversation UUID as session ID**:
- Groups all traces from one conversation
- Easy to find in dashboard
- Matches conversation ID from persistence

**Example**:
```python
conversation_id = uuid.uuid4()
conversation = Conversation(..., conversation_id=conversation_id)
# Session ID in traces = conversation_id
```

---

### 2. Enable in Production

**Enable observability for production**:
- Monitor agent behavior
- Debug issues quickly
- Optimize performance
- Track costs

**Example**:
```bash
# Production environment
export LMNR_PROJECT_API_KEY="prod-key"
# Or
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://prod-collector:4317"
```

---

### 3. Disable in Development (Optional)

**Disable tracing in development** (if desired):
- Reduce noise
- Faster execution
- Lower costs

**Example**:
```bash
# Development: Disable tracing
unset LMNR_PROJECT_API_KEY
unset OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
```

---

### 4. Use Sampling for High Volume

**Configure sampling at collector level**:
- Reduce trace volume
- Keep important traces
- Lower costs

**Example**:
```bash
# Configure sampling in OTLP collector
# Keep 10% of traces
# Or use backend-specific sampling rules
```

---

## Troubleshooting

### Traces Not Appearing

**Problem**: No traces showing up in observability platform

**Solutions**:
1. Verify environment variables are set:
   ```python
   import os
   print(f"OTEL Endpoint: {os.getenv('OTEL_EXPORTER_OTLP_TRACES_ENDPOINT')}")
   print(f"OTEL Headers: {os.getenv('OTEL_EXPORTER_OTLP_TRACES_HEADERS')}")
   ```

2. Check network connectivity:
   ```bash
   curl -v https://api.honeycomb.io:443/v1/traces
   ```

3. Validate headers (URL-encoded):
   ```bash
   # Correct
   export OTEL_EXPORTER_OTLP_TRACES_HEADERS="x-honeycomb-team=abc123"
   
   # Incorrect (not URL-encoded)
   export OTEL_EXPORTER_OTLP_TRACES_HEADERS="Authorization=Bearer token"
   ```

4. Check SDK logs (debug level):
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

### High Trace Volume

**Problem**: Too many spans being generated

**Solutions**:
1. Configure sampling at collector level
2. Use backend-specific filtering rules
3. For Laminar with non-browser tools, browser instrumentation is automatically disabled

---

### Performance Impact

**Problem**: Concerned about tracing overhead

**Solutions**:
1. Tracing has minimal overhead when properly configured
2. Disable tracing in development by unsetting environment variables
3. Use asynchronous exporters (default in most OTLP configurations)

---

## Advanced Usage

### Custom Span Attributes

The SDK automatically adds these attributes to spans:

* **`conversation_id`** - UUID of the conversation
* **`tool_name`** - Name of the tool being executed
* **`action.kind`** - Type of action being performed
* **`session_id`** - Groups all traces from one conversation

**Custom attributes** can be added via OpenTelemetry SDK if needed.

---

### Disabling Observability

To disable tracing, simply unset all OTEL environment variables:

```bash
unset LMNR_PROJECT_API_KEY
unset OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
unset OTEL_EXPORTER_OTLP_ENDPOINT
unset OTEL_ENDPOINT
```

The SDK will automatically skip all tracing instrumentation with minimal overhead.

---

## Platform-Specific Features

### Laminar

**Special Features**:
- Browser session replays (when using browser-use)
- AI-focused trace visualization
- Conversation grouping
- Easy setup (just API key)

**Best For**:
- AI agent development
- Browser automation debugging
- Quick setup

---

### Honeycomb

**Special Features**:
- High-performance distributed tracing
- Powerful query language
- Cost-effective for high volume
- Enterprise features

**Best For**:
- Production monitoring
- High-volume applications
- Enterprise deployments

---

### Jaeger

**Special Features**:
- Open-source
- Local development
- Full control
- No vendor lock-in

**Best For**:
- Local development
- Self-hosted solutions
- Learning OpenTelemetry

---

## Conclusion

**Observability Benefits**:
- ✅ Real-time monitoring
- ✅ Debugging capabilities
- ✅ Performance analysis
- ✅ Cost optimization
- ✅ Zero code changes

**Essential for**:
- Production deployments
- Debugging complex agents
- Performance optimization
- Cost analysis

**This is essential for production observability!**

---

**Observability Guide Complete**: 2026-01-14 20:50:00