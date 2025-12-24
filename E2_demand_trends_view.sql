-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

CREATE OR REPLACE VIEW public.v_demand_trends AS
SELECT 
    signal_type,
    COUNT(*) AS signal_count,
    MAX(created_at) AS last_seen_at
FROM public.demand_signals
GROUP BY signal_type
ORDER BY last_seen_at DESC;