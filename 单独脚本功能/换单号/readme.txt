Change_tracking_number_v12.0  ：  

        if shipno.startswith('TH'):
            carrier = 'yanwen'  #燕文
        elif shipno.startswith('LY'):
            carrier = 'china-ems'  #e邮宝
        elif shipno.startswith('YT') or shipno.startswith('TP'):
            carrier = 'yunexpress' # 云途
        elif shipno[0:3]=='420'or shipno[0:2]=='92':
            carrier = 'usps'  #usps
        elif shipno[0:2]=='61':
            shipno = '92'+ shipno #若usps头为61，则头前加92
            carrier = 'usps'  # usps
        elif shipno[0:3] == 'F39':
            carrier = 'flytexpress' #飞特
        elif shipno[0:3] == 'CUS'or shipno[0:3] == 'GCL' or shipno[0:3] == 'USE'or shipno[0:3] == 'SCL':
            carrier = 'ec-firstclass'  #出口易
        elif shipno[0:2] == 'SF':
            carrier = 'sf-express'  #顺丰
        elif shipno[0:3] == 'WNB':
            carrier = 'wanbexpress'  #万邦
        elif shipno[0:3] == '302'or shipno[0:3] == '303':
            carrier = '4px'  #递四方
        elif shipno[0:3] == 'HHW':
            carrier = 'hh-exp'  #华翰
        elif shipno[0:5] == 'TYZPH':
            carrier = 'topyou'  #通邮
        else:
            carrier = '1' #无法识别