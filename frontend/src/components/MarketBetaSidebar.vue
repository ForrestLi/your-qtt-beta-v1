<template>
  <div class="market-beta-sidebar">
    <!-- Market Selection -->
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-light">
        <h6 class="mb-0">Market Selection</h6>
      </div>
      <div class="card-body p-3">
        <div class="mb-3">
          <label class="form-label small text-muted mb-1">Select Market</label>
          <select v-model="selectedMarket" class="form-select form-select-sm">
            <option v-for="market in availableMarkets" :key="market.id" :value="market.id">
              {{ market.name }}
            </option>
          </select>
        </div>
        
        <!-- Time Horizon -->
        <div class="mb-3">
          <label class="form-label small text-muted mb-1">Time Horizon</label>
          <div class="btn-group w-100" role="group">
            <button 
              v-for="period in timePeriods" 
              :key="period.value"
              @click="selectTimePeriod(period.value)"
              class="btn btn-sm"
              :class="[selectedTimePeriod === period.value ? 'btn-primary' : 'btn-outline-secondary']"
            >
              {{ period.label }}
            </button>
          </div>
        </div>
        
        <!-- Valuation Summary -->
        <div class="card bg-light mb-3">
          <div class="card-body p-3">
            <h6 class="card-title small text-muted mb-3">Valuation Summary</h6>
            <div class="d-flex justify-content-between mb-2" v-for="(value, metric) in valuationMetrics" :key="metric">
              <span class="small">{{ metric }}:</span>
              <span class="fw-medium" :class="getMetricClass(metric, value)">
                {{ formatValue(metric, value) }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="d-grid gap-2">
          <button class="btn btn-sm btn-outline-primary">
            <i class="fas fa-download me-1"></i> Export Data
          </button>
          <button class="btn btn-sm btn-outline-secondary">
            <i class="fas fa-bell me-1"></i> Set Alert
          </button>
        </div>
      </div>
    </div>
    
    <!-- Quick Filters -->
    <div class="card shadow-sm">
      <div class="card-header bg-light">
        <h6 class="mb-0">Quick Filters</h6>
      </div>
      <div class="card-body p-3">
        <div class="form-check form-switch mb-2" v-for="filter in quickFilters" :key="filter.id">
          <input 
            class="form-check-input" 
            type="checkbox" 
            :id="filter.id"
            v-model="filter.active"
          >
          <label class="form-check-label small" :for="filter.id">
            {{ filter.label }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'MarketBetaSidebar',
  props: {
    modelValue: {
      type: Object,
      required: true
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const selectedMarket = ref('sp500');
    const selectedTimePeriod = ref('1y');
    
    const availableMarkets = [
      { id: 'sp500', name: 'S&P 500' },
      { id: 'nasdaq', name: 'NASDAQ' },
      { id: 'hsi', name: 'Hang Seng' },
      { id: 'csi300', name: 'CSI 300' },
      { id: 'eurostoxx', name: 'Euro Stoxx 50' },
      { id: 'nikkei', name: 'Nikkei 225' },
    ];
    
    const timePeriods = [
      { label: '1M', value: '1m' },
      { label: '3M', value: '3m' },
      { label: '6M', value: '6m' },
      { label: 'YTD', value: 'ytd' },
      { label: '1Y', value: '1y' },
      { label: '5Y', value: '5y' },
      { label: 'Max', value: 'max' },
    ];
    
    const valuationMetrics = ref({
      'Current PE': 22.5,
      'Historical Avg': 18.7,
      'Percentile': 78,
      'Dividend Yield': '1.8%',
      'Earnings Yield': '4.5%',
    });
    
    const quickFilters = ref([
      { id: 'filter-overvalued', label: 'Show Overvalued', active: false },
      { id: 'filter-undervalued', label: 'Show Undervalued', active: false },
      { id: 'filter-dividend', label: 'High Dividend', active: false },
      { id: 'filter-volatile', label: 'High Volatility', active: false },
    ]);
    
    const selectTimePeriod = (period: string) => {
      selectedTimePeriod.value = period;
      updateParent();
    };
    
    const getMetricClass = (metric: string, value: any) => {
      if (metric === 'Percentile' && typeof value === 'number') {
        if (value >= 80) return 'text-danger';
        if (value >= 60) return 'text-warning';
        return 'text-success';
      }
      return '';
    };
    
    const formatValue = (metric: string, value: any) => {
      if (metric === 'Percentile') return `${value}%`;
      return value;
    };
    
    const updateParent = () => {
      emit('update:modelValue', {
        market: selectedMarket.value,
        timePeriod: selectedTimePeriod.value,
        filters: quickFilters.value.filter(f => f.active).map(f => f.id)
      });
    };
    
    // Watch for changes and update parent
    watch([selectedMarket, quickFilters], () => {
      updateParent();
    }, { deep: true });
    
    return {
      selectedMarket,
      selectedTimePeriod,
      availableMarkets,
      timePeriods,
      valuationMetrics,
      quickFilters,
      selectTimePeriod,
      getMetricClass,
      formatValue
    };
  }
});
</script>

<style scoped>
.market-beta-sidebar {
  position: sticky;
  top: 1rem;
  height: calc(100vh - 2rem);
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar */
.market-beta-sidebar::-webkit-scrollbar {
  width: 4px;
}

.market-beta-sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.market-beta-sidebar::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.market-beta-sidebar::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Form controls */
.form-select-sm, .btn-sm {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

/* Card styling */
.card {
  border: none;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.card-header {
  border-bottom: 1px solid rgba(0,0,0,0.05);
  font-weight: 600;
}

/* Button group */
.btn-group .btn {
  font-size: 0.7rem;
  padding: 0.2rem 0.4rem;
}

/* Form switch */
.form-switch .form-check-input {
  width: 2em;
  margin-left: -2.5em;
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.form-switch .form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>
