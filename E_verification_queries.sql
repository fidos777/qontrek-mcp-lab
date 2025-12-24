-- Non-authoritative
-- Interpretability only  
-- Signals ≠ verdicts

-- Test 1: Verify signal insertion capability
INSERT INTO public.demand_signals (signal_type, payload) 
VALUES ('manual_observation', '{"observer": "test", "observation_type": "verification", "description": "Sprint E test signal"}');

-- Test 2: Verify views can read signals
SELECT 
    'v_demand_trends' as view_name,
    COUNT(*) as signal_count
FROM public.v_demand_trends
WHERE signal_type = 'manual_observation'

UNION ALL

SELECT 
    'v_proof_signal_context' as view_name,
    COUNT(*) as context_rows
FROM public.v_proof_signal_context
WHERE related_signal_type = 'manual_observation';

-- Test 3: Verify execution summary aggregation
SELECT 
    'v_execution_summary' as view_name,
    COUNT(*) as summary_rows,
    COUNT(DISTINCT execution_class) as execution_classes,
    COUNT(DISTINCT runner_type) as runner_types
FROM public.v_execution_summary;

-- Test 4: Verify signal payload structure
SELECT 
    signal_type,
    jsonb_typeof(payload) as payload_type,
    jsonb_object_keys(payload) as payload_keys
FROM public.demand_signals 
WHERE signal_type = 'manual_observation'
LIMIT 1;

-- Test 5: Verify time-based correlation
SELECT 
    DATE(ds.created_at) as signal_date,
    COUNT(ds.id) as signal_count,
    COUNT(DISTINCT pl.id) as proof_count
FROM public.demand_signals ds
LEFT JOIN public.proof_ledger pl ON DATE(ds.created_at) = DATE(pl.created_at)
GROUP BY DATE(ds.created_at)
ORDER BY signal_date DESC
LIMIT 5;

-- Cleanup test data
DELETE FROM public.demand_signals 
WHERE signal_type = 'manual_observation' 
  AND payload->>'description' = 'Sprint E test signal';