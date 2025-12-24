-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

CREATE OR REPLACE VIEW public.v_proof_signal_context AS
SELECT 
    pl.id AS proof_id,
    pl.execution_class,
    pl.authority_surface,
    pl.policy_version,
    ds.signal_type AS related_signal_type,
    ds.created_at AS signal_created_at
FROM public.proof_ledger pl
LEFT JOIN public.demand_signals ds ON DATE(pl.created_at) = DATE(ds.created_at)
ORDER BY pl.created_at DESC;