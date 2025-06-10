<template>
  <div class="metric-card p-3 border rounded h-100">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold small">{{ metric.label }}</span>
      <span class="badge" :class="getBadgeClass">
        {{ getBadgeLabel }}
      </span>
    </div>
    <div class="d-flex justify-content-between align-items-end">
      <div>
        <h4 class="mb-0">
          {{ formattedValue }}
          <small v-if="metric.additional" class="text-muted">{{ metric.additional }}</small>
        </h4>
        <small class="text-muted">vs {{ formattedIndustryAvg }} industry avg</small>
      </div>
      <div class="text-end">
        <div v-if="difference !== null" :class="differenceClass">
          <i :class="differenceIcon"></i>
          {{ formattedDifference }}
        </div>
      </div>
    </div>
    <div class="progress mt-2" style="height: 4px;">
      <div 
        class="progress-bar" 
        :class="progressBarClass"
        role="progressbar" 
        :style="{ width: progressWidth + '%' }"
      ></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'MetricCard',
  
  props: {
    metric: {
      type: Object,
      required: true
    },
    value: {
      type: [Number, String],
      required: true
    },
    industryAvg: {
      type: [Number, String],
      required: true
    }
  },
  
  setup(props) {
    // Format the value based on the metric type
    const formattedValue = computed(() => {
      if (props.metric.format === 'percent') return `${props.value}%`;
      if (props.metric.format === 'multiple') return `${props.value}x`;
      return props.value;
    });
    
    // Format the industry average
    const formattedIndustryAvg = computed(() => {
      if (props.metric.format === 'percent') return `${props.industryAvg}%`;
      if (props.metric.format === 'multiple') return `${props.industryAvg}x`;
      return props.industryAvg;
    });
    
    // Calculate the difference from industry average
    const difference = computed(() => {
      if (typeof props.value === 'number' && typeof props.industryAvg === 'number') {
        return props.value - props.industryAvg;
      }
      return null;
    });
    
    // Format the difference for display
    const formattedDifference = computed(() => {
      if (difference.value === null) return '';
      const absDiff = Math.abs(difference.value);
      
      if (props.metric.format === 'percent') return `${absDiff.toFixed(1)}%`;
      if (props.metric.format === 'multiple') return `${absDiff.toFixed(1)}x`;
      return absDiff.toFixed(1);
    });
    
    // Determine the difference icon and color
    const differenceIcon = computed(() => {
      if (difference.value === null) return '';
      
      // For reverse metrics (where lower is better), flip the logic
      const isBetter = props.metric.reverse 
        ? difference.value < 0 
        : difference.value > 0;
      
      return isBetter ? 'bi bi-arrow-up' : 'bi bi-arrow-down';
    });
    
    const differenceClass = computed(() => {
      if (difference.value === null) return '';
      
      // For reverse metrics (where lower is better), flip the logic
      const isBetter = props.metric.reverse 
        ? difference.value < 0 
        : difference.value > 0;
      
      return isBetter ? 'text-success' : 'text-danger';
    });
    
    // Determine badge class based on value
    const getBadgeClass = computed(() => {
      if (difference.value === null) return 'bg-secondary';
      
      // For reverse metrics (where lower is better), flip the logic
      const isBetter = props.metric.reverse 
        ? difference.value < 0 
        : difference.value > 0;
      
      return isBetter ? 'bg-success' : 'bg-warning';
    });
    
    // Determine badge label
    const getBadgeLabel = computed(() => {
      if (difference.value === null) return 'N/A';
      
      // For reverse metrics (where lower is better), flip the logic
      const isBetter = props.metric.reverse 
        ? difference.value < 0 
        : difference.value > 0;
      
      return isBetter ? 'Better' : 'Worse';
    });
    
    // Calculate progress bar width
    const progressWidth = computed(() => {
      const value = parseFloat(props.value);
      if (isNaN(value)) return 0;
      
      // For percentages, cap at 100%
      if (props.metric.format === 'percent') {
        return Math.min(value, 100);
      }
      
      // For multiples, use a reasonable scale
      if (props.metric.format === 'multiple') {
        return Math.min(value * 10, 100);
      }
      
      // Default to the value itself (capped at 100)
      return Math.min(value, 100);
    });
    
    // Determine progress bar color
    const progressBarClass = computed(() => {
      if (difference.value === null) return 'bg-secondary';
      
      // For reverse metrics (where lower is better), flip the logic
      const isBetter = props.metric.reverse 
        ? difference.value < 0 
        : difference.value > 0;
      
      return isBetter ? 'bg-success' : 'bg-warning';
    });
    
    return {
      formattedValue,
      formattedIndustryAvg,
      difference,
      formattedDifference,
      differenceIcon,
      differenceClass,
      getBadgeClass,
      getBadgeLabel,
      progressWidth,
      progressBarClass
    };
  }
});
</script>

<style scoped>
.metric-card {
  transition: all 0.2s ease;
  background-color: #fff;
}

.metric-card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.badge {
  font-size: 0.7rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
}

h4 {
  font-size: 1.25rem;
  font-weight: 600;
}

.small {
  font-size: 0.8rem;
}

.text-muted {
  color: #6c757d !important;
}
</style>
