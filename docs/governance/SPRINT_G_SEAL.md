# Sprint G — Constitutional Freeze (SEALED)

## Constitution
- CIVOS Version: v1.6

## Scope
Sprint G permanently hardens CIVOS against:
- Authority creep
- Governance theatre
- Silent decision escalation

## Production Verification
- Supabase function: create_constitutional_checkpoint()
- Volatility: VOLATILE (correct)
- Checkpoint name: SPRINT_G_CONSTITUTIONAL_LOCK
- Timestamp: (see database)

## Locked Artifacts

Tables:
- proof_ledger
- execution_meter
- demand_signals

Views:
- v_execution_summary
- v_demand_trends
- v_proof_signal_context
- v_context_ledger

Functions:
- estimate_credit_cost()
- insert_proof_v2()
- generate_prh_context()

## Authority Declaration

The system MAY:
- Observe
- Record proof
- Display signals

The system MAY NOT:
- Decide
- Approve
- Reject
- Enforce
- Escalate
- Recommend actions

## Amendment Rule

Any modification to locked artifacts requires:
1. Constitutional amendment proposal
2. Checkpoint comparison
3. Explicit governance approval

Status: SEALED