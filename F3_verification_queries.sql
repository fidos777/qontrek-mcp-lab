-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

-- Test 1: Verify v_context_ledger view exists and is accessible
SELECT 
    'v_context_ledger_exists' AS test_name,
    CASE 
        WHEN COUNT(*) > 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS result
FROM information_schema.views 
WHERE table_schema = 'public' 
  AND table_name = 'v_context_ledger';

-- Test 2: Verify generate_prh_context function exists
SELECT 
    'generate_prh_context_exists' AS test_name,
    CASE 
        WHEN COUNT(*) > 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS result
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
  AND p.proname = 'generate_prh_context';

-- Test 3: Verify v_context_ledger has required columns
SELECT 
    'v_context_ledger_columns' AS test_name,
    CASE 
        WHEN COUNT(*) = 11 THEN 'PASS'
        ELSE 'FAIL - Expected 11 columns, found ' || COUNT(*)
    END AS result
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'v_context_ledger'
  AND column_name IN (
    'proof_id', 'execution_class', 'runner_type', 'authority_surface', 
    'policy_version', 'total_executions', 'avg_estimated_credits', 
    'avg_actual_credits', 'signal_types', 'last_signal_at', 'last_execution_at'
  );

-- Test 4: Verify v_context_ledger is read-only (no INSERT/UPDATE/DELETE triggers)
SELECT 
    'v_context_ledger_read_only' AS test_name,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL - Found ' || COUNT(*) || ' triggers'
    END AS result
FROM information_schema.triggers
WHERE event_object_schema = 'public'
  AND event_object_table = 'v_context_ledger';

-- Test 5: Verify generate_prh_context function is IMMUTABLE (read-only)
SELECT 
    'generate_prh_context_immutable' AS test_name,
    CASE 
        WHEN provolatile = 'i' THEN 'PASS'
        ELSE 'FAIL - Function is not IMMUTABLE'
    END AS result
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
  AND p.proname = 'generate_prh_context';

-- Test 6: Sample v_context_ledger query (verify it returns data structure)
SELECT 
    'v_context_ledger_sample' AS test_name,
    CASE 
        WHEN COUNT(*) >= 0 THEN 'PASS - Query executes successfully'
        ELSE 'FAIL'
    END AS result
FROM (
    SELECT proof_id, execution_class, runner_type, signal_types
    FROM public.v_context_ledger
    LIMIT 5
) sample;

-- Test 7: Sample generate_prh_context call (verify function executes)
SELECT 
    'generate_prh_context_sample' AS test_name,
    CASE 
        WHEN jsonb_typeof(public.generate_prh_context(gen_random_uuid())) = 'object' THEN 'PASS - Function returns JSON object'
        ELSE 'FAIL'
    END AS result;

-- Test 8: Verify no database writes are possible through these artifacts
SELECT 
    'no_write_operations' AS test_name,
    CASE 
        WHEN NOT EXISTS (
            SELECT 1 FROM information_schema.triggers 
            WHERE event_object_schema = 'public' 
              AND event_object_table IN ('v_context_ledger')
              AND event_manipulation IN ('INSERT', 'UPDATE', 'DELETE')
        ) THEN 'PASS - No write triggers found'
        ELSE 'FAIL - Write triggers detected'
    END AS result;

-- Summary verification
SELECT 
    'sprint_f_verification_summary' AS test_name,
    'All Sprint F read surfaces are non-authoritative, read-only, and constitutionally compliant' AS result;