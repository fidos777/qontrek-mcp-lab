import HeroChooser from '@/components/home/HeroChooser';
import TopKerja from '@/components/home/TopKerja';
import HowItWorks from '@/components/home/HowItWorks';
import CreditTeaser from '@/components/home/CreditTeaser';
import PilotVerticals from '@/components/home/PilotVerticals';
import PartnerTeaser from '@/components/home/PartnerTeaser';
import TrustSection from '@/components/home/TrustSection';
import FinalCTA from '@/components/home/FinalCTA';

export default function HomePage() {
  return (
    <>
      <HeroChooser />
      <TopKerja />
      <HowItWorks />
      <CreditTeaser />
      <PilotVerticals />
      <PartnerTeaser />
      <TrustSection />
      <FinalCTA />
    </>
  );
}