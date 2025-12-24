-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

CREATE OR REPLACE VIEW public.v_execution_summary AS
SELECT 
    pl.execution_class,
    pl.runner_type,
    COUNT(em.id) AS total_executions,
    AVG(em.estimated_credits) AS avg_estimated_credits,
    AVG(em.actual_credits) AS avg_actual_credits,
    MAX(em.created_at) AS last_execution_at
FROM public.proof_ledger pl
LEFT JOIN public.execution_meter em ON pl.id = em.proof_id
GROUP BY pl.execution_class, pl.runner_type
ORDER BY last_execution_at DESC;