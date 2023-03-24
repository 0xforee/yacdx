import { ClashAPIConfig } from '$src/types';

import { buildWebSocketURL, getURLAndInit } from '../misc/request-helper';

import socketio, { io } from 'socket.io-client'

var socket = io('ws://127.0.0.1:9001');
console.log('create websocket connect')
socket.on('connect', onConnect);
socket.on('disconnect', onDisconnect);
socket.on('statistic', onStatistic);


function onConnect(){
  return statistic
}

function onDisconnect(){

}

function onStatistic(value){
    console.log('onStatistic: ' + value)
    statistic.appendData(value)
}


const Size = 150;

const statistic = {
  client_count:{
    category:[],
    value:[]
  },
  client_traffic:{
    category:[],
    value:[]
  },

  subscribers: [],
  appendData(o: { client_count:{}, client_traffic:{} }) {
    this.subscribers.forEach((f) => f(o));
  },

  subscribe(listener: (x: any) => void) {
    this.subscribers.push(listener);
    return () => {
      const idx = this.subscribers.indexOf(listener);
      this.subscribers.splice(idx, 1);
    };
  },
};

function fetchStatisticData() {
  return statistic;
}

export { fetchStatisticData };
