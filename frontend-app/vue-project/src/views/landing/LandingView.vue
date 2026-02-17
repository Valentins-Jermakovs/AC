<template>
  <!--
    Wrap the whole page content in a transition for fade-in effect
    The 'appear' attribute makes the animation happen when the page first loads
  -->
  <Transition name="fade" appear>
    <div>
      <!-- Main sections of the landing page -->
      <HeroSection></HeroSection>           <!-- Top hero banner with main message -->
      <AboutSection></AboutSection>         <!-- Section describing the product/company -->
      <FeaturesSection></FeaturesSection>   <!-- List of key features -->
      <CTASection></CTASection>             <!-- Call-to-action section -->
      <Footer></Footer>                     <!-- Footer with links and info -->
      <LanguageSelector></LanguageSelector> <!-- Language switcher component -->
    </div>
  </Transition>
</template>

<script>
// Import all components used in this page
import LanguageSelector from '@/components/common/LanguageSelector.vue'
import AboutSection from '@/components/landing/AboutSection.vue'
import CTASection from '@/components/landing/CTASection.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import Footer from '@/components/landing/Footer.vue'
import HeroSection from '@/components/landing/HeroSection.vue'

export default {
  // Register all imported components to be used in the template
  components: {
    AboutSection,
    CTASection,
    FeaturesSection,
    Footer,
    HeroSection,
    LanguageSelector,
  },
}
</script>

<style scoped>
/* Fade transition styles for the <Transition> wrapper */

/* Active transition: how the element changes while entering or leaving */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease; /* smooth 1-second fade */
}

/* Initial and final states of the fade */
.fade-enter-from,
.fade-leave-to {
  opacity: 0; /* start invisible and fade to visible */
}
</style>
