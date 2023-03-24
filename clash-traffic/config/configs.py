
clash_websocket_connections_url = 'ws://192.168.0.99:9090/connections?token=123456'

statistic_config = {
    "client_count": 'select source_ip, count(conn_id) as count from connections where proxy is not "DIRECT" group by source_ip order by count DESC limit 15;',
    "client_traffic": 'select source_ip, sum(download) as traffic from connections where proxy is not "DIRECT" group by source_ip order by traffic DESC limit 15;',
    "host_count": 'select host, count(conn_id) as count from connections where proxy is not "DIRECT" group by host order by count DESC limit 15;',
    "host_traffic": 'select host, sum(download) as traffic from connections where proxy is not "DIRECT" group by host order by traffic DESC limit 15;',
    "proxy_count": "select proxy, count(conn_id) as count from connections group by proxy order by count DESC limit 15;",
    "proxy_traffic": "select proxy, sum(download) as traffic from connections group by proxy order by traffic DESC limit 15;"
}