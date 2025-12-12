// implement a react table component that displays the above data. use dynamic column headers based on the keys in the data objects. export the component as default.
import React, { useState, useEffect } from 'react'
import useDebounce from '../hooks/useDebounce'

interface TableProps {
  dataKey: string
}

const Table: React.FC<TableProps> = ({ dataKey }: TableProps) => {
  if (!dataKey) {
    return <div>Loading data...</div>
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

  const columns = Object.keys(fetchedData[0] || {})

  return (
    <table className="min-w-full border-collapse border border-gray-200">
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={col}
              className="border border-gray-300 px-4 py-2 bg-gray-100 text-left"
            >
              {col}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {fetchedData.map((row, rowIndex) => (
          <tr key={rowIndex} className="hover:bg-gray-50">
            {columns.map((col) => (
              <td key={col} className="border border-gray-300 px-4 py-2">
                {row[col]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default Table
