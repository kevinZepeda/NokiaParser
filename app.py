import textfsm
import csv
from tqdm import tqdm
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
    logs basend on scenerys

    Parameters
    ----------

    console : Bool
        True if client is console, else False

    """

    def __init__(self,console = False):
        super(Nokia, self).__init__()
        self.console = console

    def scenery1(self,files,temp):
        """
        Docstring for .scenery1(files,templates)
        file Processor for logs in scenery 1

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
        for filename in tqdm(files):

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
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_1_2.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery3(self,files,temp):
        """
        Docstring for .scenery3(files,templates)
        file Processor for logs in scenery 3

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','bgp','neighbor','sap','ingress_qos_id','egress_qos_id','port','policy','card','buffer_min','buffer_max','resv_min','resv_max','shutdown']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
                if row[7] != '' and row[22] != '':
                    l3vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l3vpn": l3vpn,
                        "service_id": service_id,
                        "service_name": service_name,
                        "customer_id": customer_id,
                        "interface": row[7],
                        "bgp":row[22],
                        "neighbor":row[23],
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
                        "shutdown":row[19] if row[19] != '' else 'shutdown',
                        "resv_min":row[20],
                        "resv_max":row[21]
                    }
            for i in l3vpn_list:
                if "To-NEXTEL" in i["interface"]:
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
                        i["bgp"],
                        i["neighbor"],
                        i['sap'],
                        i["ingress_qos_id"],
                        i["egress_qos_id"],
                        port,
                        '' if port not in ports_policys else ports_policys[port],
                        port[:1],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"],
                        '' if card == '' else card["shutdown"]
                        ])

                    pass
                else:
                    pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_3.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)


    def scenery4(self,files,temp):
        """
        Docstring for .scenery4(files,templates)
        file Processor for logs in scenery 4

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
        for filename in tqdm(files):

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
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_4.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery5(self,files,temp):
        """
        Docstring for .scenery5(files,templates)
        file Processor for logs in scenery 5

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','sap','ingress_qos_id','egress_qos_id','port','policy','card','buffer_min','buffer_max','resv_min','resv_max','shutdown']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
                        "shutdown":row[19] if row[19] != '' else 'shutdown',
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
                    i['sap'],
                    i["ingress_qos_id"],
                    i["egress_qos_id"],
                    port,
                    '' if port not in ports_policys else ports_policys[port],
                    port[:1],
                    '' if card == '' else card["buffer_min"],
                    '' if card == '' else card["buffer_max"],
                    '' if card == '' else card["resv_min"],
                    '' if card == '' else card["resv_max"],
                    '' if card == '' else card["shutdown"]
                ])


        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_5.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery6(self,files,temp):
        """
        Docstring for .scenery6(files,templates)
        file Processor for logs in scenery 6

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
        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','sap','ingress_qos_id','egress_qos_id','port','policy','card','buffer_min','buffer_max','resv_min','resv_max','shutdown']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
                if row[15] != '':
                    cards[row[15]] = {
                        "buffer_min":row[16],
                        "buffer_max":row[17],
                        "shutdown":row[18] if row[18] != '' else 'shutdown',
                        "resv_min":row[19],
                        "resv_max":row[20]
                    }
            for i in l2vpn_list:
                if "lag" not in i["sap"]:
                    sap = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                else:
                    lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                    sap = '' if lag not in lags else lags[lag]
                card = '' if sap[:1] not in cards else cards[sap[:1]]
                data.append([
                    i["sysname"],
                    i["chassis"],
                    i["source_ip"],
                    i["l2vpn"],
                    i["service_id"],
                    i["service_name"],
                    i["customer_id"],
                    i['sap'],
                    i["ingress_qos_id"],
                    i["egress_qos_id"],
                    sap,
                    '' if sap not in ports_policys else ports_policys[sap],
                    sap[:1],
                    '' if card == '' else card["buffer_min"],
                    '' if card == '' else card["buffer_max"],
                    '' if card == '' else card["resv_min"],
                    '' if card == '' else card["resv_max"],
                    '' if card == '' else card["shutdown"]
                    ])

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_6.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery7(self,files,temp):
        """
        Docstring for .scenery7(files,templates)
        file Processor for logs in scenery 7

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
        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','spoke_spd_id','spoke_svc_id','sap','far_end_system_ip','port','policy','card','buffer_min','buffer_max','resv_min','resv_max','shutdown']]
        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()
            ############ Call To Parse ################
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)
            ############Vars###########################4
            source_ip = ''
            l2vpn_list = []
            ports_policys = {}
            sdp_ids = {}
            lags = {}
            cards = {}
            ############ Structure results ############
            # ['sysname', 'model', 'source_ip', 'l2vpn', 'service_id', 'service_name', 'customer_id', 'spoke_spd_id', 'spoke_svc_id', 'sap',
            # 'sdp_id', 'far_end_system_ip',
            # 'port', 'policy',
            # lag_id', 'port_lag'
            # 'card', 'buffer_min', 'buffer_max', 'shutdown', 'resv_min', 'resv_max'
            for row in fsm_results:
                if row[2] != '':
                    source_ip = row[2]
                if row[7] != '' and row[9] != '':
                    l2vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l2vpn": row[3],
                        "service_id": row[4],
                        "service_name": row[5],
                        "customer_id": row[6],
                        "spoke_spd_id": row[7],
                        "spoke_svc_id": row[8],
                        "sap": row[9],
                    })
                if row[10] != '':
                    sdp_ids[row[10]] = row[11]
                if row[12] != '':
                    ports_policys[row[12]] = row[13]
                if row[14] != '':
                    lags[row[14]] = row[15]
                if row[16] != '':
                    cards[row[16]] = {
                        "buffer_min":row[17],
                        "buffer_max":row[18],
                        "shutdown":row[19] if row[19] != '' else 'shutdown',
                        "resv_min":row[20],
                        "resv_max":row[21]
                    }

            for i in l2vpn_list:
                if "lag" not in i["sap"]:
                    sap = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                else:
                    lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                    sap = '' if lag not in lags else lags[lag]
                card = '' if sap[:1] not in cards else cards[sap[:1]]
                data.append([
                    i["sysname"],
                    i["chassis"],
                    i["source_ip"],
                    i["l2vpn"],
                    i["service_id"],
                    i["service_name"],
                    i["customer_id"],
                    i["spoke_spd_id"],
                    i["spoke_svc_id"],
                    i['sap'],
                    '' if i['spoke_spd_id'] not in sdp_ids else sdp_ids[i['spoke_spd_id']],
                    sap,
                    '' if sap not in ports_policys else ports_policys[sap],
                    sap[:1],
                    '' if card == '' else card["buffer_min"],
                    '' if card == '' else card["buffer_max"],
                    '' if card == '' else card["resv_min"],
                    '' if card == '' else card["resv_max"],
                    '' if card == '' else card["shutdown"]
                    ])

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_7.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)


    def scenery8(self,files,temp):
        """
        Docstring for .scenery8(files,templates)
        file Processor for logs in scenery 8

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','vpls','sap','ingress_qos_id','egress_qos_id','port','policy','card','buffer_min','buffer_max','resv_min','resv_max','shutdown']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
            vplss = {}
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
                if row[7] != '' and row[8] != '':
                    l3vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l3vpn": l3vpn,
                        "service_id": service_id,
                        "service_name": service_name,
                        "customer_id": customer_id,
                        "interface": row[7],
                        "vpls": row[8],
                    })
                if row[9] != '':
                    vplss[row[5]] = {
                        "sap":row[9],
                        "ingress": row[10],
                        "egress":row[11]
                    }
                if row[12] != '':
                    ports_policys[row[12]] = row[13]
                if row[14] != '':
                    lags[row[14]] = row[15]
                if row[16] != '':
                    cards[row[16]] = {
                        "buffer_min":row[17],
                        "buffer_max":row[18],
                        "shutdown":row[19] if row[19] != '' else 'shutdown',
                        "resv_min":row[20],
                        "resv_max":row[21]
                    }
            for i in l3vpn_list:
                try:
                    match = vplss[i['vpls']]
                    if "lag" not in match["sap"]:
                        port = match["sap"][:match["sap"].find(":")] if ":" in match["sap"] else match["sap"]
                    else:
                        lag = match["sap"][4:match["sap"].find(":")] if ":" in match["sap"] else match["sap"][4:]
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
                        i['vpls'],
                        match['sap'],
                        match['ingress'],
                        match['egress'],
                        port,
                        '' if port not in ports_policys else ports_policys[port],
                        port[:1],
                        '' if card == '' else card["buffer_min"],
                        '' if card == '' else card["buffer_max"],
                        '' if card == '' else card["resv_min"],
                        '' if card == '' else card["resv_max"],
                        '' if card == '' else card["shutdown"]
                        ])

                except Exception as e:
                    pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_8.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery9(self,files,temp):
        """
        Docstring for .scenery9(files,templates)
        file Processor for logs in scenery 9

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name',
        'customer_id','interface','spoke_spd_id','spoke_svc_id','sap',
        'ingress_qos_id','egress_qos_id','port','policy','card','buffer_min',
        'buffer_max','resv_min','resv_max','shutdown']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
            l2vpn_list = []
            sdp_ids = {}
            ports_policys = {}
            lags = {}
            cards = {}
            ############ Structure results ############
            # ['sysname', 'model', 'source_ip', 'l3vpn', 'service_id', 'service_name', 'customer_id', 'interface', 'spoke_spd_id', 'spoke_svc_id',9
            # 'sap', 'ingress_qos_id', 'egress_qos_id',12
            # 'sdp_id', 'far_end_system_ip' 14
            # 'port', 'policy',16
            # 'lag_id', 'port_lag' 18
            # 'card', 'buffer_min', 'buffer_max', 'shutdown', 'resv_min', 'resv_max'] 24
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
                if row[7] != '' and row[8] != '':
                    l3vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l3vpn": l3vpn,
                        "service_id": service_id,
                        "service_name": service_name,
                        "customer_id": customer_id,
                        "interface": row[7],
                        "spoke_spd_id": row[8],
                        "spoke_svc_id": row[9]
                    })
                if row[10] != '':
                    l2vpn_list.append({
                        "sap":row[10],
                        "ingress":row[11],
                        "egress":row[12],
                        "service_id": service_id
                    })
                if row[13] != '':
                    sdp_ids[row[13]] = row[14]
                if row[15] != '':
                    ports_policys[row[15]] = row[16]
                if row[17] != '':
                    lags[row[17]] = row[18]
                if row[19] != '':
                    cards[row[19]] = {
                        "buffer_min":row[20],
                        "buffer_max":row[21],
                        "shutdown":row[22] if row[22] != '' else 'shutdown',
                        "resv_min":row[23],
                        "resv_max":row[24]
                    }
            if len(l2vpn_list) != 0:
                for i in l3vpn_list:
                    for n in l2vpn_list:
                        if i['spoke_svc_id'] == n['service_id']:
                            if "lag" not in n["sap"]:
                                port = n["sap"][:n["sap"].find(":")] if ":" in n["sap"] else n["sap"]
                            else:
                                lag = n["sap"][4:n["sap"].find(":")] if ":" in n["sap"] else n["sap"][4:]
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
                                i['spoke_spd_id'],
                                i['spoke_svc_id'],
                                n['sap'],
                                n['ingress'],
                                n['egress'],
                                port,
                                '' if port not in ports_policys else ports_policys[port],
                                port[:1],
                                '' if card == '' else card["buffer_min"],
                                '' if card == '' else card["buffer_max"],
                                '' if card == '' else card["resv_min"],
                                '' if card == '' else card["resv_max"],
                                '' if card == '' else card["shutdown"]
                                ])
                            pass
                        else:
                            pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_9.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)



    def scenery10(self,files,temp):
        """
        Docstring for .scenery10(files,templates)
        file Processor for logs in scenery 10

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
        data = [['sysname','chassis','source_ip','interface','lag','port','port_type','address','isis','mpls','rsvp','queue-policy','qos','card','mda','fabric_network','fabric_access']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):

            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()

            ############ Call To Parse ################
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)

            ############ Structure results ############
            interfaces = []
            source_ip = ''
            queue_policy_list = {}
            port_types = {}
            mpls_interfaces = []
            rsvp_interfaces = []
            lag = 0
            isis_list = []
            lag_ports = {}
            card_name = ''
            cards = []
            # ['sysname', 'model', 'address', 'source_ip', 'interface', 'port',5
            # 'queue_policy', 'isis', 'mpls', 'rsvp', 'lag_id', 'port_lag',11
            # 'type_port', 'type', 'card', 'buffer_min', 'buffer_max']16
            for row in fsm_results:
                if row[3] != '':
                    source_ip = row[3]
                if row[4] != '':
                    interfaces.append({
                        "sysname":row[0],
                        "chassis":row[1],
                        "source_ip":source_ip,
                        "interface":row[4],
                        "port": row[5],
                        'address':row[2],
                    })
                if row[6] != '':
                    queue_policy_list[row[5]] = row[6]
                if row[7] != '':
                    isis_list.append(row[7])
                if row[8] != '':
                    mpls_interfaces.append(row[8])
                if row[9] != '':
                    rsvp_interfaces.append(row[9])
                if row[10] != '':
                    lag_ports['lag-'+row[10]] = row[11]
                if row[12] != '':
                    port_types[row[12]] = row[13]
                if row[14] != '':
                    card_name = row[14]
                if row[15] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[15],
                        "network":row[16],
                        "access":row[17]
                    })
            for i in interfaces:
                for card in cards:
                    if i['interface'] in isis_list:
                        port = i["port"] if i["port"] not in lag_ports else lag_ports[i['port']]
                        if port[:1] == card['card']:
                            data.append([
                                i["sysname"],
                                i["chassis"],
                                i["source_ip"],
                                i["interface"],
                                '' if i["port"] not in lag_ports else i["port"][4:],
                                port,
                                '' if port not in port_types else port_types[port],
                                i["address"],
                                0,
                                1 if i["interface"] in mpls_interfaces else 0,
                                1 if i["interface"] in rsvp_interfaces else 0,
                                '' if port not in queue_policy_list else queue_policy_list[port],
                                100,
                                card['card'],
                                card['mda'],
                                card['network'],
                                card['access']
                            ])
                    else:
                        pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_10_11.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)


    def scenery12(self,files,temp):
        """
        Docstring for .scenery12(files,templates)
        file Processor for logs in scenery 12

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','sap','ingress_qos_id','egress_qos_id','port','policy','card','mda','fabric_network','fabric_access']]
        file_list = []
        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):

            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()

            ############ Call To Parse ################
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)

            ############ Structure results ############
            source_ip = ''
            l3vpn = ''
            service_id = ''
            service_name = ''
            customer_id = ''
            l3vpn_list = []
            ports_policys = {}
            lags = {}
            card_name = ''
            cards = []

            # ['sysname', 'model', 'source_ip',2
            #'l3vpn', 'service_id', 'service_name', 'customer_id',6
            #'interface', 'sap', 'ingress_qos_id', 'egress_qos_id',10
            # 'port', 'queue_policy', 'lag_id', 'port_lag',14
            # 'card', 'mda', 'fabric_network', 'fabric_access']18

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
                    ports_policys[row[11]] = row[12]
                if row[13] != '':
                    lags[row[13]] = row[14]
                if row[15] != '':
                    card_name = row[15]
                if row[16] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[16],
                        "network":row[17],
                        "access":row[18]
                    })

            for i in l3vpn_list:
                if "lag" not in i["sap"]:
                    port = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                else:
                    lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                    port = '' if lag not in lags else lags[lag]
                for card in cards:
                    if port[:1] == card['card']:
                        data.append([
                            i["sysname"],
                            i["chassis"],
                            i["source_ip"],
                            i["l3vpn"],
                            i["service_id"],
                            i["service_name"],
                            i["customer_id"],
                            i["interface"],
                            i['sap'],
                            i["ingress_qos_id"],
                            i["egress_qos_id"],
                            port,
                            '' if port not in ports_policys else ports_policys[port],
                            card['card'],
                            card['mda'],
                            card['network'],
                            card['access']
                        ])
                        if filename not in file_list:
                            file_list.append(filename)

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_12.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()
        if console:
            print(file_list)
        return Get(200,'All files were processed correctly',data)

    def scenery13(self,files,temp):
        """
        Docstring for .scenery13(files,templates)
        file Processor for logs in scenery 13

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

        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','sap','ingress_qos_id','egress_qos_id','port','policy','card', 'mda', 'fabric_network', 'fabric_access']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
            card_name = ''
            cards = []
            #['sysname', 'model', 'source_ip',2
            # 'l2vpn', 'service_id', 'service_name', 'customer_id',6
            # 'sap', 'ingress_qos_id', 'egress_qos_id',9
            # 'port', 'queue_policy', 'lag_id', 'port_lag',13
            # 'card', 'mda', 'fabric_network', 'fabric_access']
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
                    ports_policys[row[10]] = row[11]
                if row[12] != '':
                    lags[row[12]] = row[13]
                if row[14] != '':
                    card_name = row[14]
                if row[15] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[15],
                        "network":row[16],
                        "access":row[17]
                    })
            for i in l2vpn_list:
                if "lag" not in i["sap"]:
                    sap = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                else:
                    lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                    sap = '' if lag not in lags else lags[lag]

                for card in cards:
                    if sap[:1] == card['card']:
                        data.append([
                            i["sysname"],
                            i["chassis"],
                            i["source_ip"],
                            i["l2vpn"],
                            i["service_id"],
                            i["service_name"],
                            i["customer_id"],
                            i['sap'],
                            i["ingress_qos_id"],
                            i["egress_qos_id"],
                            sap,
                            '' if sap not in ports_policys else ports_policys[sap],
                            card['card'],
                            card['mda'],
                            card['network'],
                            card['access']
                            ])
        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_13.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery14(self,files,temp):
        """
        Docstring for .scenery14(files,templates)
        file Processor for logs in scenery 14

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
        data = [['sysname','chassis','source_ip','l2vpn','service_id','service_name','customer_id','spoke_spd_id','spoke_svc_id','sap','far_end_system_ip','port','policy','card', 'mda', 'fabric_network', 'fabric_access']]
        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
            input_file = open(filename, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()
            ############ Call To Parse ################
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)
            ############Vars###########################4
            source_ip = ''
            l2vpn_list = []
            ports_policys = {}
            sdp_ids = {}
            lags = {}
            cards = []
            card_name = ''
            ############ Structure results ############
            # ['sysname', 'model', 'source_ip',2
            # 'l2vpn', 'service_id', 'service_name', 'customer_id',6
            # 'spoke_spd_id', 'spoke_svc_id', 'sap', 'sdp_id', 'far_end_system_ip',11
            # 'port', 'policy', 'lag_id', 'port_lag',15
            # 'card', 'mda', 'fabric_network', 'fabric_access']
            for row in fsm_results:
                if row[2] != '':
                    source_ip = row[2]
                if row[7] != '' and row[9] != '':
                    l2vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l2vpn": row[3],
                        "service_id": row[4],
                        "service_name": row[5],
                        "customer_id": row[6],
                        "spoke_spd_id": row[7],
                        "spoke_svc_id": row[8],
                        "sap": row[9],
                    })
                if row[10] != '':
                    sdp_ids[row[10]] = row[11]
                if row[12] != '':
                    ports_policys[row[12]] = row[13]
                if row[14] != '':
                    lags[row[14]] = row[15]
                if row[16] != '':
                    card_name = row[16]
                if row[17] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[17],
                        "network":row[18],
                        "access":row[19]
                    })

            for i in l2vpn_list:
                if "lag" not in i["sap"]:
                    sap = i["sap"][:i["sap"].find(":")] if ":" in i["sap"] else i["sap"]
                else:
                    lag = i["sap"][4:i["sap"].find(":")] if ":" in i["sap"] else i["sap"][4:]
                    sap = '' if lag not in lags else lags[lag]

                for card in cards:
                    if sap[:1] == card['card']:
                        data.append([
                        i["sysname"],
                        i["chassis"],
                        i["source_ip"],
                        i["l2vpn"],
                        i["service_id"],
                        i["service_name"],
                        i["customer_id"],
                        i["spoke_spd_id"],
                        i["spoke_svc_id"],
                        i['sap'],
                        '' if i['spoke_spd_id'] not in sdp_ids else sdp_ids[i['spoke_spd_id']],
                        sap,
                        '' if sap not in ports_policys else ports_policys[sap],
                        card['card'],
                        card['mda'],
                        card['network'],
                        card['access']
                        ])

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_14.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery15(self,files,temp):
        """
        Docstring for .scenery15(files,templates)
        file Processor for logs in scenery 15

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','vpls','sap','ingress_qos_id','egress_qos_id','port','policy','card', 'mda', 'fabric_network', 'fabric_access']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
            vplss = {}
            ports_policys = {}
            lags = {}
            cards = []
            card_name = ''
            ############ Structure results ############
            # ['sysname', 'model', 'source_ip', 2
            # 'l3vpn', 'service_id', 'service_name', 'customer_id', 6
            # 'interface', 'vpls', 'sap', 'ingress_qos_id', 'egress_qos_id', 11
            # 'port', 'queue_policy', 'lag_id', 'port_lag', 15
            # 'card', 'mda', 'fabric_network', 'fabric_access'] 19
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
                if row[7] != '' and row[8] != '':
                    l3vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l3vpn": l3vpn,
                        "service_id": service_id,
                        "service_name": service_name,
                        "customer_id": customer_id,
                        "interface": row[7],
                        "vpls": row[8],
                    })
                if row[9] != '':
                    vplss[row[5]] = {
                        "sap":row[9],
                        "ingress": row[10],
                        "egress":row[11]
                    }
                if row[12] != '':
                    ports_policys[row[12]] = row[13]
                if row[14] != '':
                    lags[row[14]] = row[15]
                if row[16] != '':
                    card_name = row[16]
                if row[17] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[17],
                        "network":row[18],
                        "access":row[19]
                    })
            for i in l3vpn_list:
                try:
                    match = vplss[i['vpls']]
                    if "lag" not in match["sap"]:
                        port = match["sap"][:match["sap"].find(":")] if ":" in match["sap"] else match["sap"]
                    else:
                        lag = match["sap"][4:match["sap"].find(":")] if ":" in match["sap"] else match["sap"][4:]
                        port = '' if lag not in lags else lags[lag]

                    for card in cards:
                        if port[:1] == card['card']:
                            data.append([
                                i["sysname"],
                                i["chassis"],
                                i["source_ip"],
                                i["l3vpn"],
                                i["service_id"],
                                i["service_name"],
                                i["customer_id"],
                                i["interface"],
                                i['vpls'],
                                match['sap'],
                                match['ingress'],
                                match['egress'],
                                port,
                                '' if port not in ports_policys else ports_policys[port],
                                card['card'],
                                card['mda'],
                                card['network'],
                                card['access']
                                ])
                except Exception as e:
                    pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_15.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)

    def scenery16(self,files,temp):
        """
        Docstring for .scenery16(files,templates)
        file Processor for logs in scenery 16

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
        data = [['sysname','chassis','source_ip','l3vpn','service_id','service_name','customer_id','interface','spoke_spd_id','spoke_svc_id','sap','ingress_qos_id','egress_qos_id','port','policy','card', 'mda', 'fabric_network', 'fabric_access']]

        ###############  Template #######################
        template = open(temp)
        ############# File Processor ##########################
        for filename in tqdm(files):
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
            l2vpn_list = []
            sdp_ids = {}
            ports_policys = {}
            lags = {}
            cards = []
            card_name = ''
            ############ Structure results ############
            # ['sysname', 'model', 'source_ip', 'l3vpn', 'service_id', 'service_name', 'customer_id', 'interface', 'spoke_spd_id', 'spoke_svc_id',9
            # 'sap', 'ingress_qos_id', 'egress_qos_id',12
            # 'sdp_id', 'far_end_system_ip' 14
            # 'port', 'policy',16
            # 'lag_id', 'port_lag' 18
            # 'card', 'mda', 'fabric_network', 'fabric_access' 22
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
                if row[7] != '' and row[8] != '':
                    l3vpn_list.append({
                        "sysname": row[0],
                        "chassis": row[1],
                        "source_ip": source_ip,
                        "l3vpn": l3vpn,
                        "service_id": service_id,
                        "service_name": service_name,
                        "customer_id": customer_id,
                        "interface": row[7],
                        "spoke_spd_id": row[8],
                        "spoke_svc_id": row[9]
                    })
                if row[10] != '':
                    l2vpn_list.append({
                        "sap":row[10],
                        "ingress":row[11],
                        "egress":row[12],
                        "service_id": service_id
                    })
                if row[13] != '':
                    sdp_ids[row[13]] = row[14]
                if row[15] != '':
                    ports_policys[row[15]] = row[16]
                if row[17] != '':
                    lags[row[17]] = row[18]
                if row[19] != '':
                    card_name = row[19]
                if row[20] != '':
                    cards.append({
                        "card":card_name,
                        "mda":row[20],
                        "network":row[21],
                        "access":row[22]
                    })
            if len(l2vpn_list) != 0:
                for i in l3vpn_list:
                    for n in l2vpn_list:
                        if i['spoke_svc_id'] == n['service_id']:
                            if "lag" not in n["sap"]:
                                port = n["sap"][:n["sap"].find(":")] if ":" in n["sap"] else n["sap"]
                            else:
                                lag = n["sap"][4:n["sap"].find(":")] if ":" in n["sap"] else n["sap"][4:]
                                port = '' if lag not in lags else lags[lag]

                            for card in cards:
                                if port[:1] == card['card']:
                                    data.append([
                                        i["sysname"],
                                        i["chassis"],
                                        i["source_ip"],
                                        i["l3vpn"],
                                        i["service_id"],
                                        i["service_name"],
                                        i["customer_id"],
                                        i["interface"],
                                        i['spoke_spd_id'],
                                        i['spoke_svc_id'],
                                        n['sap'],
                                        n['ingress'],
                                        n['egress'],
                                        port,
                                        '' if port not in ports_policys else ports_policys[port],
                                        card['card'],
                                        card['mda'],
                                        card['network'],
                                        card['access']
                                        ])
                            pass
                        else:
                            pass

        if console:
            myFile = open('Nokia_'+str(len(files))+'_files_scenery_16.csv', 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data)

        template.close()

        return Get(200,'All files were processed correctly',data)



if __name__ == '__main__':
    console = True
    try:
        files = [i for i in sys.argv if i != sys.argv[0] and i != sys.argv[1]]
        template = sys.argv[1]
    except Exception as e:
        print("We cant find params")
    if len(files) == 0:
        print("Files are empty")
    if len(sys.argv) < 3:
        print("The arguments are invalid, format: template [input_files]")
    else:
        this = Nokia(console)
        if '01.fsm' in sys.argv[1] or '02.fsm' in sys.argv[1]:
            print(this.scenery1(files,template).message)
            # print("End of scenery 1 - 2")
        elif '03' in sys.argv[1]:
            print(this.scenery3(files,template).message)
            # print("End of scenery 3")
        elif '04' in sys.argv[1]:
            print(this.scenery4(files,template).message)
            # print("End of scenery 4")
        elif '05' in sys.argv[1]:
            print(this.scenery5(files,template).message)
            # print("End of scenery 5")
        elif '06' in sys.argv[1]:
            print(this.scenery6(files,template).message)
            # print("End of scenery 6")
        elif '07' in sys.argv[1]:
            print(this.scenery7(files,template).message)
            # print("End of scenery 7")
        elif '08' in sys.argv[1]:
            print(this.scenery8(files,template).message)
            # print("End of scenery 8")
        elif '09' in sys.argv[1]:
            print(this.scenery9(files,template).message)
            # print("End of scenery 9")
        elif '10.fsm' in sys.argv[1]:
            # 10.190.2.148	ROUTER  CellSite	CANTRE-VER7054-AA	7705-SAR8
            # 10.190.2.158	ROUTER  CellSite	PUEMTX-PUE7020-AA	7705-SAR18
            # 10.190.4.138	ROUTER  CellSite	MXPUEXIU0396BHCSRMOB01	7705-SAR8 v2
            print(this.scenery10(files,template).message)
            # print("End of scenery 10")
        elif '11.fsm' in sys.argv[1]:
            print(this.scenery10(files,template).message)
            # print("End of scenery 11")
        elif '12.fsm' in sys.argv[1]:
            print(this.scenery12(files,template).message)
            # print("End of scenery 12")
        elif '13.fsm' in sys.argv[1]:
            print(this.scenery13(files,template).message)
            # print("End of scenery 13")
        elif '14.fsm' in sys.argv[1]:
            print(this.scenery14(files,template).message)
            # print("End of scenery 14")
        elif '15.fsm' in sys.argv[1]:
            print(this.scenery15(files,template).message)
            # print("End of scenery 15")
        elif '16.fsm' in sys.argv[1]:
            print(this.scenery16(files,template).message)
            # print("End of scenery 16")
        elif '17.fsm' in sys.argv[1]:
            print(this.scenery17(files,template).message)
            # print("End of scenery 17")
        else:
            print("We can't find this option or template isn't to this tool")
