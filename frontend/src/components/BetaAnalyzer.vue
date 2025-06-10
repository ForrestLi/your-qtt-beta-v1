<template>
  <div class="card shadow-sm h-100" id="beta-analyzer-card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Instrument Beta Analyzer</h5>
      <button 
        class="btn btn-sm btn-outline-secondary" 
        @click="isExpanded = !isExpanded"
        :aria-expanded="isExpanded"
        aria-controls="betaAnalyzerCollapse"
      >
        <i :class="isExpanded ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
      </button>
    </div>
    
    <div class="card-body">
      <div class="row g-3">
        <div class="col-md-5">
          <label for="tickerInput" class="form-label">Stock Ticker</label>
          <div class="input-group">
            <input 
              type="text" 
              class="form-control" 
              id="tickerInput"
              v-model="ticker"
              placeholder="e.g., AAPL, MSFT"
              :disabled="isLoading"
            >
            <button 
              class="btn btn-outline-secondary" 
              type="button"
              @click="searchTicker"
              :disabled="!ticker || isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status"></span>
              <i class="bi-search"></i>
            </button>
          </div>
        </div>
        
        <div class="col-md-5">
          <label for="marketIndex" class="form-label">Market Index</label>
          <select 
            class="form-select" 
            id="marketIndex"
            v-model="selectedIndex"
            :disabled="isLoading"
          >
            <option v-for="index in marketIndices" :key="index.id" :value="index.id">
              {{ index.name }} ({{ index.id }})
            </option>
          </select>
        </div>
        
        <div class="col-md-2 d-flex align-items-end">
          <button 
            class="btn btn-primary w-100"
            @click="calculateBeta"
            :disabled="!ticker || !selectedIndex || isLoading"
          >
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status"></span>
            Calculate
          </button>
        </div>
      </div>
      
      <div v-if="error" class="alert alert-danger mt-3 mb-0">
        <i class="bi-exclamation-triangle-fill me-2"></i>
        {{ error }}
      </div>
      
      <div v-if="betaResult" class="mt-4">
        <div class="alert" :class="getBetaAlertClass">
          <h5 class="alert-heading mb-2">
            {{ ticker.toUpperCase() }} Beta vs {{ getSelectedIndexName }}
          </h5>
          <div class="d-flex align-items-center">
            <div class="display-4 fw-bold me-3">{{ betaResult.beta.toFixed(2) }}</div>
            <div>
              <div class="d-flex align-items-center mb-1">
                <span class="badge me-2" :class="getVolatilityClass">
                  {{ getVolatilityLabel }}
                </span>
                <small class="text-muted">
                  R²: {{ (betaResult.rSquared * 100).toFixed(1) }}%
                </small>
              </div>
              <div class="small text-muted">
                Based on {{ betaResult.period }} days of historical data
              </div>
            </div>
          </div>
          <hr>
          <p class="mb-0 small">
            <i class="bi-info-circle-fill me-1"></i>
            <span v-html="getBetaInterpretation"></span>
          </p>
        </div>
        
        <div class="mt-3">
          <div class="d-flex justify-content-between mb-2">
            <span class="small text-muted">Correlation:</span>
            <span class="fw-medium">{{ betaResult.correlation.toFixed(3) }}</span>
          </div>
          <div class="d-flex justify-content-between mb-2">
            <span class="small text-muted">Alpha (annualized):</span>
            <span :class="{'text-success': betaResult.alpha >= 0, 'text-danger': betaResult.alpha < 0}">
              {{ (betaResult.alpha * 100).toFixed(2) }}%
            </span>
          </div>
          <div class="d-flex justify-content-between">
            <span class="small text-muted">Last Updated:</span>
            <span class="small">{{ formatDate(betaResult.lastUpdated) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useMarketData } from '@/composables/useMarketData';

interface BetaResult {
  beta: number;
  alpha: number;
  rSquared: number;
  correlation: number;
  period: number;
  lastUpdated: string;
}

export default defineComponent({
  name: 'BetaAnalyzer',
  
  setup() {
    console.log('BetaAnalyzer: Setup started');
    const { fetchBetaAnalysis } = useMarketData();
    
    const ticker = ref('');
    const selectedIndex = ref('SP500');
    const isLoading = ref(false);
    const error = ref('');
    const betaResult = ref<BetaResult | null>(null);
    const isExpanded = ref(true);
    
    console.log('BetaAnalyzer: Refs initialized');
    
    const marketIndices = [
      { id: 'SP500', name: 'S&P 500' },
      { id: 'NDX', name: 'NASDAQ 100' },
      { id: 'HSI', name: 'Hang Seng' },
      { id: 'CSI300', name: 'CSI 300' },
      { id: 'N225', name: 'Nikkei 225' },
      { id: 'STOXX50', name: 'Euro Stoxx 50' },
    ];
    
    const getSelectedIndexName = computed(() => {
      const index = marketIndices.find(i => i.id === selectedIndex.value);
      return index ? index.name : selectedIndex.value;
    });
    
    const getBetaAlertClass = computed(() => {
      if (!betaResult.value) return '';
      const beta = betaResult.value.beta;
      if (beta < 0.8) return 'alert-info';
      if (beta >= 0.8 && beta <= 1.2) return 'alert-success';
      if (beta > 1.2 && beta <= 1.8) return 'alert-warning';
      return 'alert-danger';
    });
    
    const getVolatilityClass = computed(() => {
      if (!betaResult.value) return '';
      const beta = betaResult.value.beta;
      if (beta < 0.8) return 'bg-info';
      if (beta >= 0.8 && beta <= 1.2) return 'bg-success';
      if (beta > 1.2 && beta <= 1.8) return 'bg-warning';
      return 'bg-danger';
    });
    
    const getVolatilityLabel = computed(() => {
      if (!betaResult.value) return '';
      const beta = betaResult.value.beta;
      if (beta < 0) return 'Inverse';
      if (beta < 0.5) return 'Very Low Volatility';
      if (beta < 0.8) return 'Low Volatility';
      if (beta < 1.2) return 'Market-Like';
      if (beta < 1.5) return 'High Volatility';
      return 'Very High Volatility';
    });
    
    const getBetaInterpretation = computed(() => {
      if (!betaResult.value) return '';
      const beta = betaResult.value.beta;
      
      if (beta < 0) {
        return `This stock tends to move in the opposite direction of the ${getSelectedIndexName.value}. ` +
               `A 1% move in the index typically results in a ${Math.abs(beta).toFixed(2)}% move in the opposite direction.`;
      } else if (beta < 0.5) {
        return `This stock is less volatile than the ${getSelectedIndexName.value}. ` +
               `A 1% move in the index typically results in a ${beta.toFixed(2)}% move in the stock.`;
      } else if (beta < 1.2) {
        return `This stock has similar volatility to the ${getSelectedIndexName.value}. ` +
               `A 1% move in the index typically results in a ${beta.toFixed(2)}% move in the stock.`;
      } else {
        return `This stock is more volatile than the ${getSelectedIndexName.value}. ` +
               `A 1% move in the index typically results in a ${beta.toFixed(2)}% move in the stock.`;
      }
    });
    
    const searchTicker = async () => {
      if (!ticker.value.trim()) return;
      await calculateBeta();
    };
    
    const calculateBeta = async () => {
      if (!ticker.value.trim() || !selectedIndex.value) return;
      
      isLoading.value = true;
      error.value = '';
      
      try {
        const result = await fetchBetaAnalysis({
          ticker: ticker.value,
          index: selectedIndex.value,
          period: 252 // 1 year of trading days
        });
        
        betaResult.value = {
          beta: result.beta,
          alpha: result.alpha,
          rSquared: result.rSquared,
          correlation: result.correlation,
          period: result.period,
          lastUpdated: result.lastUpdated
        };
      } catch (err) {
        console.error('Error calculating beta:', err);
        error.value = 'Failed to calculate beta. Please try again later.';
      } finally {
        isLoading.value = false;
      }
    };
    
    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    return {
      ticker,
      selectedIndex,
      marketIndices,
      isLoading,
      error,
      betaResult,
      isExpanded,
      getSelectedIndexName,
      getBetaAlertClass,
      getVolatilityClass,
      getVolatilityLabel,
      getBetaInterpretation,
      searchTicker,
      calculateBeta,
      formatDate,
    };
  },
});
</script>

<style scoped>
.beta-value {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.volatility-badge {
  font-size: 0.8em;
  padding: 0.35em 0.65em;
}

.alert h5 {
  font-weight: 600;
  font-size: 1.1em;
}

.alert p:last-child {
  margin-bottom: 0;
}

.form-label {
  font-weight: 500;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.input-group-text {
  background-color: #f8f9fa;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-header h5 {
  font-weight: 600;
  color: #2c3e50;
}

.btn-outline-secondary {
  border-color: #dee2e6;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .beta-value {
    font-size: 2rem;
  }
  
  .display-4 {
    font-size: 2.5rem;
  }
}
</style>
