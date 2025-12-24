-- Non-authoritative
-- Interpretability only
-- Signals ≠ verdicts

CREATE OR REPLACE FUNCTION public.generate_prh_context(input_proof_id UUID)
RETURNS JSONB
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    context_record RECORD;
    signal_records RECORD;
    result JSONB;
BEGIN
    -- Get context ledger data for the proof
    SELECT 
        proof_id,
        execution_class,
        runner_type,
        authority_surface,
        policy_version,
        total_executions,
        avg_estimated_credits,
        avg_actual_credits,
        signal_types,
        last_signal_at,
        last_execution_at,
        proof_created_at
    INTO context_record
    FROM public.v_context_ledger
    WHERE proof_id = input_proof_id;
    
    -- If no record found, return minimal context
    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'disclaimer', 'This is not a recommendation',
            'descriptive_summary', 'No context data available for the specified proof ID',
            'observed_signals', jsonb_build_array(),
            'execution_context', jsonb_build_object(),
            'temporal_context', jsonb_build_object()
        );
    END IF;
    
    -- Build the result object
    result := jsonb_build_object(
        'disclaimer', 'This is not a recommendation',
        'descriptive_summary', format(
            'Proof %s represents execution class "%s" with runner type "%s". Authority surface is "%s" under policy version "%s". This proof was created on %s.',
            context_record.proof_id,
            COALESCE(context_record.execution_class, 'unspecified'),
            COALESCE(context_record.runner_type, 'unspecified'),
            COALESCE(context_record.authority_surface, 'unspecified'),
            COALESCE(context_record.policy_version, 'unspecified'),
            COALESCE(context_record.proof_created_at::TEXT, 'unknown date')
        ),
        'observed_signals', jsonb_build_object(
            'signal_types_present', COALESCE(context_record.signal_types, ARRAY[]::TEXT[]),
            'last_signal_timestamp', COALESCE(context_record.last_signal_at::TEXT, 'no signals observed'),
            'signal_count', array_length(COALESCE(context_record.signal_types, ARRAY[]::TEXT[]), 1)
        ),
        'execution_context', jsonb_build_object(
            'total_executions_for_class_runner', COALESCE(context_record.total_executions, 0),
            'average_estimated_credits', COALESCE(context_record.avg_estimated_credits, 0),
            'average_actual_credits', COALESCE(context_record.avg_actual_credits, 0),
            'last_execution_timestamp', COALESCE(context_record.last_execution_at::TEXT, 'no executions observed')
        ),
        'temporal_context', jsonb_build_object(
            'proof_age_description', CASE 
                WHEN context_record.proof_created_at > NOW() - INTERVAL '1 day' THEN 'created within last day'
                WHEN context_record.proof_created_at > NOW() - INTERVAL '7 days' THEN 'created within last week'
                WHEN context_record.proof_created_at > NOW() - INTERVAL '30 days' THEN 'created within last month'
                ELSE 'created more than a month ago'
            END,
            'signal_recency_description', CASE 
                WHEN context_record.last_signal_at IS NULL THEN 'no signals observed'
                WHEN context_record.last_signal_at > NOW() - INTERVAL '1 day' THEN 'signals observed within last day'
                WHEN context_record.last_signal_at > NOW() - INTERVAL '7 days' THEN 'signals observed within last week'
                ELSE 'signals observed more than a week ago'
            END,
            'execution_recency_description', CASE 
                WHEN context_record.last_execution_at IS NULL THEN 'no executions observed'
                WHEN context_record.last_execution_at > NOW() - INTERVAL '1 day' THEN 'executions observed within last day'
                WHEN context_record.last_execution_at > NOW() - INTERVAL '7 days' THEN 'executions observed within last week'
                ELSE 'executions observed more than a week ago'
            END
        )
    );
    
    RETURN result;
END;
$$;