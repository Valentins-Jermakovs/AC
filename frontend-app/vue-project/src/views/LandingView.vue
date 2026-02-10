<template>
    <Transition name="fade" appear>
        <div>
            <HeroSection></HeroSection>
            <AboutSection></AboutSection>
            <FeaturesSection></FeaturesSection>
            <CTASection></CTASection>
            <Footer></Footer>
            <LanguageSelector></LanguageSelector>
        </div>
    </Transition>
</template>

<script>
import LanguageSelector from '@/components/common/LanguageSelector.vue';
import AboutSection from '@/components/landing/AboutSection.vue';
import CTASection from '@/components/landing/CTASection.vue';
import FeaturesSection from '@/components/landing/FeaturesSection.vue';
import Footer from '@/components/landing/Footer.vue';
import HeroSection from '@/components/landing/HeroSection.vue';

export default {
    components: {
        AboutSection,
        CTASection,
        FeaturesSection,
        Footer,
        HeroSection,
        LanguageSelector
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.0s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>