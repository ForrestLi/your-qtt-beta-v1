<template>
  <div class="market-beta">
    <div class="container-fluid">
      <div class="row gx-3">
        <!-- Sidebar Column -->
        <div class="col-lg-3 col-xl-2 d-none d-lg-block">
          <MarketBetaSidebar v-model="filters" @update:filters="handleFiltersUpdate" />
        </div>
        
        <!-- Main Content Column -->
        <div class="col-lg-9 col-xl-10">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="display-6 mb-4">Market Beta Dashboard</h1>
          <p class="lead">Real-time market valuations and risk metrics</p>
        </div>
      </div>

      <!-- Market Overview -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Global Market Overview</h5>
            </div>
            <div class="card-body">
              <!-- Loading State -->
              <div v-if="loading && markets.length === 0" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading market data...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ error }}
                <button @click="initializeMarkets" class="btn btn-sm btn-outline-danger ms-3">
                  Retry
                </button>
              </div>

              <!-- Market Overview -->
              <div v-else class="row mb-4">
                <div v-for="market in markets" :key="market.id" class="col-6 col-sm-4 col-md-4 col-lg-4 col-xl-2">
                  <div class="market-card p-3 border rounded" :class="{ 'opacity-75': loading }">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                      <h6 class="mb-0 fw-bold">{{ market.name }}</h6>
                      <span class="small text-muted">
                        <i class="far fa-clock me-1"></i>
                        {{ formatTimeAgo(market.lastUpdated) }}
                      </span>
                    </div>
                    <div class="d-flex justify-content-between align-items-baseline mb-2">
                      <span class="h4 mb-0">{{ market.value }}</span>
                      <span :class="['change fw-bold', market.change >= 0 ? 'text-success' : 'text-danger']">
                        <i :class="market.change >= 0 ? 'fas fa-caret-up' : 'fas fa-caret-down'" class="me-1"></i>
                        {{ Math.abs(market.change) }}%
                      </span>
                    </div>
                    <div class="market-metrics mt-2">
                      <div class="d-flex justify-content-between small py-1 border-bottom">
                        <span class="text-muted">P/E:</span>
                        <span>
                          {{ market.pe }}x 
                          <span :class="getPercentileClass(market.pePercentile)">
                            ({{ market.pePercentile }}%)
                          </span>
                        </span>
                      </div>
                      <div class="d-flex justify-content-between small py-1 border-bottom">
                        <span class="text-muted">P/B:</span>
                        <span>
                          {{ market.pb }}x 
                          <span :class="getPercentileClass(market.pbPercentile)">
                            ({{ market.pbPercentile }}%)
                          </span>
                        </span>
                      </div>
                      <div class="d-flex justify-content-between small py-1">
                        <span class="text-muted">Div Yield:</span>
                        <span class="text-success">{{ market.dividendYield }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Beta Analyzer Row -->
      <div class="row mb-4">
        <div class="col-12">
          <BetaAnalyzer />
        </div>
      </div>

      <!-- Market Analysis Row -->
      <div v-if="!loading && !error" class="row mb-4">
        <!-- PE Ratio Analysis -->
        <div class="col-lg-8 mb-4 mb-lg-0">
          <div class="card shadow-sm h-100">
            <div class="card-header">
              <h5 class="mb-0">PE Ratio Analysis</h5>
            </div>
            <div class="card-body">
              <div class="chart-container" style="position: relative; height: 300px;">
                <canvas ref="peChart"></canvas>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Return Projections -->
        <div class="col-lg-4">
          <ReturnProjections 
            :market-data="currentMarketData" 
            :time-period="filters.timePeriod"
            :loading="loading"
            :error="error"
          />
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-header">
              <h5 class="mb-0">Valuation Percentiles</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Timeframe</th>
                      <th class="text-end">Percentile</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(value, timeframe) in valuationPercentiles" :key="timeframe">
                      <td>{{ formatTimeframe(timeframe) }}</td>
                      <td class="text-end">
                        <span :class="getPercentileClass(value)">
                          {{ value }}%
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Market News -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header">
              <h5 class="mb-0">Market News</h5>
            </div>
            <div class="card-body">
              <div class="list-group list-group-flush">
                <a 
                  v-for="(news, index) in marketNews" 
                  :key="index"
                  href="#" 
                  class="list-group-item list-group-item-action"
                >
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ news.title }}</h6>
                    <small class="text-muted">{{ news.time }}</small>
                  </div>
                  <p class="mb-1">{{ news.summary }}</p>
                  <small class="text-muted">{{ news.source }}</small>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
        </div> <!-- End Main Content Column -->
      </div> <!-- End Row -->
    </div> <!-- End Container -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, reactive, computed, watch } from 'vue';
import Chart from 'chart.js/auto';
import BetaAnalyzer from '@/components/BetaAnalyzer.vue';
import MarketBetaSidebar from '@/components/MarketBetaSidebar.vue';
import ReturnProjections from '@/components/ReturnProjections.vue';
import { marketDataService, type MarketData } from '@/services/marketDataService';

export default defineComponent({
  name: 'MarketBeta',
  components: {
    MarketBetaSidebar,
    BetaAnalyzer,
    ReturnProjections
  },
  setup() {
    console.log('MarketBeta: Setup started');
    const peChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;
    
    const filters = reactive({
      market: 'sp500',
      timePeriod: '5y',
      activeFilters: [] as string[]
    });
    
    const loading = ref(false);
    const error = ref<string | null>(null);
    
    const markets = ref<MarketData[]>([
      { id: 'sp500', name: 'S&P 500', currentValue: 4567.89, change: 0.45, pe: 22.5, pb: 4.2, dividendYield: 1.3, pePercentile: 85, pbPercentile: 82, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'nasdaq', name: 'NASDAQ', currentValue: 14253.27, change: 0.78, pe: 28.7, pb: 5.1, dividendYield: 0.7, pePercentile: 88, pbPercentile: 85, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'hsi', name: 'Hang Seng', currentValue: 19213.49, change: -0.32, pe: 9.8, pb: 0.9, dividendYield: 3.8, pePercentile: 45, pbPercentile: 38, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'csi300', name: 'CSI 300', currentValue: 3982.76, change: 0.65, pe: 13.8, pb: 1.6, dividendYield: 2.5, pePercentile: 55, pbPercentile: 48, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'nifty50', name: 'NIFTY 50', currentValue: 19872.35, change: 0.92, pe: 22.8, pb: 3.8, dividendYield: 1.2, pePercentile: 82, pbPercentile: 78, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'sensex', name: 'SENSEX', currentValue: 66266.82, change: 0.85, pe: 23.1, pb: 3.6, dividendYield: 1.3, pePercentile: 84, pbPercentile: 76, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'stoxx50', name: 'Euro Stoxx 50', currentValue: 4231.76, change: 0.32, pe: 15.3, pb: 1.8, dividendYield: 3.2, pePercentile: 62, pbPercentile: 58, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'nikkei', name: 'Nikkei 225', currentValue: 32896.03, change: 0.54, pe: 16.7, pb: 1.5, dividendYield: 1.9, pePercentile: 68, pbPercentile: 52, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'straits', name: 'STI', currentValue: 3218.45, change: 0.21, pe: 11.5, pb: 1.1, dividendYield: 4.1, pePercentile: 48, pbPercentile: 42, lastUpdated: new Date().toISOString(), historicalPE: [] },
      { id: 'asx200', name: 'ASX 200', currentValue: 7356.28, change: 0.38, pe: 17.3, pb: 2.3, dividendYield: 4.3, pePercentile: 65, pbPercentile: 60, lastUpdated: new Date().toISOString(), historicalPE: [] }
    ]);
    
    const marketNews = ref([
      { id: 1, title: 'Fed signals potential rate cuts in Q2 2024', source: 'Bloomberg', time: '2 hours ago' },
      { id: 2, title: 'Tech stocks rally on strong earnings', source: 'CNBC', time: '5 hours ago' },
      { id: 3, title: 'Inflation cools more than expected in January', source: 'WSJ', time: '1 day ago' },
      { id: 4, title: 'Global markets mixed as investors weigh economic data', source: 'Reuters', time: '2 days ago' }
    ]);
    
    // Generate historical data for the chart
    const generateHistoricalData = () => {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      const baseValue = 15 + Math.random() * 5;
      return months.map((month, index) => ({
        date: `${month} 2023`,
        value: baseValue + Math.sin(index) * 2 + Math.random()
      }));
    };
    
    const updateChartForTimePeriod = (timePeriod: string) => {
      if (!chartInstance) return;
      
      // Generate appropriate data based on the selected time period
      const getDataPoints = (period: string) => {
        const basePoints = {
          '3y': 7,
          '5y': 12,
          '10y': 24,
          '20y': 36,
          'all': 60
        };
        
        const points = basePoints[period] || 12;
        const result = [];
        let value = 15 + Math.random() * 5;
        
        for (let i = 0; i < points; i++) {
          value = value * (1 + (Math.random() * 0.1 - 0.05));
          result.push(Number(value.toFixed(2)));
        }
        
        return result;
      };
      
      const data = getDataPoints(timePeriod);
      
      // Update chart data
      chartInstance.data.datasets[0].data = data;
      chartInstance.data.labels = data.map((_, i) => {
        const date = new Date();
        date.setMonth(date.getMonth() - (data.length - i - 1));
        return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
      });
      
      // Update chart title based on selected market
      const currentMarket = markets.value.find(m => m.id === filters.market);
      if (currentMarket) {
        chartInstance.data.datasets[0].label = `${currentMarket.name} PE Ratio`;
      }
      
      chartInstance.update();
    };
    
    const handleFiltersUpdate = (newFilters: any) => {
      console.log('Filters updated:', newFilters);
      
      // Update the filters
      filters.market = newFilters.market;
      filters.timePeriod = newFilters.timePeriod;
      filters.activeFilters = newFilters.activeFilters || [];
      
      // Update the chart with new time period data
      updateChartForTimePeriod(newFilters.timePeriod);
      
      // Fetch new market data if needed
      fetchMarketData(newFilters.market, newFilters.timePeriod);
    };
    
    const fetchMarketData = async (marketId: string, timePeriod: string) => {
      loading.value = true;
      error.value = null;
      
      try {
        // Fetch market data from the service
        const data = await marketDataService.getMarketData({
          marketId,
          timePeriod
        });
        
        // Update markets array
        const marketIndex = markets.value.findIndex(m => m.id === marketId);
        if (marketIndex !== -1) {
          markets.value[marketIndex] = data;
        } else {
          markets.value.push(data);
        }
        
        // Update chart with historical data
        updateChartWithData(data.historicalPE);
        
      } catch (err) {
        console.error('Error fetching market data:', err);
        error.value = 'Failed to load market data. Please try again later.';
      } finally {
        loading.value = false;
      }
    };
    
    const updateChartWithData = (historicalData: { date: string; value: number }[]) => {
      if (!chartInstance) return;
      
      // Update chart data
      chartInstance.data.labels = historicalData.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
      });
      
      chartInstance.data.datasets[0].data = historicalData.map(item => item.value);
      chartInstance.update();
    };

    // Market news, loading, and error are already declared above
    
    // Format market data for display
    const formattedMarkets = computed(() => {
      return markets.value.map(market => ({
        id: market.id,
        name: market.name,
        value: market.currentValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        change: market.change,
        pe: market.pe,
        pb: market.pb,
        dividendYield: market.dividendYield,
        pePercentile: market.pePercentile,
        pbPercentile: market.pbPercentile,
        lastUpdated: market.lastUpdated
      }));
    });
    
    // Get valuation percentiles for the table
    const valuationPercentiles = computed(() => {
      return markets.value.map(market => ({
        name: market.name,
        pe: market.pe,
        pb: market.pb,
        dividendYield: market.dividendYield,
        pePercentile: market.pePercentile,
        pbPercentile: market.pbPercentile,
        lastUpdated: market.lastUpdated
      }));
    });
    
    // Get current market data for the selected market
    const currentMarketData = computed(() => {
      return markets.value.find(market => market.id === filters.market) || markets.value[0];
    });

    const formatTimeframe = (timeframe: string): string => {
      const map: Record<string, string> = {
        '3y': '3 Years',
        '5y': '5 Years',
        '10y': '10 Years',
        '20y': '20 Years',
        allTime: 'All Time',
      };
      return map[timeframe] || timeframe;
    };

    const formatTimeAgo = (dateString: string): string => {
      const date = new Date(dateString);
      const now = new Date();
      const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
      
      if (diffInSeconds < 60) return 'Just now';
      if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
      if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    };

    const getPercentileClass = (value: number): string => {
      if (value >= 80) return 'text-danger';
      if (value >= 60) return 'text-warning';
      return 'text-success';
    };

    const initChart = () => {
      if (!peChart.value) return;

      const ctx = peChart.value.getContext('2d');
      if (!ctx) return;
      
      // Generate initial data
      const initialData = Array(12).fill(0).map((_, i) => {
        const date = new Date();
        date.setMonth(date.getMonth() - (11 - i));
        return {
          date: date.toISOString(),
          value: 15 + Math.sin(i) * 2 + Math.random()
        };
      });

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: initialData.map(item => 
            new Date(item.date).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
          ),
          datasets: [
            {
              label: 'S&P 500 PE Ratio',
              data: initialData.map(item => item.value),
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true,
              pointBackgroundColor: 'white',
              pointBorderColor: 'rgb(75, 192, 192)',
              pointHoverRadius: 5,
              pointHoverBackgroundColor: 'white',
              pointHoverBorderColor: 'rgb(75, 192, 192)',
              pointHoverBorderWidth: 2,
              pointHitRadius: 10,
              pointBorderWidth: 2
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            intersect: false,
            mode: 'index',
          },
          plugins: {
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleFont: { size: 14, weight: 'bold' },
              bodyFont: { size: 13 },
              padding: 12,
              displayColors: false,
              callbacks: {
                label: (context: any) => {
                  return `PE: ${context.parsed.y.toFixed(2)}`;
                }
              }
            },
            legend: {
              position: 'top',
              labels: {
                font: {
                  size: 14
                },
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle'
              }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            },
            x: {
              grid: {
                display: false
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            }
          }
        }
      });
    };
    
    // Initialize the component
    onMounted(() => {
      initChart();
      
      // Set up auto-refresh every 5 minutes
      const refreshInterval = setInterval(() => {
        console.log('Refreshing market data...');
      }, 5 * 60 * 1000);
      
      // Clean up interval on component unmount
      onBeforeUnmount(() => {
        clearInterval(refreshInterval);
        if (chartInstance) {
          chartInstance.destroy();
        }
      });
    });
    
    // Watch for market changes
    watch(() => filters.market, (newMarketId) => {
      if (chartInstance) {
        const market = markets.value.find(m => m.id === newMarketId);
        if (market) {
          chartInstance.data.datasets[0].label = `${market.name} PE Ratio`;
          chartInstance.update();
        }
      }
      updateChartForTimePeriod(filters.timePeriod);
    });
    
    // Watch for time period changes
    watch(() => filters.timePeriod, (newTimePeriod) => {
      updateChartForTimePeriod(newTimePeriod);
    });

    return {
      peChart,
      markets: formattedMarkets,
      valuationPercentiles,
      marketNews,
      filters,
      formatTimeframe,
      formatTimeAgo,
      getPercentileClass,
      handleFiltersUpdate,
      currentMarketData,
      loading,
      error
    };
  },
});
</script>

<style scoped>
.market-beta {
  padding: 1rem 0;
  min-height: calc(100vh - 56px);
  background-color: #f8f9fa;
}

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .market-beta {
    padding: 0.5rem;
  }
}

/* Card styling */
.card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  font-weight: 600;
  padding: 0.75rem 1.25rem;
}

/* Chart container */
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

/* Market cards */
.market-card {
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: #fff;
  display: flex;
  flex-direction: column;
}

.market-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
  border-color: rgba(13, 110, 253, 0.2);
}

.change-indicator {
  font-weight: 600;
}

.valuation-table th {
  font-weight: 500;
  color: #6c757d;
}

.news-item {
  transition: all 0.2s ease;
}

.news-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.percentile-0-20 {
  background-color: #d4edda;
  color: #155724;
}

.percentile-21-40 {
  background-color: #c3e6cb;
  color: #155724;
}

.percentile-41-60 {
  background-color: #f8f9fa;
  color: #212529;
}

.percentile-61-80 {
  background-color: #ffeeba;
  color: #856404;
}

.percentile-81-100 {
  background-color: #f8d7da;
  color: #721c24;
}

/* Loading and Error States */
.loading-placeholder {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
  height: 1.5rem;
  opacity: 0.7;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.market-card .text-success {
  color: #198754 !important;
}

.market-card .text-danger {
  color: #dc3545 !important;
}

.opacity-75 {
  opacity: 0.75;
  transition: opacity 0.3s ease;
}

/* Fade transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Alert close button */
.btn-close {
  padding: 0.5rem;
  margin: -0.5rem -0.5rem -0.5rem auto;
}

/* Spinner animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinner-border {
  display: inline-block;
  width: 1.5rem;
  height: 1.5rem;
  vertical-align: -0.125em;
  border: 0.25em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .market-card {
    margin-bottom: 1rem;
  }
  
  .spinner-border {
    width: 1.25rem;
    height: 1.25rem;
    border-width: 0.2em;
  }
}

.market-card .text-warning {
  color: #fd7e14 !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  color: #2c3e50;
  font-weight: 600;
}

/* Change indicators */
.change {
  font-weight: 600;
  font-size: 0.9em;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.text-warning {
  color: #fd7e14 !important;
}

/* Table styles */
.table {
  font-size: 0.9rem;
}

.table th {
  font-weight: 600;
  color: #495057;
  background-color: #f8f9fa;
  border-top: none;
  border-bottom: 1px solid #e9ecef;
  padding: 0.75rem 1rem;
}

.table td {
  padding: 0.75rem 1rem;
  vertical-align: middle;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .market-card {
    margin-bottom: 1rem;
  }
  
  .chart-container {
    height: 250px;
  }
}

/* Animation for loading */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.market-beta > .container-fluid > .row > div {
  animation: fadeIn 0.3s ease-out forwards;
}

.card-header {
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.list-group-item {
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}
</style>
