"""
Wallet Management

Handles credit balance management for tenants.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from kuasaturbo.database.connection import get_db_connection


class WalletManager:
    """Manages tenant wallet balances"""
    
    @staticmethod
    def create_wallet(tenant_id: str, initial_balance: float = 0.0, currency: str = "USD") -> int:
        """
        Create wallet for tenant
        
        Args:
            tenant_id: Tenant identifier
            initial_balance: Initial credit balance
            currency: Currency code
        
        Returns:
            Wallet ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO wallets (tenant_id, balance, currency)
                VALUES (?, ?, ?)
            """, (tenant_id, initial_balance, currency))
            
            conn.commit()
            wallet_id = cursor.lastrowid
            
            print(f"[WalletManager] Created wallet for tenant {tenant_id} with balance {initial_balance} {currency}")
            return wallet_id
        
        except Exception as e:
            conn.rollback()
            print(f"[WalletManager] Error creating wallet: {e}")
            raise
    
    @staticmethod
    def get_wallet(tenant_id: str) -> Optional[Dict[str, Any]]:
        """
        Get wallet for tenant
        
        Args:
            tenant_id: Tenant identifier
        
        Returns:
            Wallet dict or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM wallets
            WHERE tenant_id = ?
        """, (tenant_id,))
        
        row = cursor.fetchone()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_balance(tenant_id: str) -> float:
        """
        Get current balance for tenant
        
        Args:
            tenant_id: Tenant identifier
        
        Returns:
            Current balance (0.0 if wallet doesn't exist)
        """
        wallet = WalletManager.get_wallet(tenant_id)
        
        if not wallet:
            print(f"[WalletManager] Wallet not found for tenant {tenant_id}, returning 0.0")
            return 0.0
        
        return wallet['balance']
    
    @staticmethod
    def add_credits(tenant_id: str, amount: float, description: str = "") -> float:
        """
        Add credits to wallet
        
        Args:
            tenant_id: Tenant identifier
            amount: Amount to add
            description: Optional description
        
        Returns:
            New balance
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get or create wallet
            wallet = WalletManager.get_wallet(tenant_id)
            if not wallet:
                WalletManager.create_wallet(tenant_id, amount)
                return amount
            
            # Update balance
            new_balance = wallet['balance'] + amount
            
            cursor.execute("""
                UPDATE wallets
                SET balance = ?, updated_at = ?
                WHERE tenant_id = ?
            """, (new_balance, datetime.utcnow().isoformat(), tenant_id))
            
            conn.commit()
            
            print(f"[WalletManager] Added {amount} credits to {tenant_id}, new balance: {new_balance}")
            return new_balance
        
        except Exception as e:
            conn.rollback()
            print(f"[WalletManager] Error adding credits: {e}")
            raise
    
    @staticmethod
    def safe_decrement(tenant_id: str, amount: float, transaction_id: str) -> bool:
        """
        Safely decrement credits (atomic operation)
        
        Args:
            tenant_id: Tenant identifier
            amount: Amount to deduct
            transaction_id: Transaction identifier for logging
        
        Returns:
            True if successful, False if insufficient balance
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get current balance
            wallet = WalletManager.get_wallet(tenant_id)
            if not wallet:
                print(f"[WalletManager] Wallet not found for tenant {tenant_id}")
                return False
            
            current_balance = wallet['balance']
            
            # Check sufficient balance
            if current_balance < amount:
                print(f"[WalletManager] Insufficient balance for {tenant_id}: {current_balance} < {amount}")
                return False
            
            # Atomic decrement
            new_balance = current_balance - amount
            
            cursor.execute("""
                UPDATE wallets
                SET balance = ?, updated_at = ?
                WHERE tenant_id = ? AND balance >= ?
            """, (new_balance, datetime.utcnow().isoformat(), tenant_id, amount))
            
            conn.commit()
            
            if cursor.rowcount == 0:
                print(f"[WalletManager] Concurrent modification detected for {tenant_id}")
                return False
            
            print(f"[WalletManager] Deducted {amount} from {tenant_id}, new balance: {new_balance} (tx: {transaction_id})")
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"[WalletManager] Error decrementing credits: {e}")
            return False
    
    @staticmethod
    def refund_credits(tenant_id: str, amount: float, transaction_id: str) -> float:
        """
        Refund credits to wallet
        
        Args:
            tenant_id: Tenant identifier
            amount: Amount to refund
            transaction_id: Transaction identifier for logging
        
        Returns:
            New balance
        """
        new_balance = WalletManager.add_credits(tenant_id, amount, f"Refund for {transaction_id}")
        print(f"[WalletManager] Refunded {amount} to {tenant_id} (tx: {transaction_id})")
        return new_balance
