<template>
  <div class="about">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <h1 class="display-4 mb-4">About RiskWise Analytics</h1>
          
          <div class="card mb-4">
            <div class="card-body">
              <h2 class="h4 mb-3">Our Mission</h2>
              <p class="mb-0">
                To provide comprehensive market analysis and risk management solutions that empower traders and investors 
                to make informed decisions in today's dynamic financial markets.
              </p>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-body">
              <h2 class="h4 mb-3">Key Features</h2>
              <ul class="list-unstyled">
                <li class="mb-2">
                  <i class="fas fa-chart-line text-primary me-2"></i>
                  Real-time market data and analysis
                </li>
                <li class="mb-2">
                  <i class="fas fa-shield-alt text-primary me-2"></i>
                  Advanced risk assessment tools
                </li>
                <li class="mb-2">
                  <i class="fas fa-bell text-primary me-2"></i>
                  Customizable alerts and notifications
                </li>
                <li class="mb-2">
                  <i class="fas fa-chart-pie text-primary me-2"></i>
                  Interactive data visualization
                </li>
              </ul>
            </div>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-start">
            <router-link to="/" class="btn btn-outline-primary me-md-2">
              <i class="fas fa-arrow-left me-2"></i>Back to Home
            </router-link>
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
  padding: 2rem 0;
}

.display-4 {
  font-weight: 600;
  color: var(--bs-primary);
  margin-bottom: 1.5rem;
}

.card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 1.5rem;
}

.h4 {
  color: #2c3e50;
  font-weight: 600;
}

.list-unstyled li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f1f1;
}

.list-unstyled li:last-child {
  border-bottom: none;
}

.btn-outline-primary {
  border-radius: 2rem;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.15);
}
</style>
