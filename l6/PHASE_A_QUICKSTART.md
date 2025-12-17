# Phase A Quick Start Guide

## 🚀 Execute a Skill in 3 Steps

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

### Step 2: Execute Skill
```bash
cat payload.json | python3 l6/dispatcher_mvp.py launchkit.branding.generate.v1
```

### Step 3: Check Result
```bash
cat payload.json | python3 l6/dispatcher_mvp.py launchkit.branding.generate.v1 | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\")"
```

---

## 📋 Available Skills

```
launchkit.branding.generate.v1    - Brand content (story, taglines, tone guide)
launchkit.prd.generate.v1         - Product Requirements Document
launchkit.pricing.generate.v1     - Pricing strategy (NO hardcoded prices)
launchkit.roadmap.generate.v1     - 30/60/90-day roadmap
launchkit.pitchdeck.generate.v1   - 9-slide investor deck
launchkit.socialpack.generate.v1  - Social launch content
```

---

## 🧪 Run Tests

```bash
bash tests/test_dispatcher.sh
```

---

## 📖 Full Documentation

See `l6/PHASE_A_SUMMARY.md` for complete details.
