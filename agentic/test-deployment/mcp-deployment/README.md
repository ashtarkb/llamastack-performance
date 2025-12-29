# MCP Server Deployment

Model Context Protocol (MCP) server for testing LlamaStack Responses API with tool calling.

## Files

### nps_mcp_server.py
Python MCP server implementation with National Parks Service (NPS) API integration.

**Tools implemented:**
- `search_parks` - Search for parks by state code, park code, or query
- `get_park_alerts` - Get active alerts for a specific park
- `get_park_campgrounds` - Get campground information for a park
- `get_park_events` - Get upcoming events at a specific park
- `get_visitor_centers` - Get visitor center information for a park

This demonstrates MCP tool integration with LlamaStack using the real NPS.gov API.

### Dockerfile.nps-mcp
Container image build instructions for the MCP server.

**Base:** Python 3.11-slim  
**Dependencies:** `fastmcp`, `httpx`

### nps-mcp-server-deployment.yaml
Kubernetes manifests for deploying the MCP server.

**Creates:**
- Deployment: `nps-mcp-server`
- Service: `nps-mcp-server.bench.svc.cluster.local:3005`

## Deployment

```bash
oc apply -f nps-mcp-server-deployment.yaml -n bench
```

**Image:** `quay.io/rh-ee-tosokin/nps-mcp-server:v1-mcp-metrics` (public)


## Verify

```bash
# Check pod is running
oc get pods -n bench -l app=nps-mcp-server
```

## Usage

Reference the MCP server in your Responses API calls:

```python
client.responses.create(
    model="vllm-inference/llama-32-3b-instruct",
    input="Find parks in Rhode Island",
    tools=[{
        "type": "mcp",
        "server_url": "http://nps-mcp-server.bench.svc.cluster.local:3005/sse",
        "server_label": "National Parks Service"
    }],
    stream=False,
)
```

---

## Related

- [Locust Test with MCP](../../locustfiles/locustfile_responses_mcp.py) - Test script that uses this MCP server
- [Agentic Testing Guide](../../README.md) - Main deployment documentation

