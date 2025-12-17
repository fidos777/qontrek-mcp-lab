# Phase B Quick Start Guide

## 🚀 Execute a Workflow in 3 Steps

### Step 1: Create Payload
```bash
cat > payload.json << 'EOF'
{
  "brand_name": "MyBrand",
  "mission": "My mission statement",
  "value_proposition": "My value prop",
  "icp": {
    "demographics": "Target audience",
    "pain_points": ["Pain 1", "Pain 2"],
    "goals": ["Goal 1", "Goal 2"]
  },
  "brand_themes": ["theme1", "theme2"]
}
EOF
```

### Step 2: Execute Workflow
```bash
# Full LaunchKit (6 steps)
cat payload.json | python3 l6/runner_v2.py kuasaturbo.launchkit.v1

# OR minimal workflow (2 steps)
cat payload.json | python3 l6/runner_v2.py turbodrive.followup_only.v1
```

### Step 3: Check Result
```bash
cat payload.json | python3 l6/runner_v2.py kuasaturbo.launchkit.v1 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}, Steps: {len(d['completed_steps'])}/{len(d['completed_steps'])+len(d['pending_steps'])+len(d['failed_steps'])}\")"
```

---

## 📋 Available Workflows

```
kuasaturbo.launchkit.v1       - Full LaunchKit (6 steps: branding, prd, pricing, roadmap, pitchdeck, socialpack)
turbodrive.followup_only.v1   - Minimal workflow (2 steps: branding, prd)
```

---

## 🧪 Run Tests

```bash
bash tests/test_workflow_runner.sh
```

---

## 📖 Full Documentation

See `l6/PHASE_B_SUMMARY.md` for complete details.
