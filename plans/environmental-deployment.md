# Low-Energy Deployment Recommendations

Guide for deploying these OpenAI agents with minimal environmental impact.

---

## 1. Model Selection (Biggest Impact)

**Use the smallest model that works for your task.**

| Model | Relative Energy | When to Use |
|-------|-----------------|-------------|
| `gpt-4o-mini` | ~1x (baseline) | Default choice for most agent tasks |
| `gpt-4o` | ~3-5x | Only when mini fails quality requirements |
| `gpt-4.5` | ~10x+ | Avoid unless strictly necessary |

A typical GPT-4o query uses ~0.3 watt-hours. Smaller models use proportionally less. This is your biggest lever—model choice dwarfs infrastructure decisions.

**Recommendation:** Start with `gpt-4o-mini` for all agents. Only upgrade if you see quality issues.

---

## 2. Cloud Region Selection

If using cloud hosting, region choice matters significantly.

### Google Cloud (Best Carbon Transparency)

| Region | Carbon-Free Energy | Grid Intensity |
|--------|-------------------|----------------|
| **Osaka (asia-northeast2)** | 46% | 296 gCO2eq/kWh |
| **Seoul (asia-northeast3)** | 37% | 357 gCO2eq/kWh |
| Finland (europe-north1) | 94% | 96 gCO2eq/kWh |
| Oregon (us-west1) | 89% | 78 gCO2eq/kWh |

### AWS

| Region | Notes |
|--------|-------|
| **Oregon (us-west-2)** | Excellent renewable mix |
| **Ireland (eu-west-1)** | Good European option |
| Stockholm (eu-north-1) | High renewable percentage |

**Recommendation:** For US-based deployments, use **Oregon**. For Asia, use **Osaka**.

---

## 3. Compute Architecture

**Use ARM (Graviton) over x86.**

ARM-based processors (AWS Graviton, Apple Silicon) use 40-60% less energy than x86 for equivalent Python workloads. 2025 benchmarks show Graviton outperforming x86 by 4-5x on CPU-intensive Python tasks.

| Platform | ARM Option |
|----------|------------|
| AWS EC2 | `t4g.*`, `m7g.*`, `c7g.*` (Graviton) |
| AWS Lambda | Select "arm64" architecture |
| Fly.io | Not available (use AWS) |
| Railway | Not available (use AWS) |

**Recommendation:** If on AWS, always select Graviton/arm64.

---

## 4. Serverless vs Always-On

**Serverless wins for intermittent workloads.**

Idle servers consume ~50% of data center energy. Serverless (Lambda, Cloud Functions) scales to zero when not in use.

| Deployment Style | Best For | Energy Profile |
|------------------|----------|----------------|
| **Serverless** | Occasional agent runs | Zero idle consumption |
| Container (always-on) | Continuous processing | Constant baseline draw |
| VM (always-on) | Legacy/specific requirements | Highest idle waste |

**Recommendation:** For agents that run periodically (like your program_manager or librarian), use AWS Lambda or Google Cloud Functions.

---

## 5. Practical Deployment Options (Ranked by Energy Efficiency)

### Option A: AWS Lambda + Graviton (Lowest Energy)

```
Architecture: arm64
Region: us-west-2 (Oregon)
Memory: Start at 256MB, tune upward if needed
```

Pros:
- Zero idle energy
- ARM efficiency bonus
- Pay only for invocations

Cons:
- 15-minute execution limit
- Cold starts (~100-500ms)

### Option B: Google Cloud Run (Very Low Energy)

```
Region: us-west1 (Oregon) or europe-north1 (Finland)
CPU: 1 vCPU
Memory: 512MB
Min instances: 0 (scale to zero)
```

Pros:
- Scale to zero
- No time limit (configurable)
- Good carbon transparency via Google tools

### Option C: Fly.io (Low Energy, Easy)

```
Region: sea (Seattle) or ams (Amsterdam)
Machine: shared-cpu-1x
Memory: 256MB
Auto-stop: enabled
```

Pros:
- Dead simple deployment
- Auto-suspend when idle
- Good global distribution

Cons:
- No ARM option
- Less carbon transparency

---

## 6. Code-Level Optimizations

### Reduce Token Usage

```python
# Instead of verbose system prompts:
instructions = """You are a helpful assistant that helps users 
find information in a database. Be thorough and detailed in 
your responses. Always be polite and professional."""

# Use concise prompts:
instructions = "Search the database. Return relevant results only."
```

Fewer tokens = fewer compute cycles = less energy.

### Batch Operations

```python
# Instead of multiple single-item calls:
for item in items:
    await agent.run(f"Process {item}")

# Batch into one call:
await agent.run(f"Process all: {items}")
```

### Cache Expensive Operations

```python
import functools

@functools.lru_cache(maxsize=100)
def get_cached_result(query_hash):
    # Avoid re-running identical agent queries
    pass
```

---

## 7. Quick Reference: Lowest-Energy Stack

For your agents in this repo:

| Component | Recommendation |
|-----------|----------------|
| **Model** | `gpt-4o-mini` |
| **Platform** | AWS Lambda |
| **Architecture** | arm64 (Graviton) |
| **Region** | us-west-2 (Oregon) |
| **Scaling** | Scale to zero when idle |

Estimated energy per invocation: **~0.3-0.5 watt-hours** (including model inference on OpenAI's side).

---

## 8. Monitoring Your Impact

- **Google Cloud:** Use [Carbon Footprint](https://cloud.google.com/carbon-footprint) dashboard
- **AWS:** Use [Customer Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/)
- **Track tokens:** Log `usage.total_tokens` from API responses

---

## Summary

1. **Model choice matters most** — use `gpt-4o-mini` by default
2. **Use ARM/Graviton** — 40-60% energy savings over x86
3. **Use serverless** — eliminates idle energy waste
4. **Pick green regions** — Oregon (US), Finland/Ireland (EU), Osaka (Asia)
5. **Minimize tokens** — shorter prompts, batched operations
