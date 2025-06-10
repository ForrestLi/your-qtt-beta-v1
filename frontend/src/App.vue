<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
          <router-link class="navbar-brand" to="/">
            <i class="fas fa-chart-line me-2"></i>
            RiskWise Analytics
          </router-link>
          <button 
            class="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/">
                  Home
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/about">
                  About
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <div class="container py-4">
        <router-view />
      </div>
    </main>

    <footer class="app-footer bg-dark text-white py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5>RiskWise Analytics</h5>
            <p class="mb-0">Market analysis and risk management platform</p>
          </div>
          <div class="col-md-6 text-md-end">
            <p class="mb-0">&copy; 2025 RiskWise Analytics. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
  setup() {
    return {};
  },
});
</script>

<style lang="scss" scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.app-footer {
  margin-top: auto;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  
  .navbar-brand {
    font-weight: 600;
    display: flex;
    align-items: center;
    
    i {
      margin-right: 0.5rem;
    }
  }
  
  .nav-link {
    font-weight: 500;
    padding: 0.5rem 1rem;
    
    &.router-link-active {
      color: rgba(255, 255, 255, 0.9) !important;
      font-weight: 600;
    }
  }
}

// Responsive adjustments
@media (max-width: 767.98px) {
  .main-content {
    padding: 1rem 0;
  }
}
</style>
