---
inclusion: always
priority: critical
---

# KuasaTurbo Platform Boundaries (CRITICAL)

## ⚠️ MANDATORY READING FOR ALL KIRO SESSIONS

This document defines the **STRICT SEPARATION** between KuasaTurbo and Qontrek OS. Violating these boundaries will result in architectural contamination.

---

## 🚫 WHAT KUASATURBO MUST NEVER INCLUDE

KuasaTurbo is a **lightweight microservices platform**. It MUST NOT include:

### Forbidden Features (Qontrek OS Only)
- ❌ Governance features
- ❌ Compliance logic
- ❌ Audit trails
- ❌ Ledger events
- ❌ SLA logic
- ❌ Drift detection
- ❌ Exception workflows
- ❌ Multi-party approvals (G18)
- ❌ Certification logic (G21)
- ❌ Any Qontrek governance gates (G13-G21)

### Forbidden Schema Fields
- ❌ `governance_gate`
- ❌ `mcp_task`
- ❌ `ledger_commit`
- ❌ `seal`
- ❌ `drift`
- ❌ `audit`
- ❌ `compliance`
- ❌ `multi_approval`
- ❌ `SLA`
- ❌ `exception_handling`

**If Kiro detects these fields → REJECT immediately**

---

## ✅ WHAT KUASATURBO IS

KuasaTurbo is a **lightweight AI worker engine** using:

- **L3**: Lightweight Widgets (simple forms)
- **L4**: Vertical Packs (structure only, NO governance)
- **L5**: Persona Packs (tone, language, behavior)
- **L6**: Engine (dispatcher + persona routing)
- **L8**: Workflows (simple, fast execution)

**NOT USED**: L7 (Governance), L9 (Ledger)

---

## ✅ WHAT KUASATURBO DOES

KuasaTurbo performs **FAST, SIMPLE, NON-GOVERNED** AI actions:

### Content & Creative
- Generate content ideas
- Produce captions, hooks, scripts
- Create social media posts
- Build creative briefs
- Generate content calendars

### Accounting Lite
- Generate invoices
- Categorize expenses
- Calculate cashflow snapshots
- Compute profit margins

### CRM & Sales
- Capture lead information
- Handle objections
- Plan follow-ups
- Generate WhatsApp templates
- Book appointments

### HR / Ops
- Record attendance (local)
- Create task checklists
- Send announcements
- Lookup SOPs

### F&B / Retail
- Update menus
- Track daily sales
- Capture orders
- Generate product descriptions

### Proposals
- Generate proposals
- Compare prices
- Build upsell offers

### Automotive (Base KuasaTurbo)
- Evaluate trade-ins
- Check loan eligibility
- Book test drives
- Explain car specs

**All actions MUST be:**
- ✔ Stateless
- ✔ Non-compliant
- ✔ Non-governed
- ✔ Lightweight
- ✔ Direct
- ✔ Workflow-driven

---

## 📋 WIDGET SCHEMA (L3 - KuasaTurbo Edition)

### Valid Widget Structure

```yaml
widget_id: <string>
widget_name: <string>
vertical: <string>
description: <string>

fields:
  - id: <string>
    label: <string>
    type: <text|number|select|checkbox|textarea|file>
    required: <true|false>
    options: [optional for select]

validations:
  - field: <string>
    rule: <string>
    message: <string>

workflow:
  trigger: <workflow_id>
  persona: <persona_id>

presentation:
  style: <string>
  icon: <string>
```

### Forbidden Widget Fields

A KuasaTurbo widget MUST NOT contain:
- ❌ `governance_gate`
- ❌ `mcp_task`
- ❌ `ledger_commit`
- ❌ `seal`
- ❌ `drift`
- ❌ `audit`
- ❌ `compliance`
- ❌ `multi_approval`
- ❌ `SLA`
- ❌ `exception_handling`

**Widgets must be simple.**

---

## 🔄 WORKFLOW BEHAVIOR (L8)

### Valid Workflow Pattern

```yaml
workflow_id: content_idea_workflow.v1
steps:
  - type: ai_generate
    persona: zeyti_bbnu_creator
    input: "{{fields.topic}}, {{fields.platform}}, {{fields.audience}}"
```

A KuasaTurbo workflow MUST:
- Map directly: widget → engine → persona
- Return immediate AI-generated output
- Never interact with governance
- Never call ledger-based handlers

### Invalid Workflow Pattern (REJECT)

```yaml
workflow_id: approval_flow.v1
steps:
  - type: governance_check  # ❌ NOT ALLOWED
```

---

## 👤 PERSONA PACKS (L5) - Valid for KuasaTurbo

Personas are **ALLOWED** and provide:
- ✔ Tone
- ✔ Language mix (English/BBNU)
- ✔ Persuasion style
- ✔ Structure preferences

Personas MUST NEVER define:
- ❌ Compliance rules
- ❌ Governance rules
- ❌ Vertical-specific restrictions

### Valid Personas (Already Implemented)
- Izzara - Friendly Consultant
- Zeyti - BBNU Creator
- Tawfiq - Sales Closer
- Jordan - CFO Analyst
- Raya - Campaign Storyteller

---

## 🏢 VERTICAL PACKS (L4) - KuasaTurbo Edition

A KuasaTurbo vertical ONLY defines:
- ✔ Domain name
- ✔ Typical workflows
- ✔ Typical widgets
- ✔ Typical fields

A KuasaTurbo vertical MUST NOT define:
- ❌ Governance rules
- ❌ Compliance items
- ❌ Audit rules
- ❌ Chain-of-approval

### Valid Verticals (KuasaTurbo)
- content
- creative
- accounting
- hr
- crm
- fnb
- retail
- automotive

---

## 🏗️ MICROSERVICES ARCHITECTURE

Each microservice = **1 widget** + **1 workflow**

### API Pattern

```
POST /service/{service_id}
{
  "widget_payload": { ...fields },
  "persona_id": "<persona>",
  "workflow_id": "<workflow>"
}
```

Microservices MUST be:
- ✔ Stateless
- ✔ Fast
- ✔ Persona-driven
- ✔ Workflow-driven
- ✔ Qontrek-independent

**No microservice may use governance code.**

---

## 🔒 STRICT BOUNDARY: Qontrek vs KuasaTurbo

### KuasaTurbo
- Lightweight
- No governance
- No ledger
- Fast actions
- Microservices
- Multi-vertical
- WhatsApp-first

### Qontrek OS
- Governance
- Proof ledger
- Multi-party approval
- SLA
- Drift detection
- Certification
- Compliance automation

**These systems MUST stay separate.**

---

## ❌ WHAT KIRO MUST NOT DO

When working on KuasaTurbo, Kiro MUST NOT:

1. ❌ Add governance layers into KuasaTurbo
2. ❌ Enforce Qontrek schema constraints
3. ❌ Introduce audit logic
4. ❌ Generate `ledger_event` actions
5. ❌ Add compliance fields
6. ❌ Merge KuasaTurbo and Qontrek verticals
7. ❌ Build approval chains in workflows
8. ❌ Create widgets with certification or governance gates

**If Kiro detects governance fields → Reject them**  
**If Kiro accidentally creates governance logic → Remove it**

---

## ✅ WHAT KIRO MUST ALWAYS DO

When working on KuasaTurbo, Kiro MUST:

1. ✔ Keep KuasaTurbo widgets simple
2. ✔ Keep workflows short and direct
3. ✔ Maintain strict separation from Qontrek
4. ✔ Generate clean YAML specs
5. ✔ Align persona with workflow
6. ✔ Support multi-vertical microservices
7. ✔ Ensure no governance leaks into KuasaTurbo
8. ✔ Produce L3/L4/L5/L6/L8, NOT L7/L9

---

## 🧪 VALIDATION CHECKLIST

Before implementing any KuasaTurbo feature, verify:

- [ ] No governance fields in widget schema
- [ ] No compliance logic in workflow
- [ ] No ledger events in handlers
- [ ] No audit trails in output
- [ ] No SLA logic in execution
- [ ] No multi-party approval in flow
- [ ] Workflow is stateless
- [ ] Widget is simple (< 10 fields ideal)
- [ ] Persona is behavioral only (no vertical logic)
- [ ] Vertical is structural only (no governance)

---

## 📚 LAYER REFERENCE

| Layer | KuasaTurbo | Qontrek OS |
|-------|------------|------------|
| L3 | ✅ Lightweight Widgets | ❌ Not used |
| L4 | ✅ Vertical Packs (simple) | ✅ Vertical Packs (governed) |
| L5 | ✅ Persona Packs | ✅ Persona Packs |
| L6 | ✅ Engine (dispatcher) | ✅ Engine (dispatcher) |
| L7 | ❌ NOT USED | ✅ Governance Layer |
| L8 | ✅ Workflows (simple) | ✅ Workflows (governed) |
| L9 | ❌ NOT USED | ✅ Ledger & Proof |

---

## 🚨 CRITICAL REMINDER

**KuasaTurbo is NOT a governance platform.**  
**KuasaTurbo is a lightweight microservices platform.**

If you see governance features creeping into KuasaTurbo:
1. Stop immediately
2. Remove the governance logic
3. Simplify to stateless workflow
4. Verify against this document

---

## 📖 RELATED DOCUMENTATION

- Phase E Summary: `l6/PHASE_E_SUMMARY.md` (Vertical Packs)
- Phase F Summary: `l5/PHASE_F_SUMMARY.md` (Persona Packs)
- Vertical Schema: `verticals/spec/vertical_pack_schema.json`
- Persona Schema: `l5/schema/persona_pack_schema.json`

---

**Document Version**: 1.0.0  
**Last Updated**: December 8, 2025  
**Status**: MANDATORY - Always Included  
**Priority**: CRITICAL
