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
import { createContext,useContext } from 'react';
// echars
import EChartsReactCore from 'echarts-for-react/lib/core';
// Import the echarts core module, which provides the necessary interfaces for using echarts.
import * as echarts from 'echarts/core';
import ReactECharts from 'echarts-for-react';
// Import charts, all with Chart suffix
import { BarChart, PieChart, PieSeriesOption, BarSeriesOption } from 'echarts/charts';
import { LabelLayout } from 'echarts/features';

// import components, all suffixed with Component
import {GridComponent, TooltipComponent, TitleComponent, DatasetComponent} from "echarts/components"
// Import renderer, note that introducing the CanvasRenderer or SVGRenderer is a required step
import {
  CanvasRenderer,
  // SVGRenderer,
} from 'echarts/renderers';
import { EChartsCoreOption, EChartsOption } from 'echarts';
import ClientCount from './ClientCount';
import ClientTraffic from './ClientTraffic';
import HostCount from './HostCount';
import HostTraffic from './HostTraffic';
import ProxyTraffic from './ProxyTraffic';
// Register the required components
echarts.use(
  [TitleComponent, TooltipComponent, GridComponent, CanvasRenderer, BarChart, PieChart, LabelLayout]
);
const { useMemo } = React;

export const context = createContext('')

const mapState = (s: State) => ({
  apiConfig: getClashAPIConfig(s),
  selectedChartStyleIndex: getSelectedChartStyleIndex(s),
});

interface Param{
  param:string
}
export default connect(mapState)(AllChart);

function AllChart({ apiConfig, selectedChartStyleIndex }) {
  const { t } = useTranslation();

  return (
    <div className={s0.AllChart}>

      <div className={s0.sec}>
      <TrafficChart />
      </div>

          <div className={s0.sec}>
        
              <ClientCount/>
          </div>

          <div className={s0.sec}>
        
              <ClientTraffic/>
          </div>
          <div className={s0.sec}>
        
              <HostCount/>
          </div>
          <div className={s0.sec}>
        
              <HostTraffic/>
          </div>
          {/* <div className={s0.sec}>
        
            <ProxyCount/>
        </div> */}
        <div className={s0.sec}>
            
                  <ProxyTraffic/>
              </div>
      


    </div>
  );
}
