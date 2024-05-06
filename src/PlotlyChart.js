import React from 'react';
import Plot from 'react-plotly.js';

class PlotlyChart extends React.Component {
  render() {
    return (
      <Plot
        data={[
          {
            type: 'scatter',
            mode: 'lines+markers',
            x: [1, 2, 3],
            y: [2, 6, 3],
            marker: {color: 'red'},
          },
          // More traces here as needed
        ]}
        layout={{width: 320, height: 240, title: 'A Fancy Plot'}}
      />
    );
  }
}

export default PlotlyChart;
