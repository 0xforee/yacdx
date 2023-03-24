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

  var i;
  var traffic_data:any[] = new Array(category.length)
  for(i = 0; i < category.length -1; i++) {
    traffic_data[i] = { value: value[i], name: category[i]}
  }
  
  return (
    <EChartsReactCore
        echarts={echarts}
        option={
          {
            tooltip: {
              trigger: 'item',
              formatter:function (params){
                return params.name + ' ' + (parseFloat(params.value + '') /(1000 * 1000)).toFixed(2) + 'MB'
              }
            },
            legend: {
              bottom: '1%',
              left: 'center'
            },
            grid:{
              left:"100px",
              top:"100px",
              bottom: "100px",
              // containLabel:true
            },
            series: [
              {
                name: 'Access From',
                type: 'pie',
                radius: ['35%', '65%'],
                avoidLabelOverlap: true,
                label: {
                  formatter:function (params){
                    return params.name + ' ' + (parseFloat(params.value + '') /(1000 * 1000)).toFixed(2) + 'MB'
                },
                  show: true,
                },
                
                labelLine: {
                  show: true
                },
                data: traffic_data
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
        category: o.proxy_traffic.category,
        value: o.proxy_traffic.value
    })
  }
    
  );

    return client_count
}