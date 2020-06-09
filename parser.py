import textfsm
import csv
import sys

class Get(object):
    """docstring for Get."""

    def __init__(self, status,message,data):
        super(Get, self).__init__()
        self.data = data
        self.status = status
        self.message = message

class Nokia(object):
    """docstring for Nokia."""

    def __init__(self, arg):
        super(Nokia, self).__init__()
        self.arg = arg
    def stage1(self):
        if len(self.arg) < 5:
            return Get(404,'The arguments are invalid, format: [--stage-1] template [files] output_name',None)
        data = [['sysname','chassis','source_ip','interface','lag','port','port_type','queue_group_port','address','isis','mpls','rsvp','slope-policy','egress-scheduler-policy','queue-policy','qos','queue-group']]

        ###############  Template #######################
        template = open(self.arg[2])
        ############# File Processor ##########################
        for filename in self.arg:
            if filename != self.arg[0] and filename != self.arg[1] and filename != self.arg[2] and filename != self.arg[-1]:
                input_file = open(filename, encoding='utf-8')
                raw_text_data = input_file.read()
                input_file.close()

                ############ Call To Parse ################
                re_table = textfsm.TextFSM(template)
                fsm_results = re_table.ParseText(raw_text_data)

                ############ Structure results ############
                count = 0
                success = 0
                interfaces = []
                source_ip = ''
                slope_policy_list = {}
                queue_policy_list = {}
                egress_policy_list = {}
                queue_group_name = {}
                port_types = {}
                mpls_interfaces = []
                rsvp_interfaces = []
                isis = 0
                lag = 0
                port_pr = ''
                isis_list = {}
                lag_ports = {}

                for row in fsm_results:
                    if row[3] != '' and count == 0:
                        source_ip = row[3]
                        count += 1
                    if row[4] != '':
                        interfaces.append({
                            "sysname":row[0],
                            "chassis":row[1],
                            "source_ip":source_ip,
                            "interface":row[4],
                            "port": row[5],
                            'address':row[2],
                            'qos':row[8],
                            'queue-group':row[9],
                        })
                    if row[6] != '':
                        slope_policy_list[row[5]] = row[6]
                    if row[7] != '':
                        queue_policy_list[row[5]] = row[7]
                    if row[10] != '' and row[11] != '':
                        isis = row[10]
                    elif row[11] != '' and row[10] == '':
                        isis_list[row[11]] = isis
                    if row[12] != '':
                        mpls_interfaces.append(row[12])
                    if row[13] != '':
                        rsvp_interfaces.append(row[13])
                    if row[14] != '':
                        lag_ports['lag-'+row[14]]=row[15]
                    if row[16] != '':
                        egress_policy_list[row[5]] = row[16]
                    if row[17] != '':
                        port_types[row[17]] = row[18]
                    if row[19] != '':
                        queue_group_name[row[5]] = row[19]
                for i in interfaces:
                    print(i)
                    port = i["port"] if i["port"] not in lag_ports and 'lag' not in i['port'] else lag_ports[i["port"]]
                    data.append([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["interface"],
                        '' if i["port"] not in lag_ports else i["port"][4:],
                        port,
                        '' if port not in port_types else port_types[port],
                        '' if port not in queue_group_name else queue_group_name[port],
                        i["address"],
                        '' if i['interface'] not in isis_list else isis_list[i['interface']],
                        1 if i["interface"] in mpls_interfaces else 0,
                        1 if i["interface"] in rsvp_interfaces else 0,
                        '' if port not in slope_policy_list else slope_policy_list[port],
                        '' if port not in egress_policy_list else egress_policy_list[port],
                        '' if port not in queue_policy_list else queue_policy_list[port],
                        i["qos"],
                        i["queue-group"]
                    ])
            elif self.arg[-1] == filename:
                myFile = open(filename+'.csv', 'w')
                success = 1

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(data)
            success = 2

        template.close()

        return Get(200,'All files were processed correctly',data)

    def stage5(self):
        # ['0sysname', '1model', '2source_ip', '3l3vpn', '4service_id', '5service_name',
        # '6customer_id', '7interface', '8sap', '9ingress_qos_id', '10egress_qos_id', '11port',
        # '12port_address', '13policy', '14lag_id', '15port_lag', '16card', '17buffer_min', '18buffer_max',
        # '19shutdown', '20resv_min', '21resv_max']
        if len(self.arg) < 5:
            return Get(404,'The arguments are invalid, format: [--stage-5] template [files] output_name',None)
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','sap','ingress_qos_id','egress_qos_id','buffer_min','buffer_max','resv_min','resv_max']]

        ###############  Template #######################
        template = open(self.arg[2])
        ############# File Processor ##########################
        for filename in self.arg:
            if filename != self.arg[0] and filename != self.arg[1] and filename != self.arg[2] and filename != self.arg[-1]:
                input_file = open(filename, encoding='utf-8')
                raw_text_data = input_file.read()
                input_file.close()

                ############ Call To Parse ################
                re_table = textfsm.TextFSM(template)
                fsm_results = re_table.ParseText(raw_text_data)
                ############Vars###########################
                source_ip = ''
                l3vpn = ''
                service_id = ''
                service_name = ''
                customer_id = ''
                l3vpn_list = []
                ports_policys = {}
                lags = {}
                cards = {}
                ############ Structure results ############
                for row in fsm_results:
                    if row[2] != '':
                        source_ip = row[2]
                    if row[3] != '':
                        l3vpn = row[3]
                    if row[4] != '':
                        service_id = row[4]
                    if row[5] != '':
                        service_name = row[5]
                    if row[6] != '':
                        customer_id = row[6]
                    if row[7] != '':
                        l3vpn_list.append({
                            "sysname": row[0],
                            "chassis": row[1],
                            "source_ip": source_ip,
                            "l3vpn": l3vpn,
                            "service_id": service_id,
                            "service_name": service_name,
                            "customer_id": customer_id,
                            "interface": row[7],
                            "sap": row[8],
                            "ingress_qos_id": row[9],
                            "egress_qos_id": row[10],
                        })
                    if row[11] != '':
                        ports_policys[row[11]] = row[13]
                    if row[14] != '':
                        lags[row[14]] = row[15]
                    if row[16] != '' and row[19] != '':
                        cards[row[16]] = {
                            "buffer_min":row[17],
                            "buffer_max":row[18],
                            "shutdown":row[19],
                            "resv_min":row[20],
                            "resv_max":row[21]
                        }
                for i in l3vpn_list:
                    if "lag" not in i["sap"]:
                        port = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                    else:
                        lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                        port = lags[lag]
                    card = '' if port[:1] not in cards else cards[port[:1]]
                    data.append([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["l3vpn"],
                        i["service_id"],
                        i["service_name"],
                        i["customer_id"],
                        i["interface"],
                        port,
                        i["ingress_qos_id"],
                        i["egress_qos_id"],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"]
                    ])
                    print([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["l3vpn"],
                        i["service_id"],
                        i["service_name"],
                        i["customer_id"],
                        i["interface"],
                        port,
                        i["ingress_qos_id"],
                        i["egress_qos_id"],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"]
                    ])
            elif self.arg[-1] == filename:
                myFile = open(filename+'.csv', 'w')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def Stage6(self):
        if len(self.arg) < 5:
            return Get(404,'The arguments are invalid, format: [--stage-6] template [files] output_name',None)
        # ['sysname', 'model', 'source_ip', 'l2vpn', 'service_id',4
        # 'service_name', 'customer_id', 'sap', 'ingress_qos_id',8
        #  'egress_qos_id', 'port', 'port_address', 'policy', 'lag_id',13
        #  'port_lag', 'card','buffer_min', 'buffer_max', 'shutdown', 'resv_min', 'resv_max']20
        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','sap','ingress_qos_id','egress_qos_id','buffer_min','buffer_max','resv_min','resv_max']]

        ###############  Template #######################
        template = open(self.arg[2])
        ############# File Processor ##########################
        for filename in self.arg:
            if filename != self.arg[0] and filename != self.arg[1] and filename != self.arg[2] and filename != self.arg[-1]:
                input_file = open(filename, encoding='utf-8')
                raw_text_data = input_file.read()
                input_file.close()

                ############ Call To Parse ################
                re_table = textfsm.TextFSM(template)
                fsm_results = re_table.ParseText(raw_text_data)
                ############Vars###########################
                source_ip = ''
                l2vpn = ''
                service_id = ''
                service_name = ''
                customer_id = ''
                l2vpn_list = []
                ports_policys = {}
                lags = {}
                cards = {}
                ############ Structure results ############
                for row in fsm_results:
                    if row[2] != '':
                        source_ip = row[2]
                    if row[3] != '':
                        l2vpn = row[3]
                    if row[4] != '':
                        service_id = row[4]
                    if row[5] != '':
                        service_name = row[5]
                    if row[6] != '':
                        customer_id = row[6]
                    if row[7] != '':
                        l2vpn_list.append({
                            "sysname": row[0],
                            "chassis": row[1],
                            "source_ip": source_ip,
                            "l2vpn": l2vpn,
                            "service_id": service_id,
                            "service_name": service_name,
                            "customer_id": customer_id,
                            "sap": row[7],
                            "ingress_qos_id": row[8],
                            "egress_qos_id": row[9],
                        })
                    if row[10] != '':
                        ports_policys[row[10]] = row[12]
                    if row[13] != '':
                        lags[row[13]] = row[14]
                    if row[15] != '' and row[18] != '':
                        cards[row[15]] = {
                            "buffer_min":row[16],
                            "buffer_max":row[17],
                            "shutdown":row[18],
                            "resv_min":row[19],
                            "resv_max":row[20]
                        }
                for i in l2vpn_list:
                    if "lag" not in i["sap"]:
                        sap = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                    else:
                        lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                        sap = lags[lag]
                    card = '' if sap[:1] not in cards else cards[sap[:1]]
                    data.append([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["l2vpn"],
                        i["service_id"],
                        i["service_name"],
                        i["customer_id"],
                        sap,
                        i["ingress_qos_id"],
                        i["egress_qos_id"],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"]
                    ])
                    print([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["l2vpn"],
                        i["service_id"],
                        i["service_name"],
                        i["customer_id"],
                        sap,
                        i["ingress_qos_id"],
                        i["egress_qos_id"],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"]
                    ])
            elif self.arg[-1] == filename:
                myFile = open(filename+'.csv', 'w')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)



if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("The arguments are invalid, format: --stage-1 template [input_files] output_file")
    else:
        this = Nokia(sys.argv)
        if '1' in sys.argv[1] or '2' in sys.argv[1]:
            print(this.stage1().message)
        elif '3' in sys.argv[1]:
            print(this.stage3().message)
        elif '5' in sys.argv[1]:
            print(this.stage5().message)
        elif '6' in sys.argv[1]:
            print(this.stage6().message)
        else:
            print("We can't find this option")
