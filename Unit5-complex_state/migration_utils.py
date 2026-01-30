# Resumable Batch Migration with Progress Tracking

## Estimated Time Calculation Implementation

### 1. Migration Status Monitoring
```python
def estimated_minutes_remaining(self):
    """Estimates remaining time based on migration progress"""
    
    progress = json.loads(self.redis.get("migration:progress") or "{}")
    
    if not (progress.get("total") and progress.get("processed")):
        return 0
    
    total = progress.get("total", 0)
    processed = progress.get("processed", 0)
    remaining = total - processed
    
    if processed == 0:
        return 0
    
    time_per_item = (time.time() - START_TIMESTAMP) / processed
    remaining_time = remaining * time_per_item
    
    return int(remaining_time / 60)  # Convert to minutes
```

## 2. Updated Migration Status
```python
def get_migration_status(self):
    """Returns comprehensive migration statistics"""
    progress = json.loads(self.redis.get("migration:progress") or "{}")
    
    return {
        "status": "running",
        "total_keys": int(self.redis.get("migration:total") or 0),
        "processed": progress.get("processed", 0),
        "incomplete": int(self.redis.get("migration:total") or 0) - progress.get("processed", 0),
        "failed": self.redis.llen(self.failures_key),
        "failures": list(self.redis.lrange(self.failures_key, 0, -1)),
        "current_key": progress.get("current_key", "none active"),
        "history": [json.loads(h) for h in self.redis.zrevrange("migration:history", 0, 10)],
        "estimated_minutes_remaining": self.estimated_minutes_remaining(),
        "next_resume_point": self.redis.get("migration:next_resume") or cursor
    }
```

## 3. Real-Time Monitoring Integration
```python
# Integration with OpenTelemetry
from opentelemetry import metrics

exporter = PrometheusExporter()

migrated_states = metrics.Counter("states_migrated")
failed_migrations = metrics.Counter("migration_errors")

# Instrument migration operations
try:
    success = await self.process_batch()
    if success:
        migrated_states.add(1)
    else:
        failed_migrations.add(1)
except Exception as e:
    failed_migrations.add(1)
    raise
```

## 4. Progress Tracking Implementation
```python
# Redis tracking with sorted sets
self.redis.zadd(
    "migration:history",
    {
        f"{key}:{current_time}": current_time
        for key in processed_keys
    }
)
self.redis.expire("migration:history", 24 * 60 * 60)  # 24 hour retention
```

## 5. Batch Resumption Logic
```python
def resume_batch(self, pattern="*:state"):
    """Resume migration from last known state"""
    progress_data = self.redis.get("migration:progress")
    if not progress_data:
        self.start_batch_migration(pattern)
        return True
    
    cursor = progress_data.get("cursor", 0)
    processed = progress_data.get("processed", 0)
    
    # Skip already processed keys
    processed_keys = self.redis.smembers("migration:processed")
    current_keys = self.redis.scan(cursor, pattern, count=batch_size)
    unprocessed = [k for k in current_keys if k not in processed_keys]
    
    if unprocessed:
        return self.process_batch(pattern=pattern, keys=unprocessed)
    return False
```

## 6. Migration UI Dashboard Concept
```mermaid
flowchart LR
    A[Start Migration] --> B{Batch Progress?}
    B -->|Processing| C[Current Key: $KEY]
    B -->|Paused| D[Resume Point: $cursor]
    C --> E[Estimated: $minutes min]
    D --> F[Recover from: $last_fail]
    E --> G[Metric: $progress%]
    F --> G
```
