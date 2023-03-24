import websocket
import json
from log import log_info,log_error,log_debug
from db_helper import DBHelper
from config import configs

test_message_json = '''
{
   "downloadTotal":482546,
   "uploadTotal":193964,
   "connections":[
      {
         "id":"99427630-ba17-4f69-8f56-b95da47d3b57",
         "metadata":{
            "network":"tcp",
            "type":"Socks4",
            "sourceIP":"172.17.0.1",
            "destinationIP":"20.205.243.166",
            "sourcePort":"56950",
            "destinationPort":"443",
            "host":"",
            "dnsMode":"normal",
            "processPath":"",
            "specialProxy":""
         },
         "upload":6083,
         "download":31306,
         "start":"2023-03-20T06:36:30.809383885Z",
         "chains":[
            "JK1-V4-广港BGP01|v2ray",
            "Proxy",
            "Others"
         ],
         "rule":"Match",
         "rulePayload":""
      }
   ]
}
'''


class Connections:
    def __init__(self):
        self.url = configs.clash_websocket_connections_url
        self.ws = None
        self.db_helper = DBHelper()
        self.pre_connections = []
        self.cur_connections = []
        self.closed_connections = []

    def teardown(self):
        self.ws.close()
        log_info("connection server closed")

    def on_open(self, ws):
        """
        Callback object which is called at opening websocket.
        1 argument:
        @ ws: the WebSocketApp object
        """
        log_info('A new WebSocketApp is opened!')

    def on_message(self, ws, message):
        """
        Callback object which is called when received data.
        2 arguments:
        @ ws: the WebSocketApp object
        @ message: utf-8 data received from the server
        """
        try:
        # 对收到的message进行解析
        #     print(message)
            received_msg = json.loads(message)
            self.deal_conenction_changed(received_msg['connections'])
        except Exception as e:
            log_error("on_message: %s " % e)


    def deal_conenction_changed(self, connections):
        """
        prev: A B C
        cur:    B C D
        A: closed,deal
        B,C: connecting,ignore
        D: added,ignore
        """
        # 检查 connections，判断哪些被 close 了
        self.cur_connections = connections
        # print(connections)
        for prev in self.pre_connections:
            prev_id = prev['id']
            found = False
            for cur in self.cur_connections:
                cur_id = cur['id']
                if prev_id == cur_id:
                    found = True
                    break

            if not found:
                self.deal_closed_connection(prev)

        self.pre_connections = connections

    def deal_closed_connection(self, connection):
        """
        处理已被关闭的 connection
        :param connection:
        :return:
        """
        id = connection['id']
        log_info('%s connection closed!' % id)
        self.db_helper.insert(connection)

    def on_close(self, ws, close_status_code, close_msg):
        log_info('The websocket connect is closed')
        print(close_msg)

    def on_error(self, ws, error):
        log_error("on_error:" + str(error))

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log_info("start connection server")
    conn = Connections()
    conn.start()


