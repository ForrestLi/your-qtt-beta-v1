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
            <optgroup v-for="(markets, region) in groupedMarkets" :key="region" :label="region">
              <option v-for="market in markets" :key="market.id" :value="market.id">
                {{ market.name }}
              </option>
            </optgroup>
          </select>
        </div>
        
        <!-- Time Horizon -->
        <div class="mb-3">
          <label class="form-label small text-muted mb-1">Time Horizon</label>
          <div class="d-flex flex-column gap-2">
            <button 
              v-for="period in timePeriods" 
              :key="period.value"
              @click="selectTimePeriod(period.value)"
              class="btn btn-sm text-start d-flex justify-content-between align-items-center"
              :class="[selectedTimePeriod === period.value ? 'btn-primary' : 'btn-outline-secondary']"
            >
              <span>{{ period.label }}</span>
              <small class="opacity-75 ms-2">{{ period.description }}</small>
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
import { defineComponent, ref, watch, computed } from 'vue';

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
    
    const availableMarkets = ref([
      { id: 'sp500', name: ' S&P 500', region: 'US' },
      { id: 'nasdaq', name: ' NASDAQ', region: 'US' },
      { id: 'hsi', name: ' Hang Seng', region: 'Asia' },
      { id: 'csi300', name: ' CSI 300', region: 'Asia' },
      { id: 'nifty50', name: ' NIFTY 50', region: 'Asia' },
      { id: 'sensex', name: ' SENSEX', region: 'Asia' },
      { id: 'stoxx50', name: ' Euro Stoxx 50', region: 'Europe' },
      { id: 'nikkei', name: ' Nikkei 225', region: 'Asia' },
      { id: 'straits', name: ' STI', region: 'Asia' },
      { id: 'asx200', name: ' ASX 200', region: 'Oceania' },
    ]);
    
    const groupedMarkets = computed(() => {
      const groups: Record<string, Array<{id: string; name: string; region: string}>> = {};
      availableMarkets.value.forEach(market => {
        if (!groups[market.region]) {
          groups[market.region] = [];
        }
        groups[market.region].push(market);
      });
      return groups;
    });
    
    const timePeriods = [
      { label: '3Y', value: '3y', description: '3 Years' },
      { label: '5Y', value: '5y', description: '5 Years' },
      { label: '10Y', value: '10y', description: '10 Years' },
      { label: '20Y', value: '20y', description: '20 Years' },
      { label: 'All Time', value: 'all', description: 'All Historical Data' },
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
      // Update the chart data based on the selected time period
      // This would typically involve an API call to fetch data for the selected period
      console.log(`Selected time period: ${period}`);
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

/* Time period selector */
.time-period-selector .btn {
  font-size: 0.85rem;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
  border: 1px solid #dee2e6;
}

.time-period-selector .btn:hover {
  background-color: #f8f9fa;
}

.time-period-selector .btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.time-period-selector .btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.time-period-selector .btn small {
  opacity: 0.8;
  font-weight: 400;
}

.time-period-selector .btn-primary small {
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.9) !important;
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
