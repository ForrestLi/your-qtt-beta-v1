<template>
  <div class="card shadow-sm h-100">
    <div class="card-header bg-light d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Forward-Looking Return Projections</h5>
      <div v-if="loading" class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger m-3" role="alert">
      {{ error }}
    </div>
    <div class="card-body">
      <!-- Projection Tabs -->
      <ul class="nav nav-tabs nav-fill mb-3" role="tablist">
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ 'active': activeTab === 'forecast' }"
            @click="activeTab = 'forecast'"
          >
            Statistical Forecast
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ 'active': activeTab === 'meanReversion' }"
            @click="activeTab = 'meanReversion'"
          >
            PE Mean Reversion
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            :class="{ 'active': activeTab === 'percentile' }"
            @click="activeTab = 'percentile'"
          >
            Historical Percentiles
          </button>
        </li>
      </ul>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Statistical Forecast -->
        <div v-if="activeTab === 'forecast'" class="forecast-tab">
          <div class="mb-3">
            <div class="d-flex justify-content-between mb-2">
              <span class="small text-muted">Projected 5-Year Annual Return</span>
              <span class="fw-bold" :class="getReturnClass(projections.annualReturn)">
                {{ projections.annualReturn > 0 ? '+' : '' }}{{ projections.annualReturn }}%
              </span>
            </div>
            <div class="progress" style="height: 8px;">
              <div 
                class="progress-bar" 
                :class="getReturnClass(projections.annualReturn, true)"
                role="progressbar" 
                :style="{ width: Math.min(Math.abs(projections.annualReturn) * 2, 100) + '%' }"
                :aria-valuenow="projections.annualReturn" 
                aria-valuemin="-50" 
                aria-valuemax="50"
              ></div>
            </div>
            <div class="d-flex justify-content-between mt-2">
              <small class="text-muted">-25%</small>
              <small class="text-muted">0%</small>
              <small class="text-muted">+25%</small>
            </div>
          </div>
          
          <div class="forecast-metrics mt-4">
            <div class="row g-2">
              <div class="col-6" v-for="(metric, key) in forecastMetrics" :key="key">
                <div class="metric-card p-2 border rounded">
                  <div class="small text-muted">{{ metric.label }}</div>
                  <div class="d-flex align-items-baseline">
                    <span class="h5 mb-0 me-2" :class="getMetricClass(metric.value)">
                      {{ metric.value > 0 ? '+' : '' }}{{ metric.value }}%
                    </span>
                    <small class="text-muted">{{ metric.timeframe }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- PE Mean Reversion -->
        <div v-else-if="activeTab === 'meanReversion'" class="mean-reversion-tab">
          <div class="chart-container" style="height: 200px; position: relative;">
            <canvas ref="meanReversionChart"></canvas>
          </div>
          <div class="mt-3">
            <div class="d-flex justify-content-between small mb-1">
              <span class="text-muted">Current PE:</span>
              <span class="fw-medium">{{ currentPE }}x</span>
            </div>
            <div class="d-flex justify-content-between small mb-1">
              <span class="text-muted">Historical Mean:</span>
              <span class="fw-medium">{{ historicalMean }}x</span>
            </div>
            <div class="d-flex justify-content-between small">
              <span class="text-muted">Deviation:</span>
              <span :class="['fw-medium', deviation >= 0 ? 'text-danger' : 'text-success']">
                {{ deviation > 0 ? '+' : '' }}{{ deviation }}%
              </span>
            </div>
          </div>
        </div>

        <!-- Historical Percentiles -->
        <div v-else class="percentile-tab">
          <div class="mb-3">
            <div class="d-flex justify-content-between small mb-2">
              <span class="text-muted">Current Valuation Percentile:</span>
              <span class="fw-medium">{{ currentPercentile }}%</span>
            </div>
            <div class="progress" style="height: 20px;">
              <div 
                class="progress-bar bg-primary" 
                role="progressbar" 
                :style="{ width: currentPercentile + '%' }"
                :aria-valuenow="currentPercentile" 
                aria-valuemin="0" 
                aria-valuemax="100"
              ></div>
            </div>
            <div class="d-flex justify-content-between mt-2">
              <small class="text-muted">0%</small>
              <small class="text-muted">50%</small>
              <small class="text-muted">100%</small>
            </div>
          </div>
          
          <div class="percentile-comparison">
            <div 
              v-for="(period, index) in percentileHistory" 
              v-show="!loading && !error"
              :key="index"
              class="d-flex align-items-center py-2 border-bottom"
            >
              <div class="flex-grow-1 small">
                {{ period.label }}
              </div>
              <div class="d-flex align-items-center">
                <div class="progress flex-grow-1 me-2" style="height: 6px; width: 100px;">
                  <div 
                    class="progress-bar" 
                    :class="getPercentileClass(period.percentile)"
                    role="progressbar" 
                    :style="{ width: period.percentile + '%' }"
                  ></div>
                </div>
                <span class="small fw-medium" :class="getPercentileTextClass(period.percentile)">
                  {{ period.percentile }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch, computed } from 'vue';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'ReturnProjections',
  props: {
    marketData: {
      type: Object as () => {
        id: string;
        name: string;
        pe: number;
        pb: number;
        dividendYield: number;
        pePercentile: number;
        pbPercentile: number;
        projections: {
          annualReturn: number;
          upsidePotential: number;
          downsideRisk: number;
          sharpeRatio: number;
          probabilityPositiveReturn: number;
        };
        valuationPercentiles: {
          '3y': number;
          '5y': number;
          '10y': number;
          '20y': number;
          allTime: number;
        };
      },
      required: true
    },
    timePeriod: {
      type: String as () => '3y' | '5y' | '10y' | '20y' | 'all',
      default: '5y'
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  },
  setup(props) {
    const activeTab = ref('forecast');
    const meanReversionChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    // Computed properties based on props
    const projections = computed(() => props.marketData?.projections || {
      annualReturn: 0,
      upsidePotential: 0,
      downsideRisk: 0,
      sharpeRatio: 0,
      probabilityPositiveReturn: 0
    });

    const currentPE = computed(() => props.marketData?.pe || 0);
    const historicalMean = ref(18.7); // This would come from API in a real app
    const currentPercentile = computed(() => {
      if (!props.marketData?.valuationPercentiles) return 0;
      return props.marketData.valuationPercentiles[props.timePeriod as keyof typeof props.marketData.valuationPercentiles] || 0;
    });

    const forecastMetrics = computed(() => [
      { label: 'Upside Potential', value: projections.value.upsidePotential, timeframe: '1Y' },
      { label: 'Downside Risk', value: projections.value.downsideRisk, timeframe: '1Y' },
      { label: 'Sharpe Ratio', value: projections.value.sharpeRatio, timeframe: '5Y' },
      { label: 'Probability Positive', value: projections.value.probabilityPositiveReturn, timeframe: '1Y' }
    ]);

    const percentileHistory = computed(() => {
      if (!props.marketData?.valuationPercentiles) return [];
      
      const { valuationPercentiles } = props.marketData;
      return [
        { label: 'Current', percentile: currentPercentile.value },
        { label: '3 Years', percentile: valuationPercentiles['3y'] },
        { label: '5 Years', percentile: valuationPercentiles['5y'] },
        { label: '10 Years', percentile: valuationPercentiles['10y'] },
        { label: '20 Years', percentile: valuationPercentiles['20y'] },
        { label: 'All Time', percentile: valuationPercentiles.allTime }
      ];
    });

    const deviation = computed(() => {
      if (!currentPE.value || !historicalMean.value) return 0;
      return Math.round(((currentPE.value - historicalMean.value) / historicalMean.value) * 100);
    });

    const getReturnClass = (value: number, isBg = false) => {
      if (value > 0) return isBg ? 'bg-success' : 'text-success';
      if (value < 0) return isBg ? 'bg-danger' : 'text-danger';
      return isBg ? 'bg-secondary' : 'text-muted';
    };

    const getMetricClass = (value: number) => {
      if (value > 0) return 'text-success';
      if (value < 0) return 'text-danger';
      return 'text-muted';
    };

    const getPercentileClass = (percentile: number) => {
      if (percentile >= 80) return 'bg-danger';
      if (percentile >= 60) return 'bg-warning';
      return 'bg-success';
    };

    const getPercentileTextClass = (percentile: number) => {
      if (percentile >= 80) return 'text-danger';
      if (percentile >= 60) return 'text-warning';
      return 'text-success';
    };

    const initMeanReversionChart = () => {
      if (!meanReversionChart.value) return;

      const ctx = meanReversionChart.value.getContext('2d');
      if (!ctx) return;

      // Destroy previous chart instance if it exists
      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({ length: 60 }, (_, i) => i + 1).map(i => `${i}M`),
          datasets: [
            {
              label: 'PE Ratio',
              data: Array.from({ length: 60 }, () => Math.random() * 10 + 15),
              borderColor: 'rgba(13, 110, 253, 0.8)',
              backgroundColor: 'rgba(13, 110, 253, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true,
              pointRadius: 0
            },
            {
              label: 'Historical Mean',
              data: Array(60).fill(historicalMean.value),
              borderColor: 'rgba(108, 117, 125, 0.8)',
              borderWidth: 1,
              borderDash: [5, 5],
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 12,
                padding: 10,
                usePointStyle: true,
                pointStyle: 'circle'
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleFont: { size: 12 },
              bodyFont: { size: 12 },
              padding: 10,
              callbacks: {
                label: (context) => {
                  return ` ${context.dataset.label}: ${context.parsed.y.toFixed(2)}x`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                maxRotation: 0,
                autoSkip: true,
                maxTicksLimit: 6
              }
            },
            y: {
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              title: {
                display: true,
                text: 'PE Ratio'
              }
            }
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          }
        }
      });
    };

    // Watch for tab changes to initialize charts when needed
    watch(activeTab, (newTab) => {
      if (newTab === 'meanReversion' && meanReversionChart.value) {
        // Small delay to ensure the container is rendered
        setTimeout(() => {
          initMeanReversionChart();
        }, 100);
      }
    });

    // Watch for time period changes to update data
    watch(() => props.timePeriod, (newPeriod, oldPeriod) => {
      if (newPeriod !== oldPeriod && activeTab.value === 'meanReversion') {
        nextTick(() => {
          initMeanReversionChart();
        });
      }
    });
    
    // Watch for market data changes
    watch(() => props.marketData, (newData, oldData) => {
      if (newData?.id !== oldData?.id) {
        // Reinitialize charts when market changes
        nextTick(() => {
          if (activeTab.value === 'meanReversion') {
            initMeanReversionChart();
          }
        });
      }
    }, { deep: true });

    onMounted(() => {
      // Initialize the chart if the default tab is meanReversion
      if (activeTab.value === 'meanReversion') {
        initMeanReversionChart();
      }
    });

    return {
      activeTab,
      projections,
      forecastMetrics,
      meanReversionChart,
      currentPE,
      historicalMean,
      deviation,
      currentPercentile,
      percentileHistory,
      getReturnClass,
      getMetricClass,
      getPercentileClass,
      getPercentileTextClass,
      loading: computed(() => props.loading),
      error: computed(() => props.error)
    };
  }
});
</script>

<style scoped>
.nav-tabs {
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 1rem;
}

.nav-tabs .nav-link {
  color: #6c757d;
  font-weight: 500;
  border: none;
  padding: 0.5rem 0.75rem;
  position: relative;
  transition: all 0.2s ease;
}

.nav-tabs .nav-link:hover {
  color: #0d6efd;
  border: none;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  background: none;
  border: none;
  border-bottom: 2px solid #0d6efd;
  font-weight: 600;
}

.metric-card {
  transition: all 0.2s ease;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.metric-card:hover {
  background-color: #f1f3f5;
  transform: translateY(-2px);
}

.progress {
  border-radius: 10px;
  background-color: #e9ecef;
  overflow: hidden;
}

.progress-bar {
  transition: width 0.6s ease;
}

.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
}

.percentile-comparison {
  max-height: 200px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar */
.percentile-comparison::-webkit-scrollbar {
  width: 4px;
}

.percentile-comparison::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.percentile-comparison::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.percentile-comparison::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
