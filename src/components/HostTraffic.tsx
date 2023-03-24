import * as React from 'react';
import { useTranslation } from 'react-i18next';

import { State } from '$src/store/types';
import { ClashAPIConfig } from '$src/types';

import * as connAPI from '../api/connections';
import { fetchData } from '../api/traffic';
import prettyBytes from '../misc/pretty-bytes';
import { getClashAPIConfig } from '../store/app';
import { connect } from './StateProvider';
import s0 from './TrafficNow.module.scss';
import { fetchStatisticData } from '$src/api/statistic';
import { EChartsCoreOption, EChartsOption } from 'echarts';
import EChartsReactCore from 'echarts-for-react/lib/core';
import * as echarts from 'echarts/core';
import { context } from './AllChart';

const { useState, useEffect, useCallback, useContext } = React;

const mapState = (s: State) => ({
  apiConfig: getClashAPIConfig(s),
});
export default connect(mapState)(TrafficNow);

function TrafficNow({ apiConfig }) {
  const { t } = useTranslation();
  const { category, value } = useClientCount();

  
  return (
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
              data: category
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
              left: "10px",
              top:"10px",
              bottom: "10px",
              containLabel:true
            },
            series: [
              {
                label:{
                  formatter:function (params){
                      return (parseFloat(params.value + '') /(1000 * 1000)).toFixed(2) + 'MB'
                  },
                  color:"gray",
                  show:true,
                  position:"right"
                },
                data: value,
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
  );
}

function useClientCount(){
  const [client_count, setClientCount] = useState({category:[], value:[]})

  fetchStatisticData().subscribe((o) =>{
    setClientCount({
        category: o.host_traffic.category,
        value: o.host_traffic.value
    })
  }
    
  );

    return client_count
}