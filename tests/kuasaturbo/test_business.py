"""
Test Suite for Business Layer (Phase XVIII)

Tests consultant, reseller, and partner management.
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.business.consultants import ConsultantManager
from kuasaturbo.business.resellers import ResellerManager
from kuasaturbo.business.partners import PartnerManager
from kuasaturbo.database.connection import get_db_connection, init_database, DB_PATH


class TestConsultantManager(unittest.TestCase):
    """Test consultant management"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize database"""
        if DB_PATH.exists():
            DB_PATH.unlink()
        init_database()
    
    def test_create_consultant(self):
        """Test consultant creation"""
        print("\n[Test] Creating consultant")
        
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="test_tenant_1",
            name="John Doe",
            email="john@example.com",
            phone="+60123456789",
            commission_rate=15.0
        )
        
        self.assertIsNotNone(consultant_id)
        self.assertTrue(consultant_id.startswith("cons_"))
        
        print(f"[Test] ✓ Consultant created: {consultant_id}")
    
    def test_get_consultant(self):
        """Test getting consultant details"""
        print("\n[Test] Getting consultant")
        
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="test_tenant_1",
            name="Jane Smith",
            email="jane@example.com",
            commission_rate=12.5
        )
        
        consultant = ConsultantManager.get_consultant(consultant_id)
        
        self.assertIsNotNone(consultant)
        self.assertEqual(consultant['name'], "Jane Smith")
        self.assertEqual(consultant['email'], "jane@example.com")
        self.assertEqual(consultant['commission_rate'], 12.5)
        self.assertEqual(consultant['status'], "active")
        
        print(f"[Test] ✓ Retrieved consultant: {consultant['name']}")
    
    def test_list_consultants(self):
        """Test listing consultants"""
        print("\n[Test] Listing consultants")
        
        # Create multiple consultants
        for i in range(3):
            ConsultantManager.create_consultant(
                tenant_id="test_tenant_2",
                name=f"Consultant {i}",
                email=f"consultant{i}@example.com"
            )
        
        consultants = ConsultantManager.list_consultants("test_tenant_2")
        
        self.assertEqual(len(consultants), 3)
        
        print(f"[Test] ✓ Listed {len(consultants)} consultants")
    
    def test_update_consultant(self):
        """Test updating consultant"""
        print("\n[Test] Updating consultant")
        
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="test_tenant_1",
            name="Old Name",
            email="old@example.com"
        )
        
        success = ConsultantManager.update_consultant(
            consultant_id=consultant_id,
            name="New Name",
            email="new@example.com",
            commission_rate=20.0
        )
        
        self.assertTrue(success)
        
        consultant = ConsultantManager.get_consultant(consultant_id)
        self.assertEqual(consultant['name'], "New Name")
        self.assertEqual(consultant['email'], "new@example.com")
        self.assertEqual(consultant['commission_rate'], 20.0)
        
        print(f"[Test] ✓ Consultant updated")
    
    def test_record_sale_and_earnings(self):
        """Test recording sale and calculating earnings"""
        print("\n[Test] Recording sale and calculating earnings")
        
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="test_tenant_1",
            name="Sales Person",
            email="sales@example.com",
            commission_rate=10.0
        )
        
        # Record sales
        ConsultantManager.record_sale(consultant_id, 1000.0)
        ConsultantManager.record_sale(consultant_id, 500.0)
        
        # Get earnings summary
        summary = ConsultantManager.get_earnings_summary(consultant_id)
        
        self.assertEqual(summary['total_sales'], 2)
        self.assertEqual(summary['total_earnings'], 150.0)  # 10% of 1500
        self.assertEqual(summary['commission_rate'], 10.0)
        
        print(f"[Test] ✓ Earnings: {summary['total_earnings']} from {summary['total_sales']} sales")
    
    def test_delete_consultant(self):
        """Test deleting consultant (soft delete)"""
        print("\n[Test] Deleting consultant")
        
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="test_tenant_1",
            name="To Delete",
            email="delete@example.com"
        )
        
        success = ConsultantManager.delete_consultant(consultant_id)
        self.assertTrue(success)
        
        consultant = ConsultantManager.get_consultant(consultant_id)
        self.assertEqual(consultant['status'], "inactive")
        
        print(f"[Test] ✓ Consultant soft deleted")


class TestResellerManager(unittest.TestCase):
    """Test reseller management"""
    
    def test_create_reseller(self):
        """Test reseller creation"""
        print("\n[Test] Creating reseller")
        
        reseller_id = ResellerManager.create_reseller(
            tenant_id="test_tenant_1",
            company_name="Tech Solutions Inc",
            contact_name="Alice Johnson",
            email="alice@techsolutions.com",
            tier="gold"
        )
        
        self.assertIsNotNone(reseller_id)
        self.assertTrue(reseller_id.startswith("res_"))
        
        print(f"[Test] ✓ Reseller created: {reseller_id}")
    
    def test_get_reseller(self):
        """Test getting reseller details"""
        print("\n[Test] Getting reseller")
        
        reseller_id = ResellerManager.create_reseller(
            tenant_id="test_tenant_1",
            company_name="Digital Partners",
            contact_name="Bob Wilson",
            email="bob@digitalpartners.com",
            tier="silver"
        )
        
        reseller = ResellerManager.get_reseller(reseller_id)
        
        self.assertIsNotNone(reseller)
        self.assertEqual(reseller['company_name'], "Digital Partners")
        self.assertEqual(reseller['tier'], "silver")
        self.assertEqual(reseller['commission_rate'], 10.0)  # Silver tier
        
        print(f"[Test] ✓ Retrieved reseller: {reseller['company_name']}")
    
    def test_tier_commission_rates(self):
        """Test tier-based commission rates"""
        print("\n[Test] Testing tier commission rates")
        
        tiers = {
            "bronze": 5.0,
            "silver": 10.0,
            "gold": 15.0,
            "platinum": 20.0
        }
        
        for tier, expected_rate in tiers.items():
            reseller_id = ResellerManager.create_reseller(
                tenant_id="test_tenant_1",
                company_name=f"{tier.capitalize()} Company",
                contact_name="Test Contact",
                email=f"{tier}@example.com",
                tier=tier
            )
            
            reseller = ResellerManager.get_reseller(reseller_id)
            self.assertEqual(reseller['commission_rate'], expected_rate)
            
            print(f"[Test] ✓ {tier.capitalize()} tier: {expected_rate}% commission")
    
    def test_update_reseller_tier(self):
        """Test updating reseller tier"""
        print("\n[Test] Updating reseller tier")
        
        reseller_id = ResellerManager.create_reseller(
            tenant_id="test_tenant_1",
            company_name="Growing Company",
            contact_name="Charlie Brown",
            email="charlie@growing.com",
            tier="bronze"
        )
        
        # Upgrade to platinum
        success = ResellerManager.update_reseller(
            reseller_id=reseller_id,
            tier="platinum"
        )
        
        self.assertTrue(success)
        
        reseller = ResellerManager.get_reseller(reseller_id)
        self.assertEqual(reseller['tier'], "platinum")
        self.assertEqual(reseller['commission_rate'], 20.0)
        
        print(f"[Test] ✓ Tier upgraded to platinum (20% commission)")
    
    def test_record_sale_and_earnings(self):
        """Test recording sale and calculating earnings"""
        print("\n[Test] Recording reseller sale")
        
        reseller_id = ResellerManager.create_reseller(
            tenant_id="test_tenant_1",
            company_name="Sales Corp",
            contact_name="Diana Prince",
            email="diana@salescorp.com",
            tier="gold"  # 15% commission
        )
        
        # Record sales
        ResellerManager.record_sale(reseller_id, 2000.0)
        ResellerManager.record_sale(reseller_id, 1000.0)
        
        # Get earnings summary
        summary = ResellerManager.get_earnings_summary(reseller_id)
        
        self.assertEqual(summary['total_sales'], 2)
        self.assertEqual(summary['total_earnings'], 450.0)  # 15% of 3000
        self.assertEqual(summary['tier'], "gold")
        
        print(f"[Test] ✓ Earnings: {summary['total_earnings']} from {summary['total_sales']} sales")
    
    def test_list_resellers_by_tier(self):
        """Test listing resellers filtered by tier"""
        print("\n[Test] Listing resellers by tier")
        
        # Create resellers with different tiers
        ResellerManager.create_reseller(
            tenant_id="test_tenant_3",
            company_name="Bronze Co",
            contact_name="Test",
            email="bronze@test.com",
            tier="bronze"
        )
        ResellerManager.create_reseller(
            tenant_id="test_tenant_3",
            company_name="Gold Co",
            contact_name="Test",
            email="gold@test.com",
            tier="gold"
        )
        
        # List gold tier only
        gold_resellers = ResellerManager.list_resellers(
            tenant_id="test_tenant_3",
            tier="gold"
        )
        
        self.assertEqual(len(gold_resellers), 1)
        self.assertEqual(gold_resellers[0]['tier'], "gold")
        
        print(f"[Test] ✓ Listed {len(gold_resellers)} gold tier resellers")


class TestPartnerManager(unittest.TestCase):
    """Test partner management"""
    
    def test_create_partner(self):
        """Test partner creation"""
        print("\n[Test] Creating partner")
        
        partner_id = PartnerManager.create_partner(
            tenant_id="test_tenant_1",
            company_name="Strategic Alliance Corp",
            contact_name="Eve Adams",
            email="eve@strategic.com",
            partnership_type="enterprise"
        )
        
        self.assertIsNotNone(partner_id)
        self.assertTrue(partner_id.startswith("part_"))
        
        print(f"[Test] ✓ Partner created: {partner_id}")
    
    def test_get_partner(self):
        """Test getting partner details"""
        print("\n[Test] Getting partner")
        
        partner_id = PartnerManager.create_partner(
            tenant_id="test_tenant_1",
            company_name="Premium Partners LLC",
            contact_name="Frank Miller",
            email="frank@premium.com",
            partnership_type="premium"
        )
        
        partner = PartnerManager.get_partner(partner_id)
        
        self.assertIsNotNone(partner)
        self.assertEqual(partner['company_name'], "Premium Partners LLC")
        self.assertEqual(partner['partnership_type'], "premium")
        self.assertEqual(partner['revenue_share_rate'], 20.0)  # Premium type
        
        print(f"[Test] ✓ Retrieved partner: {partner['company_name']}")
    
    def test_partnership_type_rates(self):
        """Test partnership type revenue share rates"""
        print("\n[Test] Testing partnership type rates")
        
        types = {
            "standard": 10.0,
            "premium": 20.0,
            "enterprise": 30.0,
            "strategic": 40.0
        }
        
        for ptype, expected_rate in types.items():
            partner_id = PartnerManager.create_partner(
                tenant_id="test_tenant_1",
                company_name=f"{ptype.capitalize()} Partner",
                contact_name="Test Contact",
                email=f"{ptype}@example.com",
                partnership_type=ptype
            )
            
            partner = PartnerManager.get_partner(partner_id)
            self.assertEqual(partner['revenue_share_rate'], expected_rate)
            
            print(f"[Test] ✓ {ptype.capitalize()} type: {expected_rate}% revenue share")
    
    def test_record_referral_and_revenue(self):
        """Test recording referral and calculating revenue"""
        print("\n[Test] Recording partner referral")
        
        partner_id = PartnerManager.create_partner(
            tenant_id="test_tenant_1",
            company_name="Referral Masters",
            contact_name="Grace Lee",
            email="grace@referralmasters.com",
            partnership_type="enterprise"  # 30% revenue share
        )
        
        # Record referrals
        PartnerManager.record_referral(partner_id, 5000.0)
        PartnerManager.record_referral(partner_id, 3000.0)
        
        # Get revenue summary
        summary = PartnerManager.get_revenue_summary(partner_id)
        
        self.assertEqual(summary['total_referrals'], 2)
        self.assertEqual(summary['total_revenue'], 2400.0)  # 30% of 8000
        self.assertEqual(summary['partnership_type'], "enterprise")
        
        print(f"[Test] ✓ Revenue: {summary['total_revenue']} from {summary['total_referrals']} referrals")
    
    def test_update_partnership_type(self):
        """Test updating partnership type"""
        print("\n[Test] Updating partnership type")
        
        partner_id = PartnerManager.create_partner(
            tenant_id="test_tenant_1",
            company_name="Evolving Partner",
            contact_name="Henry Ford",
            email="henry@evolving.com",
            partnership_type="standard"
        )
        
        # Upgrade to strategic
        success = PartnerManager.update_partner(
            partner_id=partner_id,
            partnership_type="strategic"
        )
        
        self.assertTrue(success)
        
        partner = PartnerManager.get_partner(partner_id)
        self.assertEqual(partner['partnership_type'], "strategic")
        self.assertEqual(partner['revenue_share_rate'], 40.0)
        
        print(f"[Test] ✓ Partnership upgraded to strategic (40% revenue share)")


class TestMultiTenantIsolation(unittest.TestCase):
    """Test multi-tenant isolation"""
    
    def test_consultant_isolation(self):
        """Test consultant multi-tenant isolation"""
        print("\n[Test] Testing consultant tenant isolation")
        
        # Create consultants for different tenants
        c1 = ConsultantManager.create_consultant(
            tenant_id="tenant_a",
            name="Consultant A",
            email="a@example.com"
        )
        c2 = ConsultantManager.create_consultant(
            tenant_id="tenant_b",
            name="Consultant B",
            email="b@example.com"
        )
        
        # List consultants for tenant_a
        consultants_a = ConsultantManager.list_consultants("tenant_a")
        
        # Should only see tenant_a's consultant
        self.assertEqual(len(consultants_a), 1)
        self.assertEqual(consultants_a[0]['consultant_id'], c1)
        
        print(f"[Test] ✓ Tenant isolation verified for consultants")
    
    def test_reseller_isolation(self):
        """Test reseller multi-tenant isolation"""
        print("\n[Test] Testing reseller tenant isolation")
        
        # Create resellers for different tenants
        r1 = ResellerManager.create_reseller(
            tenant_id="tenant_a",
            company_name="Company A",
            contact_name="Contact A",
            email="a@company.com"
        )
        r2 = ResellerManager.create_reseller(
            tenant_id="tenant_b",
            company_name="Company B",
            contact_name="Contact B",
            email="b@company.com"
        )
        
        # List resellers for tenant_a
        resellers_a = ResellerManager.list_resellers("tenant_a")
        
        # Should only see tenant_a's reseller
        self.assertEqual(len(resellers_a), 1)
        self.assertEqual(resellers_a[0]['reseller_id'], r1)
        
        print(f"[Test] ✓ Tenant isolation verified for resellers")
    
    def test_partner_isolation(self):
        """Test partner multi-tenant isolation"""
        print("\n[Test] Testing partner tenant isolation")
        
        # Create partners for different tenants
        p1 = PartnerManager.create_partner(
            tenant_id="tenant_a",
            company_name="Partner A",
            contact_name="Contact A",
            email="a@partner.com"
        )
        p2 = PartnerManager.create_partner(
            tenant_id="tenant_b",
            company_name="Partner B",
            contact_name="Contact B",
            email="b@partner.com"
        )
        
        # List partners for tenant_a
        partners_a = PartnerManager.list_partners("tenant_a")
        
        # Should only see tenant_a's partner
        self.assertEqual(len(partners_a), 1)
        self.assertEqual(partners_a[0]['partner_id'], p1)
        
        print(f"[Test] ✓ Tenant isolation verified for partners")


def run_tests():
    """Run all business layer tests"""
    print("\n" + "="*70)
    print("PHASE XVIII - BUSINESS LAYER TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConsultantManager))
    suite.addTests(loader.loadTestsFromTestCase(TestResellerManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPartnerManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiTenantIsolation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
