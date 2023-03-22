import * as React from 'react';
import { useTranslation } from 'react-i18next';

import { State } from '$src/store/types';

import { fetchData } from '../api/traffic';
import useLineChart from '../hooks/useLineChart';
import { chartJSResource, chartStyles, commonDataSetProps } from '../misc/chart';
import { getClashAPIConfig, getSelectedChartStyleIndex } from '../store/app';
import { connect } from './StateProvider';
import s0 from './AllChart.module.scss';
import TrafficChart from './TrafficChart';

// echars
import EChartsReactCore from 'echarts-for-react/lib/core';
// Import the echarts core module, which provides the necessary interfaces for using echarts.
import * as echarts from 'echarts/core';
import ReactECharts from 'echarts-for-react';
// Import charts, all with Chart suffix
import { BarChart, BarSeriesOption } from 'echarts/charts';
// import components, all suffixed with Component
import {GridComponent, TooltipComponent, TitleComponent, DatasetComponent} from "echarts/components"
// Import renderer, note that introducing the CanvasRenderer or SVGRenderer is a required step
import {
  CanvasRenderer,
  // SVGRenderer,
} from 'echarts/renderers';
import { EChartsCoreOption, EChartsOption } from 'echarts';
// Register the required components
echarts.use(
  [TitleComponent, TooltipComponent, GridComponent, CanvasRenderer, BarChart]
);
const { useMemo } = React;

const mapState = (s: State) => ({
  apiConfig: getClashAPIConfig(s),
  selectedChartStyleIndex: getSelectedChartStyleIndex(s),
});

export default connect(mapState)(AllChart);

function AllChart({ apiConfig, selectedChartStyleIndex }) {
  const { t } = useTranslation();

  return (
    <div className={s0.AllChart}>

      <div className={s0.sec}>
      <TrafficChart />
      </div>

      <div className={s0.sec}>
      <EChartsReactCore
        echarts={echarts}
        option={
          {
            yAxis: {
              axisLine:{
                show:false
              },
              axisTick:{
                show:false
              },
              type: 'category',
              data: ['192.168.130.235', '192.168.130.5', '192.168.0.235', '192.168.130.235', '192.168.130.235', '192.168.130.235', '192.168.130.235']
            },
            xAxis: {
              axisLine:{
                show:false
              },
              splitLine:{
                show:false
              },
              axisLabel:{
                show:false
              },
              type: 'value'
            },
            grid:{
              left: "110px",
              right:"40px",
              bottom:"10px",
              top:"10px"
            },
            series: [
              {
                label:{
                  color:"gray",
                  show:true,
                  position:"right"
                },
                data: [120, 200, 150, 80, 70, 110, 130],
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                  color: 'rgba(180, 180, 180, 0.2)'
                }
              }
            ]
          } as EChartsOption
        }
      />
      </div>


    </div>
  );
}
