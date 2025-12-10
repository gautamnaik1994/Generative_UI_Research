import {
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Line,
} from 'recharts'

import React, { useState, useEffect, useRef } from 'react'

// #region Sample data
const data = [
  {
    Date: '2025-11-10',
    Open: 268.9599914550781,
    High: 273.7300109863281,
    Low: 267.4599914550781,
    Close: 269.43,
    Volume: 41312400,
    Dividends: 0.26,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-11',
    Open: 269.80999755859375,
    High: 275.9100036621094,
    Low: 269.79998779296875,
    Close: 275.25,
    Volume: 46208300,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-12',
    Open: 275.0,
    High: 275.7300109863281,
    Low: 271.70001220703125,
    Close: 273.47,
    Volume: 48398000,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-13',
    Open: 274.1099853515625,
    High: 276.70001220703125,
    Low: 272.0899963378906,
    Close: 272.95,
    Volume: 49602800,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-14',
    Open: 271.04998779296875,
    High: 275.9599914550781,
    Low: 269.6000061035156,
    Close: 272.41,
    Volume: 47431300,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-17',
    Open: 268.82000732421875,
    High: 270.489990234375,
    Low: 265.7300109863281,
    Close: 267.46,
    Volume: 45018300,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-18',
    Open: 269.989990234375,
    High: 270.7099914550781,
    Low: 265.32000732421875,
    Close: 267.44,
    Volume: 45677300,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-19',
    Open: 265.5299987792969,
    High: 272.2099914550781,
    Low: 265.5,
    Close: 268.56,
    Volume: 40424500,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-20',
    Open: 270.8299865722656,
    High: 275.42999267578125,
    Low: 265.9200134277344,
    Close: 266.25,
    Volume: 45823600,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-21',
    Open: 265.95001220703125,
    High: 273.3299865722656,
    Low: 265.6700134277344,
    Close: 271.49,
    Volume: 59030800,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-24',
    Open: 270.8999938964844,
    High: 277.0,
    Low: 270.8999938964844,
    Close: 275.92,
    Volume: 65585800,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-25',
    Open: 275.2699890136719,
    High: 280.3800048828125,
    Low: 275.25,
    Close: 276.97,
    Volume: 46914200,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-26',
    Open: 276.9599914550781,
    High: 279.5299987792969,
    Low: 276.6300048828125,
    Close: 277.55,
    Volume: 33431400,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-11-28',
    Open: 277.260009765625,
    High: 279.0,
    Low: 275.989990234375,
    Close: 278.85,
    Volume: 20135600,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-01',
    Open: 278.010009765625,
    High: 283.4200134277344,
    Low: 276.1400146484375,
    Close: 283.1,
    Volume: 46587700,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-02',
    Open: 283.0,
    High: 287.3999938964844,
    Low: 282.6300048828125,
    Close: 286.19,
    Volume: 53669500,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-03',
    Open: 286.20001220703125,
    High: 288.6199951171875,
    Low: 283.29998779296875,
    Close: 284.15,
    Volume: 43538700,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-04',
    Open: 284.1000061035156,
    High: 284.7300109863281,
    Low: 278.5899963378906,
    Close: 280.7,
    Volume: 43989100,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-05',
    Open: 280.5400085449219,
    High: 281.1400146484375,
    Low: 278.04998779296875,
    Close: 278.78,
    Volume: 47265800,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-08',
    Open: 278.1300048828125,
    High: 279.6700134277344,
    Low: 276.1499938964844,
    Close: 277.89,
    Volume: 38211800,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
  {
    Date: '2025-12-09',
    Open: 278.1600036621094,
    High: 280.0299987792969,
    Low: 276.9200134277344,
    Close: 277.18,
    Volume: 32159900,
    Dividends: 0.0,
    'Stock Splits': 0.0,
  },
]

// #endregion

export function useStableValue<T>(value: T, repeats: number = 2): T {
  const [stable, setStable] = useState<T>(value)

  const ref = useRef<{ value: T; count: number }>({
    value,
    count: 0,
  })

  useEffect(() => {
    if (ref.current.value === value) {
      // same value repeated
      ref.current.count++

      if (ref.current.count >= repeats) {
        setStable(value)
      }
    } else {
      // value changed — reset
      ref.current = { value, count: 0 }
    }
  }, [value, repeats])

  return stable
}

export function useDebounce<T>(value: T, delay = 250): T {
  const [debounced, setDebounced] = useState(value)

  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(id)
  }, [value, delay])

  return debounced
}

// props

interface ChartProps {
  dataKey: any[]
  x_axis: string
  y_axis: string
}

const Chart = ({ dataKey, x_axis, y_axis }: ChartProps) => {
  console.log('Chart component received dataKey:', dataKey)
  if (!dataKey) {
    return <div>Loading chart data...</div>
  }
  const stableKey = useDebounce(dataKey, 200) // <-- FIX
  const [fetchedData, setFetchedData] = useState<any[]>([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/data_registry/${stableKey}`
        )
        const result = await response.json()
        console.log('Fetched data:', result)
        if (Array.isArray(result.value)) {
          setFetchedData(result.value)
        }
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }

    fetchData()
  }, [stableKey])

  return (
    <LineChart
      style={{
        width: '100%',
        maxWidth: '700px',
        maxHeight: '70vh',
        aspectRatio: 1.618,
      }}
      responsive
      data={fetchedData}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey={x_axis} />
      <YAxis width="auto" />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey={y_axis} stroke="#8884d8" />
    </LineChart>
  )
}

export default Chart
