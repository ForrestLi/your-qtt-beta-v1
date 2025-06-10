<template>
  <div class="home">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 text-center">
          <h1 class="display-4 mb-4">Welcome to RiskWise Analytics</h1>
          <p class="lead">Your comprehensive market analysis and risk management solution</p>
          <router-link to="/about" class="btn btn-primary btn-lg mt-3">
            Learn More
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  setup() {
    return {};
  },
});
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

.display-4 {
  font-weight: 600;
  color: var(--bs-primary);
  margin-bottom: 1.5rem;
}

.lead {
  font-size: 1.5rem;
  color: #495057;
  margin-bottom: 2rem;
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-size: 1.25rem;
  border-radius: 2rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-lg:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
}
</style>
