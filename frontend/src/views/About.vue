<template>
  <div class="about">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body p-5">
              <h1 class="display-4 text-center mb-4">About RiskWise Analytics</h1>
              <p class="lead text-center mb-5">
                Smart Risk Hedging Platform for Modern Investors
              </p>
              
              <div class="mb-5">
                <h2 class="h4 mb-3">Our Mission</h2>
                <p>
                  RiskWise Analytics provides institutional-grade risk analysis tools to help investors make 
                  informed decisions in today's complex financial markets. Our platform combines traditional 
                  fundamental analysis with modern quantitative techniques to deliver actionable insights.
                </p>
              </div>

              <div class="mb-5">
                <h2 class="h4 mb-3">Key Features</h2>
                <ul class="list-unstyled">
                  <li class="mb-3">
                    <i class="fas fa-chart-line text-primary me-2"></i>
                    <strong>Market Beta Analysis:</strong> Real-time valuation metrics and historical analysis
                  </li>
                  <li class="mb-3">
                    <i class="fas fa-star text-primary me-2"></i>
                    <strong>Stock Alpha Analysis:</strong> Buffett-style fundamental analysis for individual stocks
                  </li>
                  <li class="mb-3">
                    <i class="fas fa-flask text-primary me-2"></i>
                    <strong>Strategy Fitness Lab:</strong> Backtesting environment for trading strategies
                  </li>
                </ul>
              </div>

              <div class="text-center mt-5">
                <router-link to="/" class="btn btn-primary btn-lg px-4">
                  <i class="fas fa-arrow-left me-2"></i> Back to Dashboard
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AboutView',
  setup() {
    return {};
  },
});
</script>

<style scoped>
.about {
  min-height: calc(100vh - 200px);
  background-color: var(--bs-light-bg-subtle);
}

.card {
  border: none;
  border-radius: 1rem;
  overflow: hidden;
}

.list-unstyled li {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.list-unstyled li:last-child {
  border-bottom: none;
}

.btn-primary {
  padding: 0.75rem 2rem;
  font-weight: 500;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(13, 110, 253, 0.2);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 110, 253, 0.3);
}
</style>
