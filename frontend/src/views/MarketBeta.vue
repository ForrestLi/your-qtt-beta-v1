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
              <div class="row g-3">
                <div v-for="market in markets" :key="market.id" class="col-md-4 col-lg-2">
                  <div class="market-card p-3 border rounded text-center">
                    <h6 class="mb-2">{{ market.name }}</h6>
                    <div class="h4 mb-1">{{ market.value }}</div>
                    <div :class="['change', market.change >= 0 ? 'text-success' : 'text-danger']">
                      <i :class="market.change >= 0 ? 'fas fa-caret-up' : 'fas fa-caret-down'" class="me-1"></i>
                      {{ market.change }}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- PE Ratio Analysis -->
      <div class="row mb-4">
        <div class="col-md-8">
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
import { defineComponent, ref, onMounted, onBeforeUnmount, reactive } from 'vue';
import Chart from 'chart.js/auto';
import MarketBetaSidebar from '@/components/MarketBetaSidebar.vue';

export default defineComponent({
  name: 'MarketBeta',
  components: {
    MarketBetaSidebar
  },
  setup() {
    const peChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;
    
    const filters = reactive({
      market: 'sp500',
      timePeriod: '1y',
      activeFilters: [] as string[]
    });
    
    const handleFiltersUpdate = (newFilters: any) => {
      // Handle filter updates from the sidebar
      console.log('Filters updated:', newFilters);
      // Here you would typically fetch new data based on the filters
      fetchMarketData(newFilters.market, newFilters.timePeriod);
    };
    
    const fetchMarketData = async (marketId: string, timePeriod: string) => {
      // Simulate API call
      console.log(`Fetching data for ${marketId} with time period ${timePeriod}`);
      // In a real app, you would make an API call here
      // const response = await fetch(`/api/market-data/${marketId}?period=${timePeriod}`);
      // const data = await response.json();
      // update charts and data with the new data
    };

    const markets = ref([
      { id: 'sp500', name: 'S&P 500', value: '4,567.89', change: 0.45 },
      { id: 'nasdaq', name: 'NASDAQ', value: '14,567.34', change: -0.23 },
      { id: 'hsi', name: 'Hang Seng', value: '18,234.56', change: 1.23 },
      { id: 'csi300', name: 'CSI 300', value: '3,456.78', change: 0.78 },
      { id: 'eurostoxx', name: 'Euro Stoxx', value: '4,321.09', change: -0.56 },
      { id: 'nikkei', name: 'Nikkei 225', value: '32,456.78', change: 0.34 },
    ]);

    const valuationPercentiles = ref({
      '3y': 78,
      '5y': 82,
      '10y': 75,
      '20y': 68,
      allTime: 72,
    });

    const marketNews = ref([
      {
        title: 'Global Markets Rally on Positive Economic Data',
        summary: 'Markets worldwide showed strong gains as economic indicators surpassed expectations.',
        source: 'Financial Times',
        time: '2 hours ago',
      },
      {
        title: 'Tech Stocks Lead Market Recovery',
        summary: 'Major tech companies report better than expected earnings, boosting market sentiment.',
        source: 'Bloomberg',
        time: '5 hours ago',
      },
      {
        title: 'Central Banks Signal Rate Stability',
        summary: 'Federal Reserve and ECB suggest rates may have peaked, easing investor concerns.',
        source: 'Reuters',
        time: '1 day ago',
      },
    ]);

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

    const getPercentileClass = (value: number): string => {
      if (value >= 80) return 'text-danger';
      if (value >= 60) return 'text-warning';
      return 'text-success';
    };

    const initChart = () => {
      if (!peChart.value) return;

      const ctx = peChart.value.getContext('2d');
      if (!ctx) return;

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
          datasets: [
            {
              label: 'S&P 500 PE Ratio',
              data: [18.5, 18.8, 19.2, 19.5, 20.1, 19.8, 20.5],
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.3,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              mode: 'index',
              intersect: false,
            },
          },
          scales: {
            y: {
              beginAtZero: false,
            },
          },
        },
      });
    };


    onMounted(() => {
      initChart();
      // Fetch initial data
      fetchMarketData(filters.market, filters.timePeriod);
    });

    onBeforeUnmount(() => {
      if (chartInstance) {
        chartInstance.destroy();
      }
    });

    return {
      peChart,
      markets,
      valuationPercentiles,
      marketNews,
      filters,
      formatTimeframe,
      getPercentileClass,
      handleFiltersUpdate
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
  transition: all 0.2s ease;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: #fff;
}

.market-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
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
