-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

CREATE OR REPLACE VIEW public.v_context_ledger AS
SELECT 
    pl.id AS proof_id,
    pl.execution_class,
    pl.runner_type,
    pl.authority_surface,
    pl.policy_version,
    COALESCE(es.total_executions, 0) AS total_executions,
    es.avg_estimated_credits,
    es.avg_actual_credits,
    COALESCE(
        ARRAY_AGG(DISTINCT ds.signal_type) FILTER (WHERE ds.signal_type IS NOT NULL),
        ARRAY[]::TEXT[]
    ) AS signal_types,
    MAX(ds.created_at) AS last_signal_at,
    es.last_execution_at,
    pl.created_at AS proof_created_at
FROM public.proof_ledger pl
LEFT JOIN public.v_execution_summary es ON (
    pl.execution_class = es.execution_class AND 
    pl.runner_type = es.runner_type
)
LEFT JOIN public.demand_signals ds ON DATE(pl.created_at) = DATE(ds.created_at)
GROUP BY 
    pl.id,
    pl.execution_class,
    pl.runner_type,
    pl.authority_surface,
    pl.policy_version,
    pl.created_at,
    es.total_executions,
    es.avg_estimated_credits,
    es.avg_actual_credits,
    es.last_execution_at
ORDER BY pl.created_at DESC;