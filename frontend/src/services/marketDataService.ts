// API base URL will be used when connecting to real backend
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

interface MarketDataParams {
  marketId: string;
  timePeriod: string;
}

export interface MarketData {
  id: string;
  name: string;
  currentValue: number;
  change: number;
  pe: number;
  pb: number;
  dividendYield: number;
  pePercentile: number;
  pbPercentile: number;
  lastUpdated: string;
  historicalPE: { date: string; value: number }[];
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
}

export const marketDataService = {
  async getMarketData({ marketId, timePeriod }: MarketDataParams): Promise<MarketData> {
    try {
      // In a real app, this would be an actual API call
      // const response = await axios.get(`${API_BASE_URL}/market-data/${marketId}`, {
      //   params: { period: timePeriod }
      // });
      // return response.data;

      // Mock data for demonstration
      return mockMarketData(marketId, timePeriod);
    } catch (error) {
      console.error('Error fetching market data:', error);
      throw error;
    }
  },

  async getHistoricalData(_marketId: string, timePeriod: string) {
    try {
      // Mock implementation - replace with actual API call
      return generateHistoricalData(timePeriod);
    } catch (error) {
      console.error('Error fetching historical data:', error);
      throw error;
    }
  }
};

// Helper function to generate mock data
function mockMarketData(marketId: string, timePeriod: string): MarketData {
  const now = new Date();
  const lastUpdated = now.toISOString();
  
  // Base values for different markets
  const marketConfigs: Record<string, { name: string; basePE: number; basePB: number; divYield: number }> = {
    'sp500': { name: 'S&P 500', basePE: 24.5, basePB: 4.2, divYield: 1.4 },
    'nasdaq': { name: 'NASDAQ', basePE: 32.1, basePB: 5.7, divYield: 0.8 },
    'hsi': { name: 'Hang Seng', basePE: 10.2, basePB: 0.9, divYield: 3.8 },
    'csi300': { name: 'CSI 300', basePE: 13.8, basePB: 1.6, divYield: 2.5 },
    'stoxx50': { name: 'Euro Stoxx 50', basePE: 15.3, basePB: 1.8, divYield: 3.2 },
    'nikkei': { name: 'Nikkei 225', basePE: 16.7, basePB: 1.5, divYield: 1.9 },
    'nifty50': { name: 'NIFTY 50', basePE: 22.8, basePB: 3.8, divYield: 1.2 },
    'sensex': { name: 'SENSEX', basePE: 23.1, basePB: 3.6, divYield: 1.3 },
    'straits': { name: 'STI', basePE: 11.5, basePB: 1.1, divYield: 4.1 },
    'asx200': { name: 'ASX 200', basePE: 17.3, basePB: 2.3, divYield: 4.3 },
  };

  const market = marketConfigs[marketId] || { name: 'Unknown', basePE: 15, basePB: 2, divYield: 2, baseValue: 1000 };
  
  // Add some randomness to the base values
  const pe = market.basePE * (0.9 + Math.random() * 0.2);
  const pb = market.basePB * (0.9 + Math.random() * 0.2);
  const divYield = market.divYield * (0.9 + Math.random() * 0.2);
  
  // Calculate index value based on PB ratio
  const baseValue = Math.round(1000 + Math.random() * 40000);
  const change = -5 + Math.random() * 10;
  const pePercentile = Math.floor(Math.random() * 100);
  const pbPercentile = Math.floor(Math.random() * 100);
  
  // Generate historical PE data
  const historicalPE = Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (30 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    value: pe * (0.8 + Math.random() * 0.4) // Random value within 20% of current PE
  }));
  
  // Generate valuation percentiles
  const valuationPercentiles = {
    '3y': Math.floor(20 + Math.random() * 60),
    '5y': Math.floor(15 + Math.random() * 70),
    '10y': Math.floor(10 + Math.random() * 80),
    '20y': Math.floor(5 + Math.random() * 90),
    allTime: Math.floor(Math.random() * 100)
  };

  return {
    id: marketId,
    name: market.name,
    currentValue: baseValue,
    change: parseFloat(change.toFixed(2)),
    pe: parseFloat(pe.toFixed(2)),
    pb: parseFloat(pb.toFixed(2)),
    dividendYield: parseFloat(divYield.toFixed(2)),
    pePercentile,
    pbPercentile,
    lastUpdated: new Date().toISOString(),
    historicalPE,
    projections: {
      annualReturn: parseFloat((Math.random() * 20 - 5).toFixed(1)),
      upsidePotential: parseFloat((5 + Math.random() * 15).toFixed(1)),
      downsideRisk: parseFloat((-5 - Math.random() * 10).toFixed(1)),
      sharpeRatio: parseFloat((0.5 + Math.random() * 1.5).toFixed(2)),
      probabilityPositiveReturn: parseFloat((50 + Math.random() * 45).toFixed(1))
    },
    valuationPercentiles
  };
}

function generateHistoricalData(timePeriod: string) {
  const now = new Date();
  let months = 60; // Default 5 years
  
  switch(timePeriod) {
    case '3y': months = 36; break;
    case '5y': months = 60; break;
    case '10y': months = 120; break;
    case '20y': months = 240; break;
    case 'all': months = 300; break; // 25 years for 'all'
  }
  return Array.from({ length: months }, (_, i) => {
    const date = new Date(now);
    date.setMonth(date.getMonth() - (months - i - 1));
    return {
      date: date.toISOString().split('T')[0],
      value: parseFloat((10 + Math.random() * 20).toFixed(2))
    };
  });
}
