<template>
  <div class="stock-alpha">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h1 class="display-6 mb-4">Stock Alpha Analyzer</h1>
          <p class="lead">Fundamental analysis and risk assessment for individual stocks</p>
        </div>
      </div>

      <!-- Stock Search -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="row g-3 align-items-center">
                <div class="col-md-8">
                  <label for="tickerInput" class="form-label">Search for a stock</label>
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control form-control-lg"
                      id="tickerInput"
                      v-model="ticker"
                      placeholder="e.g., AAPL, MSFT, GOOGL"
                      @keyup.enter="searchStock"
                      :disabled="loading"
                    >
                    <button 
                      class="btn btn-primary" 
                      type="button"
                      @click="searchStock"
                      :disabled="!ticker || loading"
                    >
                      <span v-if="loading" class="spinner-border spinner-border-sm me-1" role="status"></span>
                      <i class="bi bi-search me-1"></i> Analyze
                    </button>
                  </div>
                </div>
                <div v-if="ticker" class="col-md-4 text-md-end">
                  <h3 class="mb-0">${{ stockData.price.toFixed(2) }}</h3>
                  <span :class="stockData.change >= 0 ? 'text-success' : 'text-danger'">
                    <i :class="stockData.change >= 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                    {{ Math.abs(stockData.change).toFixed(2) }} ({{ Math.abs(stockData.changePercent).toFixed(2) }}%)
                  </span>
                </div>
              </div>
              <div v-if="error" class="alert alert-danger mt-3 mb-0">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ error }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Stock Header -->
      <div v-if="ticker" class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h2 class="mb-1">{{ stockData.companyName }} <small class="text-muted">({{ stockData.ticker }})</small></h2>
                  <p class="text-muted mb-0">{{ stockData.description }}</p>
                </div>
                <div class="text-end">
                  <div class="badge bg-primary mb-2">
                    <i class="bi bi-shield-check me-1"></i>
                    Risk Score: {{ stockData.riskScore }}
                  </div>
                  <div class="d-flex justify-content-end">
                    <span class="badge" :class="getRiskLevelClass(stockData.riskScore)">
                      {{ getRiskLevel(stockData.riskScore) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis Results -->
      <div v-if="ticker" class="row">
        <!-- Profitability Metrics -->
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Profitability Metrics</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <!-- ROE -->
                <div class="col-md-4 mb-3" v-for="metric in [
                  { key: 'roe', label: 'Return on Equity (5Y Avg)', format: 'percent', reverse: false },
                  { key: 'roic', label: 'Return on Invested Capital', format: 'percent', reverse: false },
                  { key: 'roa', label: 'Return on Assets', format: 'percent', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Valuation Metrics -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Valuation</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 mb-3" v-for="metric in [
                  { key: 'peRatio', label: 'P/E Ratio (TTM)', format: 'multiple', reverse: true, additional: `(${stockData.metrics.pePercentile}% 5Y Percentile)` },
                  { key: 'pbRatio', label: 'Price/Book', format: 'multiple', reverse: true },
                  { key: 'fcfYield', label: 'FCF Yield', format: 'percent', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Financial Health -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Financial Health</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 mb-3" v-for="metric in [
                  { key: 'debtToEquity', label: 'Debt/Equity', format: 'multiple', reverse: true },
                  { key: 'currentRatio', label: 'Current Ratio', format: 'multiple', reverse: false },
                  { key: 'interestCoverage', label: 'Interest Coverage', format: 'multiple', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Growth Metrics -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Growth Metrics</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 mb-3" v-for="metric in [
                  { key: 'revenueGrowth', label: 'Revenue Growth (YoY)', format: 'percent', reverse: false },
                  { key: 'epsGrowth', label: 'EPS Growth (YoY)', format: 'percent', reverse: false },
                  { key: 'fcfGrowth', label: 'FCF Growth (YoY)', format: 'percent', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Capital Allocation -->
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Capital Allocation</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 mb-3" v-for="metric in [
                  { key: 'dividendYield', label: 'Dividend Yield', format: 'percent', reverse: false },
                  { key: 'shareBuybackRate', label: 'Share Buyback Rate', format: 'percent', reverse: false },
                  { key: 'insiderBuying', label: 'Net Insider Buying', format: 'percent', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Efficiency Metrics -->
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-header bg-light">
              <h5 class="mb-0">Efficiency Metrics</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-4 mb-3" v-for="metric in [
                  { key: 'assetTurnover', label: 'Asset Turnover', format: 'multiple', reverse: false },
                  { key: 'inventoryTurnover', label: 'Inventory Turnover', format: 'multiple', reverse: false },
                  { key: 'profitMargin', label: 'Net Profit Margin', format: 'percent', reverse: false }
                ]" :key="metric.key">
                  <MetricCard 
                    :metric="metric" 
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Metrics Grid -->
      <div class="row g-4 mb-4">
        <!-- Profitability Metrics -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-graph-up me-2"></i>Profitability Metrics
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-3" v-for="metric in profitabilityMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Valuation Metrics -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-cash-coin me-2"></i>Valuation Metrics
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-3" v-for="metric in valuationMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Financial Health -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-heart-pulse me-2"></i>Financial Health
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-4" v-for="metric in financialHealthMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Growth Metrics -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-graph-up-arrow me-2"></i>Growth Metrics
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-4" v-for="metric in growthMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Capital Allocation -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-piggy-bank me-2"></i>Capital Allocation
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-3" v-for="metric in capitalAllocationMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Efficiency Metrics -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-speedometer2 me-2"></i>Efficiency Metrics
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6" v-for="metric in efficiencyMetrics" :key="metric.key">
                  <MetricCard 
                    :metric="metric"
                    :value="stockData.metrics[metric.key]"
                    :industry-avg="stockData.industryAvg[metric.key]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Risk Factors -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-exclamation-triangle me-2"></i>Key Risk Factors
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6 col-lg-3" v-for="(factor, index) in stockData.riskFactors" :key="index">
                  <div class="card h-100">
                    <div class="card-body">
                      <h6 class="card-title d-flex justify-content-between align-items-center">
                        {{ factor.name }}
                        <span class="badge" :class="getRiskFactorClass(factor.impact)">
                          {{ factor.impact }}
                        </span>
                      </h6>
                      <div class="progress mt-2" style="height: 4px;">
                        <div 
                          class="progress-bar" 
                          :class="getProgressBarClass(factor.impact)"
                          role="progressbar" 
                          :style="{ width: getImpactWidth(factor.impact) + '%' }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Risk Assessment CTA -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card bg-light border-0 text-center py-4">
            <div class="card-body">
              <h4>Want a personalized risk assessment?</h4>
              <p class="text-muted mb-4">Take our AI-powered questionnaire to evaluate your risk tolerance and get personalized investment recommendations.</p>
              <button class="btn btn-primary btn-lg" @click="startQuestionnaire">
                <i class="bi bi-clipboard2-pulse me-2"></i>Start Risk Assessment
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import MetricCard from '@/components/MetricCard.vue';

export default defineComponent({
  name: 'StockAlpha',
  components: {
    MetricCard
  },
  setup() {
    const ticker = ref('AAPL');
    const loading = ref(false);
    const error = ref('');
    
    const stockData = ref({
      companyName: 'Apple Inc.',
      ticker: 'AAPL',
      price: 189.98,
      change: 2.34,
      changePercent: 1.25,
      description: 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.',
      metrics: {
        // Profitability Metrics
        roe: 22.5, // Return on Equity (5Y Avg)
        roic: 18.7, // Return on Invested Capital
        roa: 12.3, // Return on Assets
        profitMargin: 25.9, // Net Profit Margin
        
        // Valuation Metrics
        peRatio: 28.7, // P/E Ratio (TTM)
        pePercentile: 85, // PE Percentile (5Y)
        pbRatio: 12.5, // Price-to-Book Ratio
        fcfYield: 4.2, // Free Cash Flow Yield
        
        // Financial Health
        debtToEquity: 0.8, // Debt to Equity Ratio
        currentRatio: 1.5, // Current Assets / Current Liabilities
        interestCoverage: 12.4, // EBIT / Interest Expense
        
        // Growth Metrics
        revenueGrowth: 8.1, // Revenue Growth (YoY)
        epsGrowth: 10.2, // EPS Growth (YoY)
        fcfGrowth: 7.5, // Free Cash Flow Growth (YoY)
        
        // Capital Allocation
        dividendYield: 1.8, // Dividend Yield
        dividendPayoutRatio: 32.5, // % of Earnings Paid as Dividends
        shareBuybackRate: 2.1, // % of Shares Repurchased (Annual)
        insiderBuying: 1.2, // Net Insider Buying as % of Float
        
        // Efficiency
        assetTurnover: 0.85, // Revenue / Total Assets
        inventoryTurnover: 8.2, // COGS / Average Inventory
      },
      industryAvg: {
        roe: 15.2,
        roic: 12.1,
        roa: 8.7,
        profitMargin: 18.7,
        peRatio: 22.4,
        pbRatio: 3.8,
        fcfYield: 3.8,
        debtToEquity: 1.2,
        currentRatio: 1.8,
        interestCoverage: 9.8,
        revenueGrowth: 5.4,
        epsGrowth: 6.8,
        fcfGrowth: 4.2,
        dividendYield: 2.1,
        dividendPayoutRatio: 45.3,
        shareBuybackRate: 1.2,
        insiderBuying: 0.8,
        assetTurnover: 0.72,
        inventoryTurnover: 6.5
      },
      riskScore: 72, // 0-100 scale
      riskFactors: [
        { name: 'Valuation Risk', impact: 'High' },
        { name: 'Competition', impact: 'Medium' },
        { name: 'Regulatory', impact: 'Low' },
        { name: 'Management', impact: 'Low' },
      ]
    });

    const searchStock = () => {
      if (!ticker.value.trim()) {
        error.value = 'Please enter a stock ticker';
        return;
      }
      
      loading.value = true;
      error.value = '';
      
      // In a real app, you would fetch data from an API here
      // For now, we'll just simulate a delay
      setTimeout(() => {
        loading.value = false;
      }, 1000);
    };

    const profitabilityMetrics = [
      { key: 'roe', label: 'Return on Equity (5Y Avg)', format: 'percent', reverse: false },
      { key: 'roic', label: 'Return on Invested Capital', format: 'percent', reverse: false },
      { key: 'roa', label: 'Return on Assets', format: 'percent', reverse: false },
      { key: 'profitMargin', label: 'Net Profit Margin', format: 'percent', reverse: false }
    ];

    const valuationMetrics = [
      { key: 'peRatio', label: 'P/E Ratio (TTM)', format: 'multiple', reverse: true },
      { key: 'pbRatio', label: 'Price-to-Book Ratio', format: 'multiple', reverse: true },
      { key: 'fcfYield', label: 'Free Cash Flow Yield', format: 'percent', reverse: false },
      { key: 'pePercentile', label: 'PE Percentile (5Y)', format: 'percent', reverse: true }
    ];

    const financialHealthMetrics = [
      { key: 'debtToEquity', label: 'Debt to Equity', format: 'multiple', reverse: true },
      { key: 'currentRatio', label: 'Current Ratio', format: 'multiple', reverse: false },
      { key: 'interestCoverage', label: 'Interest Coverage', format: 'multiple', reverse: false }
    ];

    const growthMetrics = [
      { key: 'revenueGrowth', label: 'Revenue Growth (YoY)', format: 'percent', reverse: false },
      { key: 'epsGrowth', label: 'EPS Growth (YoY)', format: 'percent', reverse: false },
      { key: 'fcfGrowth', label: 'FCF Growth (YoY)', format: 'percent', reverse: false }
    ];

    const capitalAllocationMetrics = [
      { key: 'dividendYield', label: 'Dividend Yield', format: 'percent', reverse: false },
      { key: 'dividendPayoutRatio', label: 'Dividend Payout Ratio', format: 'percent', reverse: true },
      { key: 'shareBuybackRate', label: 'Share Buyback Rate', format: 'percent', reverse: false },
      { key: 'insiderBuying', label: 'Net Insider Buying', format: 'percent', reverse: false, additional: 'of float' }
    ];
    
    const efficiencyMetrics = [
      { key: 'assetTurnover', label: 'Asset Turnover', format: 'multiple', reverse: false },
      { key: 'inventoryTurnover', label: 'Inventory Turnover', format: 'multiple', reverse: false }
    ];

    const getMetricClass = (metric: string, value: number, inverse = false) => {
      if (inverse) {
        // For metrics where lower is better (e.g., debt-to-equity)
        if (value < 0.5) return 'bg-success';
        if (value < 1) return 'bg-warning';
        return 'bg-danger';
      } else {
        // For metrics where higher is better (e.g., ROE, profit margin)
        if (value > 20) return 'bg-success';
        if (value > 10) return 'bg-warning';
        return 'bg-danger';
      }
    };

    const getMetricLabel = (metric: string, value: number, inverse = false) => {
      if (inverse) {
        if (value < 0.5) return 'Low';
        if (value < 1) return 'Medium';
        return 'High';
      } else {
        if (value > 20) return 'Strong';
        if (value > 10) return 'Moderate';
        return 'Weak';
      }
    };

    const getPercentileClass = (percentile: number) => {
      if (percentile > 80) return 'bg-danger';
      if (percentile > 60) return 'bg-warning';
      return 'bg-success';
    };

    const getRiskScoreColor = (score: number) => {
      if (score < 30) return '#28a745'; // Green for low risk
      if (score < 70) return '#ffc107'; // Yellow for medium risk
      return '#dc3545'; // Red for high risk
    };

    const getRiskLevel = (score: number) => {
      if (score >= 75) return 'High Risk';
      if (score >= 40) return 'Moderate Risk';
      return 'Low Risk';
    };

    const getRiskLevelClass = (score: number) => {
      if (score >= 75) return 'bg-danger';
      if (score >= 40) return 'bg-warning';
      return 'bg-success';
    };

    const getRiskFactorClass = (impact: string) => {
      switch (impact.toLowerCase()) {
        case 'high': return 'bg-danger';
        case 'medium': return 'bg-warning';
        default: return 'bg-success';
      }
    };

    const getProgressBarClass = (impact: string) => {
      switch (impact.toLowerCase()) {
        case 'high': return 'bg-danger';
        case 'medium': return 'bg-warning';
        default: return 'bg-success';
      }
    };

    const getImpactWidth = (impact: string) => {
      switch (impact.toLowerCase()) {
        case 'high': return 100;
        case 'medium': return 65;
        default: return 30;
      }
    };

    const getPbRatioClass = (pbRatio: number) => {
      if (pbRatio < 1) return 'bg-success';
      if (pbRatio < 3) return 'bg-warning';
      return 'bg-danger';
    };

    const getPbRatioLabel = (pbRatio: number) => {
      if (pbRatio < 1) return 'Undervalued';
      if (pbRatio < 3) return 'Fair Value';
      return 'Overvalued';
    };

    const startQuestionnaire = () => {
      alert('Risk assessment questionnaire would open here in a real application.');
    };

    return {
      ticker,
      loading,
      error,
      stockData,
      searchStock,
      getRiskLevel,
      getRiskLevelClass,
      getRiskFactorClass,
      getProgressBarClass,
      getImpactWidth,
      getPbRatioLabel,
      startQuestionnaire,
      // Metrics
      profitabilityMetrics,
      valuationMetrics,
      financialHealthMetrics,
      growthMetrics,
      capitalAllocationMetrics,
      efficiencyMetrics
    };
  }
});
</script>

<style scoped>
.metric-card {
  transition: all 0.2s ease;
  height: 100%;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
}

.progress-ring circle {
  transition: stroke-dashoffset 0.5s;
  transform-origin: 50% 50%;
  transform: rotate(-90deg);
}

.risk-factors .progress {
  height: 4px;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .metric-card {
    margin-bottom: 1rem;
  }
}
</style>
