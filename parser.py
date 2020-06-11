import textfsm
import csv
import sys

class Get(object):
    """
    Docstring for Get.
    This Class is only for send some
    data from methods results.

    Parameters
    ----------
    status : int
        the status code
    message : str
        Healthy status message.
    data : [{'key', 'value'}]
        the results in a list


    Raises
    ------
    KeyError
        When create object whitout params
    """

    def __init__(self, status,message,data):
        super(Get, self).__init__()
        self.data = data
        self.status = status
        self.message = message

class Nokia(object):
    """
    Docstring for Nokia.
    Class to parse nokia devices
    logs basend on stages

    Parameters
    ----------

    console : Bool
        True if client is console, else False

    """

    def __init__(self,console = False):
        super(Nokia, self).__init__()
        self.console = console
    def stage1(self,files,temp):
        """
        Docstring for .stage1(files,templates)
        file Processor for logs in Stage 1

        Parameters
        ----------
        files : [list_of_files]
            the list of files to be processed
        temp : str
            file for template


        Returns
        -------
        object : Get()
            .status  : status code
            .message : Healthy status message
            .data    : Data into a JSON

        Raises
        ------
        KeyError
            When Parameter It's empty
        Status 200
            It's OK
        Status 400
            Something It's wrong
        Status 404
            File not foud
        """
        if len(files) < 1:
            return Get(404,'Files are empty',None)
        data = [['sysname','chassis','source_ip','interface','lag','port','port_type','queue_group_port','address','isis','mpls','rsvp','slope-policy','egress-scheduler-policy','queue-policy','qos','queue-group']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in files:

            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()

            ############ Call To Parse ################
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)

            ############ Structure results ############
            count = 0
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
                    lag_ports['lag-'+row[14]] = row[15]
                if row[16] != '':
                    egress_policy_list[row[5]] = row[16]
                if row[17] != '':
                    port_types[row[17]] = row[18]
                if row[19] != '':
                    queue_group_name[row[5]] = row[19]
            for i in interfaces:
                port = i["port"] if i["port"] not in lag_ports else lag_ports[i['port']]
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
                if console:
                    print(
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
                    )

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_stage_1_2.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def stage5(self,files,temp):
        """
        Docstring for .stage5(files,templates)
        file Processor for logs in Stage 5

        Parameters
        ----------
        files : [list_of_files]
            the list of files to be processed
        temp : str
            file for template


        Returns
        -------
        object : Get()
            .status  : status code
            .message : Healthy status message
            .data    : Data into a JSON

        Raises
        ------
        KeyError
            When Parameter It's empty
        Status 200
            It's OK
        Status 400
            Something It's wrong
        Status 404
            File not foud
        """
        if len(files) < 1:
            return Get(404,'Files are empty',None)
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','sap','ingress_qos_id','egress_qos_id','buffer_min','buffer_max','resv_min','resv_max']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in files:
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
                    port = '' if lag not in lags else lags[lag]
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
                if console:
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

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_stage_5.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def stage6(self,files,temp):
        """
        Docstring for .stage6(files,templates)
        file Processor for logs in Stage 6

        Parameters
        ----------
        files : [list_of_files]
            the list of files to be processed
        temp : str
            file for template


        Returns
        -------
        object : Get()
            .status  : status code
            .message : Healthy status message
            .data    : Data into a JSON

        Raises
        ------
        KeyError
            When Parameter It's empty
        Status 200
            It's OK
        Status 400
            Something It's wrong
        Status 404
            File not foud
        """
        if len(files) < 1:
            return Get(404,'Files are empty',None)
        # ['sysname', 'model', 'source_ip', 'l2vpn', 'service_id',4
        # 'service_name', 'customer_id', 'sap', 'ingress_qos_id',8
        #  'egress_qos_id', 'port', 'port_address', 'policy', 'lag_id',13
        #  'port_lag', 'card','buffer_min', 'buffer_max', 'shutdown', 'resv_min', 'resv_max']20
        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','sap','ingress_qos_id','egress_qos_id','buffer_min','buffer_max','resv_min','resv_max']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in files:
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
                if console:
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
        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_stage_6.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def stage7(self):
        """
        Docstring for .stage7(files,templates)
        file Processor for logs in Stage 7

        Parameters
        ----------
        files : [list_of_files]
            the list of files to be processed
        temp : str
            file for template


        Returns
        -------
        object : Get()
            .status  : status code
            .message : Healthy status message
            .data    : Data into a JSON

        Raises
        ------
        KeyError
            When Parameter It's empty
        Status 200
            It's OK
        Status 400
            Something It's wrong
        Status 404
            File not foud
        """
        if len(files) < 1:
            return Get(404,'Files are empty',None)
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','sap','ingress_qos_id','egress_qos_id','buffer_min','buffer_max','resv_min','resv_max']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in files:
            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()



if __name__ == '__main__':
    console = True
    try:
        files = [i for i in sys.argv if i != sys.argv[0] and i != sys.argv[1] and i != sys.argv[2]]
        template = sys.argv[2]
    except Exception as e:
        print("We cant find params")
    if len(files) == 0:
        print("Files are empty")
    if len(sys.argv) < 4:
        print("The arguments are invalid, format: --stage-x template [input_files]")
    else:
        this = Nokia(console)
        if '1' in sys.argv[1] or '2' in sys.argv[1]:
            print(this.stage1(files,template).message)
        elif '3' in sys.argv[1]:
            print(this.stage3(files,template).message)
        elif '5' in sys.argv[1]:
            print(this.stage5(files,template).message)
        elif '6' in sys.argv[1]:
            print(this.stage6(files,template).message)
        else:
            print("We can't find this option")
