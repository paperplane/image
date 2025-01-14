import csv
import pprint


def read_csv():
    redis_dict = {}
    mysql_dict = {}
    methods = ['GetSkuStock', 'MGetSkuBackendStock', 'MGetSkuStockByProductID', 'MGetSkuStockBySkuID',
               'StockBizQuery', 'StockBizCheck', 'BatchGetStoreForMarket', 'MGetProductStock', 'PreStockBizDecrease',
               'SetBackendStock']
    methods = ['GetSkuStockNonCache', 'GetWarehouseListForMarket', 'GetWarehouseByStoreToC', 'GetCargoBindFromDB',
               'StockBizDecrease']
    methods = ['OnBingLogEvent', 'MessageHandler', 'OnStockEvent', 'OnStockDecreaseEvent', 'OnActivityReturnEvent']
    with open('/Users/bytedance/Downloads/117760538-3585809254.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            from_psm, from_method, to_psm, to_method = lines

            read_or_write = 'N'
            service_type = 'TCE'
            to_psm = to_psm.replace('.service.hj', '')
            if to_psm.endswith('_read'):
                read_or_write = 'R'
                to_psm = to_psm.replace('_read', '')
                to_method = to_method.split('.')[0]
            elif to_psm.endswith('_write'):
                read_or_write = 'W'
                to_psm = to_psm.replace('_write', '')
                to_method = to_method.split('.')[0]
            elif to_psm.endswith('_2'):
                to_psm = to_psm.replace('_2', '')
            elif to_psm.endswith('_1'):
                to_psm = to_psm.replace('_1', '')
            elif to_psm.endswith('_3'):
                to_psm = to_psm.replace('_3', '')
            else:
                read_or_write = 'N'

            if to_psm.startswith('toutiao.mysql'):
                service_type = 'MySQL'
            elif to_psm.startswith('toutiao.redis'):
                service_type = 'Redis'
            elif to_psm.startswith('bytefaas'):
                service_type = 'FaaS'
            else:
                service_type = 'TCE'

            # print(from_psm, from_method, to_psm, to_method, read_or_write, service_type)
            if service_type == 'MySQL':
                mysql_dict.setdefault(to_psm + ' ' + to_method, set()).add(from_method)

            elif service_type == 'Redis':
                redis_dict.setdefault(to_psm, set()).add(from_method)

    pprint.pprint(mysql_dict)

    print('-----')
    pprint.pprint(redis_dict)


if __name__ == '__main__':
    read_csv()
