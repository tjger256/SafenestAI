import React, { useEffect, useState } from 'react';
import { ReactGoogleChartEvent, Chart } from 'react-google-charts';
import axios from 'axios';
import './Charter.css';

export const options = {
  title: 'Baby Vitals',
  titleTextStyle: {color: 'white'},
  hAxis: {
    title: "Time",
    textStyle: {color: 'white'}
  },
  vAxis: {
    title: "Value",
    textStyle: {color: 'white'}
  },
  legend: {
    textStyle: {color: 'white'}
  },
  series: {
    0: {
      curveType: "function"
    },
    1: {
      curveType: "function"
    },
    2: {
      type: "scatter",
      visibleInLegend: false
    }
  },
  backgroundColor: 'black',
};

export const chartEvents: ReactGoogleChartEvent[] = [
  {
    eventName: "select",
    callback: ({ chartWrapper }) => {
      const chart = chartWrapper.getChart();
      const selection = chart.getSelection();
      if (selection.length === 1) {
        const [selectedItem] = selection;
        const dataTable = chartWrapper.getDataTable();
        const { row, column } = selectedItem;

        alert("You selected:" + 
          row + " " +
          column + " " +
          dataTable?.getValue(row, column)
        );
      }
    },
  },
];

const Charter: React.FC = () => {
  const [data, setData] = useState<any[]>([]);

  // useEffect(() => {
  //   fetch('http://127.0.0.1:1601/data')
  //     .then(response => response.json())
  //     .then(data => setData(data))
  //     .catch(error => console.error('Error fetching data:', error));
  // }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:1601/data');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData(); // Initial fetch

    const intervalId = setInterval(fetchData, 1000); // Fetch data every 5 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div>
      {/* <h1>Line Chart from Python Backend</h1> */}
      {data.length > 0 ? (
        <Chart
          chartType="LineChart"
          width="100%"
          height="400px"
          data={data}
          options={options}
          chartEvents={chartEvents}
        />
      ) : (
        <p>Loadings...</p>
      )}
    </div>
  );
};

export default Charter;