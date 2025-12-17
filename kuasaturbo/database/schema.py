"""
Database Schema Definitions

Defines all tables for KuasaTurbo platform.
"""

import sqlite3


def create_tables(conn: sqlite3.Connection):
    """
    Create all database tables
    
    Args:
        conn: SQLite connection
    """
    cursor = conn.cursor()
    
    # Audit Log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            tenant_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            execution_id TEXT,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            duration_ms REAL,
            user_agent TEXT,
            ip_address TEXT,
            persona_id TEXT,
            model_id TEXT,
            error_message TEXT,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for audit log
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_audit_tenant 
        ON audit_log(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_audit_request 
        ON audit_log(request_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_audit_execution 
        ON audit_log(execution_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_audit_timestamp 
        ON audit_log(timestamp)
    """)
    
    print("[Schema] Created audit_log table with indexes")
    
    # Wallets Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL DEFAULT 0.0,
            currency TEXT NOT NULL DEFAULT 'USD',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_wallet_tenant 
        ON wallets(tenant_id)
    """)
    
    print("[Schema] Created wallets table with indexes")
    
    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL UNIQUE,
            tenant_id TEXT NOT NULL,
            execution_id TEXT NOT NULL,
            idempotency_key TEXT UNIQUE,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            status TEXT NOT NULL,
            service_id TEXT,
            persona_id TEXT,
            model_id TEXT,
            error_message TEXT,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transaction_tenant 
        ON transactions(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transaction_execution 
        ON transactions(execution_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transaction_idempotency 
        ON transactions(idempotency_key)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transaction_status 
        ON transactions(status)
    """)
    
    print("[Schema] Created transactions table with indexes")
    
    # Execution History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_id TEXT NOT NULL,
            tenant_id TEXT NOT NULL,
            transaction_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            persona_id TEXT,
            model_id TEXT,
            status TEXT NOT NULL,
            input_data TEXT,
            output_data TEXT,
            error_message TEXT,
            duration_ms REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_execution_history_execution 
        ON execution_history(execution_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_execution_history_tenant 
        ON execution_history(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_execution_history_transaction 
        ON execution_history(transaction_id)
    """)
    
    print("[Schema] Created execution_history table with indexes")
    
    # Consultants Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultant_id TEXT NOT NULL UNIQUE,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            commission_rate REAL NOT NULL DEFAULT 0.0,
            total_earnings REAL NOT NULL DEFAULT 0.0,
            total_sales INTEGER NOT NULL DEFAULT 0,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_consultant_tenant 
        ON consultants(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_consultant_status 
        ON consultants(status)
    """)
    
    print("[Schema] Created consultants table with indexes")
    
    # Resellers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reseller_id TEXT NOT NULL UNIQUE,
            tenant_id TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            commission_rate REAL NOT NULL DEFAULT 0.0,
            total_earnings REAL NOT NULL DEFAULT 0.0,
            total_sales INTEGER NOT NULL DEFAULT 0,
            tier TEXT NOT NULL DEFAULT 'bronze',
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reseller_tenant 
        ON resellers(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reseller_status 
        ON resellers(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reseller_tier 
        ON resellers(tier)
    """)
    
    print("[Schema] Created resellers table with indexes")
    
    # Partners Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id TEXT NOT NULL UNIQUE,
            tenant_id TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            revenue_share_rate REAL NOT NULL DEFAULT 0.0,
            total_revenue REAL NOT NULL DEFAULT 0.0,
            total_referrals INTEGER NOT NULL DEFAULT 0,
            partnership_type TEXT NOT NULL DEFAULT 'standard',
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_partner_tenant 
        ON partners(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_partner_status 
        ON partners(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_partner_type 
        ON partners(partnership_type)
    """)
    
    print("[Schema] Created partners table with indexes")
    
    # API Keys Table (Phase XIX)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT NOT NULL UNIQUE,
            tenant_id TEXT NOT NULL,
            api_key TEXT NOT NULL UNIQUE,
            scopes TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_used_at TEXT,
            revoked_at TEXT,
            rotated_at TEXT,
            rotated_from TEXT,
            metadata TEXT
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_api_key_tenant 
        ON api_keys(tenant_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_api_key_status 
        ON api_keys(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_api_key_key 
        ON api_keys(api_key)
    """)
    
    print("[Schema] Created api_keys table with indexes")
    
    # MCP Shadow Log Table (Sprint C-1)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcp_shadow_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_type TEXT NOT NULL,
            validation_result TEXT NOT NULL CHECK (validation_result IN ('rejected', 'malformed', 'scope_violation')),
            reason TEXT NOT NULL,
            request_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_mcp_shadow_validation 
        ON mcp_shadow_log(validation_result)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_mcp_shadow_timestamp 
        ON mcp_shadow_log(timestamp)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_mcp_shadow_hash 
        ON mcp_shadow_log(request_hash)
    """)
    
    print("[Schema] Created mcp_shadow_log table with indexes")
    
    conn.commit()
