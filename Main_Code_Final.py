# https://stackoverflow.com/questions/50807514/kafka-python-consumers-running-in-parallel-threads
# https://stackoverflow.com/questions/50807514/kafka-python-consumers-running-in-parallel-threads
# https://stackoverflow.com/questions/50807514/kafka-python-consumers-running-in-parallel-threads
# Server_Address='you should write your server address'
# Server_Address=Server_Address
# =======================
import multiprocessing
import sys
import threading

# ==== for Show in matplot ====
# from distutils.command.install_data import install_data

import matplotlib
from json import JSONEncoder

from Utils_SUMO import calculate_Avg_CoSimCH, cosineSimilarity, calculate_Avg_CoSimCH_threeElements

matplotlib.use('TkAgg')
# ================

from multiprocessing import Process

from bson.json_util import dumps
from kafka import KafkaProducer, KafkaConsumer, KafkaClient
from bson.json_util import dumps
import json
import random
import datetime
import numpy

from FL_learning import load_minist_data
from sklearn.linear_model import SGDClassifier

# =====
# EPC
# ======
Dic_CH_Coeff = {}

public_topicc = 'public_topic4'


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def preprocess_coeff(coeff):
    try:
        coeff.shape[0]
        return coeff
    except:
        return ''
class vehicle_VIB:
    In_TIMER = 10
    MAX_HOPs = 10
    MAX_Member_CH = 100
    MAX_Member_CM = 10
    SE_TIMER =10
    tedad = 0
    # for Public Topic
    producer = KafkaProducer(bootstrap_servers=[Server_Address])
    consumer = KafkaConsumer(public_topicc, bootstrap_servers=[Server_Address],
                             consumer_timeout_ms=In_TIMER * 1000)

    producer_request_CH = KafkaProducer(bootstrap_servers=[Server_Address])
    producer_respect_CH = KafkaProducer(bootstrap_servers=[Server_Address])

    producer_coeff_to_CH = KafkaProducer(bootstrap_servers=[Server_Address])
    consumer_coeff_from_CH = ''

    producer_coeff_to_CM = KafkaProducer(bootstrap_servers=[Server_Address])
    consumer_coeff_from_CM = ''

    consumer_request_CH = ''
    # producer_respect_CH = ''
    consumer_respect_CH = ''
    # For Request to CM
    producer_request_CM = ''
    consumer_request_CM = ''
    producer_respect_CM = ''
    consumer_respect_CM = ''

    position_x = ''
    position_y = ''
    direction = 'forward'
    velocity = ''
    current_clustering_state = 'SE'
    number_of_hops_to_CH = '0'
    SourceID = ''
    clusteringMetric_averageSpeed = ''
    speed = ''
    SequenceNumeber_dataPacket = ''
    ID_to_CH = '-'
    IDs_from_CH = ''
    TRANMISSION_RANGE = '1000'
    avg_speed = 0
    avg_coeff = 0
    V_state = ''
    vib_neighbor = {}
    Member_CH = 0
    Member_CM = 0
    HOPE_CM = -1
    X_data = ''
    Y_data = ''
    coefficients = ''
    intercept_ = ''
    hello_packet = ''
    list_neighbor_VIB = list()
    Dic_recieve_coeff_in_CH = {}
    mess_resp = {}
    msg_coef = {}
    mess_from_CH = {}
    have_coef=0  # First Time
    msg_request_CH=''
    remain_CH=0
    alpha=0.5
    timer_CM=0
    SourceID_EPC=100
    producer_coeff_to_EPC=''
    neighbor_Avg_CoSimCH={}
    neighbor_Avg_CoSimCM={}
    consumer_EPC=''
    producer_EPC_coeff_to_CH=''
    CH_start=''
    CH_end=''
    list_remain_CH=list()
    def __init__(self, pos_x, pos_y, speed, SourceID,
                 X_data, Y_data, X_data_test, Y_data_test, max_iter,dic_vehicl_times,
                 isEPC,
                 haveClustering):
        self.position_x = pos_x
        self.position_y = pos_y
        self.speed = speed
        self.SourceID = SourceID
        self.avg_speed = speed
        self.V_state = 'SE'
        self.X_data = X_data
        self.Y_data = Y_data
        self.msg_request_CH=''
        self.X_data_test = X_data_test
        self.Y_data_test = Y_data_test
        self.accuracy = 0
        self.have_coef = 0
        self.remain_CH=0
        self.timer_CM=0
        self.sgd_classifier = SGDClassifier(random_state=42, max_iter=max_iter)
        self.sgd_classifier_CH = SGDClassifier(random_state=42, max_iter=max_iter)
        self.dic_vehicl_times=dic_vehicl_times
        self.timeChangePosition=1
        self.producer_coeff_to_EPC= KafkaProducer(bootstrap_servers=[Server_Address])
        self.producer_EPC_coeff_to_CH = KafkaProducer(bootstrap_servers=[Server_Address])
        self.neighbor_Avg_CoSimCH={}
        self.neighbor_Avg_CoSimCM={}
        self.consumer_EPC=''


        if (isEPC=='0'):  # for non-EPC vehicles

            if (haveClustering=='1'):  # for Clustering
                #====
                # Main Algorithm
                #=====
                Main_Algorithm_thread = threading.Thread(target=self.Main_Algorithm)
                # Main_Algorithm_thread = multiprocessing.Process(target=self.Main_Algorithm)
                Main_Algorithm_thread.start()


                CH_CM_RecieveHelloPacket_Thread = threading.Thread(target=self.CH_CM_RecieveHelloPacket)
                # CH_CM_RecieveHelloPacket_Thread = multiprocessing.Process(target=self.CH_CM_RecieveHelloPacket)
                CH_CM_RecieveHelloPacket_Thread.start()


                Join_Request_Thread = threading.Thread(target=self.Join_Request)
                Join_Request_Thread.start()


                Connect_Request_Thread = threading.Thread(target=self.Connect_Request)
                Connect_Request_Thread.start()
                # ====
                # Revieve Hello Packets
                # ===
                # recieve_hello_packet_thread = threading.Thread(target=self.recieve_Hello_packet)
                # recieve_hello_packet_thread.start()
                #
                # time.sleep(1)
                # =======
                # Send Hello Packets
                # =====
                # send_hello_packet_thread = threading.Thread(target=self.send_Hello_packet)
                # send_hello_packet_thread.start()

                # self.recieve_Hello_packet()

                # =============
                # Producer and Consumer for Unicast
                # ============
                # For Request to CH
                # consumer_request_CH_thread = threading.Thread(target=self.recieve_request_CH)
                # consumer_request_CH_thread.start()


                # consumer_recieve_RequestConnectionCH_thread = threading.Thread(target=self.recieve_RequestConnectionCH_)
                # consumer_recieve_RequestConnectionCH_thread.start()


                # remain_CH_thread = threading.Thread(target=self.remain_CH_thread_func)
                # remain_CH_thread.start()

                # =============
                # Producer and Consumer for Coeffient
                # ============
                # consumer_coeff_from_CM_thread = threading.Thread(target=self.recieve_coeff_from_CM)
                # consumer_coeff_from_CM_thread.start()

                # consumer_request_CH = KafkaConsumer('RequestCH_'+str(self.SourceID), bootstrap_servers=[Server_Address])
                # producer_respect_CH = KafkaProducer(bootstrap_servers=[Server_Address])
                # consumer_respect_CH = KafkaConsumer('RespectCH_'+str(self.SourceID), bootstrap_servers=[Server_Address])
                # # For Request to CM
                # producer_request_CM = KafkaProducer(bootstrap_servers=[Server_Address])
                # consumer_request_CM = KafkaConsumer('RequestCM_' + str(self.SourceID), bootstrap_servers=[Server_Address])
                # producer_respect_CM = KafkaProducer(bootstrap_servers=[Server_Address])
                # consumer_respect_CM = KafkaConsumer('RespectCM_' + str(self.SourceID), bootstrap_servers=[Server_Address])



            else:   # No Clustering ...
                NoClustering_HFL_Thread = threading.Thread(target=self.NoClustering_HFL)
                NoClustering_HFL_Thread.start()




        else: # is EPC
            print('is EPC')
            EPC_Thread = threading.Thread(target=self.EPC)
            EPC_Thread.start()
            # pass


    # ---
    def get_accuracy(self):
        # self.sgd_classifier_CH = SGDClassifier(random_state=42)

        self.sgd_classifier_CH.coef_ = self.avg_coeff
        self.sgd_classifier_CH.intercept_ = self.intercept_
        # self.sgd_classifier_CH.fit(self.X_data, self.Y_data)
        try:
            self.sgd_classifier_CH.partial_fit(self.X_data, self.Y_data, classes=numpy.unique(self.Y_data))
            # print('partialFITTT_ACCU')
        except:
            self.sgd_classifier_CH.fit(self.X_data, self.Y_data)
            # self.intercept_=self.sgd_classifier_CH.intercept_

        # print('ACCU===='+ '  '+str(self.sgd_classifier_CH.score(self.X_data_test, self.Y_data_test))+'___ID_CH___'+str(self.SourceID))

        return str(self.sgd_classifier_CH.score(self.X_data_test, self.Y_data_test))

    def recieve_coeff_from_CH(self):

        pass

    def recieve_coeff_from_CM(self):
        wait_recieve_coff_from_CMs = 3

        self.consumer_coeff_from_CM = KafkaConsumer('SendCHCoeff_' + str(self.SourceID),
                                                    bootstrap_servers=[Server_Address])
        round_time = 1
        # ================================*********************=====================
        self.Dic_recieve_coeff_in_CH = {}
        #
        # ================================*********************=====================

        while (True):
            # #===============
            # self.Dic_recieve_coeff_in_CH = {}
            # #================

            # time.sleep(1)
            msg_coff_ch = self.consumer_coeff_from_CM.poll(
                timeout_ms=wait_recieve_coff_from_CMs * 1000)  # wait from now to timeout_ms for recieving all messages within time
            if not msg_coff_ch:
                ''
            else:
                sum_coeff = 0
                self.tedad = 0
                list_CMs_Source_IDs = list()
                for topic_data, consumer_records in msg_coff_ch.items():  # All messages
                    for message in consumer_records:  # each message
                        mess_coeff_ch = json.loads(message.value)

                        if (mess_coeff_ch['SourceID'] not in self.Dic_recieve_coeff_in_CH.keys()):
                            self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']] = {}
                            self.tedad = self.tedad + 1
                        self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']]['coefficients'] = mess_coeff_ch[
                            'coefficients']
                        self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']]['intercept_'] = mess_coeff_ch[
                            'intercept_']

                        #
                        # if (sum_coeff==0):
                        #     sum_coeff = mess['coefficients']
                        #     print('nodeCM_'+mess['SourceID']+'__sendCoefficientsTo___'+'nodeCH_'+self.SourceID+'__IN_RoundTIme'+str(round_time))
                        #     # print(str(self.SourceID) + '_______' + 'multi')
                        #
                        #
                        # else:
                        #     print('nodeCM_' + mess['SourceID'] + '__sendCoefficientsTo___' + 'nodeCH_' + self.SourceID+'__IN_RoundTIme'+str(round_time))
                        #     sum_coeff=sum_coeff+mess['coefficients']
                        #     # print(str(self.SourceID)+'_______'+'multi')

                        list_CMs_Source_IDs.append(mess_coeff_ch['SourceID'])

                round_time = round_time + 1
                # === Average Coefficients===
                # tmp=numpy.asarray(sum_coeff)/tedad
                # if (self.avg_coeff!=tmp):
                #     print('YYESSSS')
                sum_coeff = 0
                sum_inter = 0
                for agent in self.Dic_recieve_coeff_in_CH.keys():
                    try:
                        sum_coeff = sum_coeff + numpy.array(self.Dic_recieve_coeff_in_CH[agent]['coefficients'])
                        sum_inter = sum_inter + numpy.array(self.Dic_recieve_coeff_in_CH[agent]['intercept_'])

                    except:
                        sum_coeff = numpy.array(self.Dic_recieve_coeff_in_CH[agent]['coefficients'])
                        sum_inter = numpy.array(self.Dic_recieve_coeff_in_CH[agent]['intercept_'])

                self.avg_coeff = numpy.asarray(sum_coeff) / len(self.Dic_recieve_coeff_in_CH.keys())
                self.intercept_ = numpy.asarray(sum_inter) / len(self.Dic_recieve_coeff_in_CH.keys())
                strr = ''
                for i in self.Dic_recieve_coeff_in_CH.keys():
                    strr = strr + ',' + str(i)
                # print('tedaddd===== '+'==IN_CH_'+str(self.SourceID)+'____'+str(len(self.Dic_recieve_coeff_in_CH.keys()))+
                #       strr)
                # if (self.tedad>1):
                #     print('tedad_ziaddd')
                self.accuracy = self.get_accuracy()  # calculate accuracy in CH node

                # ===
                # EPC (Set Coeff Parameters)
                # ===
                if (self.SourceID not in Dic_CH_Coeff.keys()):
                    Dic_CH_Coeff[self.SourceID] = {}
                Dic_CH_Coeff[self.SourceID]['avg_coeff'] = self.avg_coeff
                Dic_CH_Coeff[self.SourceID]['intercept_'] = self.intercept_
                # =====

                self.hello_packet['coefficients'] = preprocess_coeff(self.avg_coeff)

                self.hello_packet['intercept_'] = preprocess_coeff(self.intercept_)
                # Covnert to list (np.asarray(a)/2).tolist()

                # === send back to CMs
                for CM_ID in list_CMs_Source_IDs:
                    self.hello_packet['coefficients'] = preprocess_coeff(self.avg_coeff)
                    self.hello_packet['intercept_'] =preprocess_coeff(self.intercept_)
                    # print('sendCoeff_'+'From_'+str(CM_ID)+)
                    time.sleep(2)
                    try:
                        self.producer_coeff_to_CM.send('RecieveCHCoeff_' + str(CM_ID),
                                                       value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))
                    except:
                        print('Error in producer_coeff_to_CM')
                        continue

                # print(str(self.SourceID)+'______'+'get_multiple_coeff')
            # pass

    # ====
    def remain_CH_thread_func(self):
        while(True):
            time.sleep(30)
            if self.remain_CH==0:
                print('Modify CH_State___' + str(self.SourceID))
                # ====
                self.V_state = 'SE'
                self.ID_to_CH = ''
                # ====
            else:
                self.remain_CH = 0


    def Join_Request(self):
        while(True):
            try:
                self.consumer_request_CH = KafkaConsumer('Join_Request_' + str(self.SourceID),
                                                         bootstrap_servers=[Server_Address])

                #========
                for message in self.consumer_request_CH :  # each message
                    if (
                            self.Member_CH <= self.MAX_Member_CH):
                        ## self.Member_CH = self.Member_CH + 1
                        self.hello_packet = self.create_Hello_packet()
                        time.sleep(3)
                        try:
                            self.producer_respect_CH.send('Join_Response_' + str(json.loads(message.value)['SourceID']),
                                                      value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'),
                                                          )
                        except:
                            print('Error Created for producer_respect_CH')
                            continue
                        self.remain_CH=1
            except:
                continue


    def Connect_Request(self):
        # while(True):/
        #     try:
        self.consumer_request_CH = KafkaConsumer('Connect_Request_' + str(self.SourceID),
                                                 bootstrap_servers=[Server_Address])

        # ========
        for message in self.consumer_request_CH:  # each message
            if (
                    self.Member_CH <= self.MAX_Member_CH):
                ## self.Member_CH = self.Member_CH + 1
                self.hello_packet = self.create_Hello_packet()
                time.sleep(3)
                try:
                    self.producer_respect_CH.send('Connect_Response_' + str(json.loads(message.value)['SourceID']),
                                                  value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'),
                                                  )
                except:
                    print('Error Created for producer_respect_CH')
                    continue
                self.remain_CH = 1

    # =====

    def create_Hello_packet(self):
        self.hello_packet = {}
        self.hello_packet['direction'] = self.direction
        self.hello_packet['velocity'] = self.velocity
        self.hello_packet['current_clustering_state'] = self.current_clustering_state
        self.hello_packet['number_of_hops_to_CH'] = self.number_of_hops_to_CH
        self.hello_packet['ID_to_CH'] = self.ID_to_CH
        self.hello_packet['speed'] = self.speed
        self.hello_packet['avg_speed'] = self.avg_speed
        self.hello_packet['SourceID'] = self.SourceID
        self.hello_packet['position_x'] = self.position_x
        self.hello_packet['position_y'] = self.position_y
        self.hello_packet['timestamp'] = str(datetime.datetime.now())
        self.hello_packet['V_state'] = self.V_state
        self.hello_packet['HOPE_CM'] = self.HOPE_CM
        self.hello_packet['Member_CM'] = self.Member_CM
        self.hello_packet['Member_CH'] = self.Member_CH
        self.hello_packet['coefficients'] = preprocess_coeff(self.coefficients)
        self.hello_packet['intercept_'] = preprocess_coeff(self.intercept_)
        return self.hello_packet

    def Train_Update_local_SGD(self):
        # Use Stochastic Gradient Descent(SGD) classifier for fit and prediction\
        try:
            self.X_data = numpy.asarray(self.X_data)
            self.Y_data = numpy.asarray(self.Y_data)
            self.sgd_classifier.coef_ = self.coefficients
            self.sgd_classifier.intercept_ = self.intercept_
            try:
                self.sgd_classifier.partial_fit(self.X_data, self.Y_data)
                # print('partialFITTT_TRAINN')
            except:
                self.sgd_classifier.fit(self.X_data, self.Y_data)

            # sgd_classifier.partial_fit(X_train_data, Y_data, classes=numpy.unique(Y_data))
            self.coefficients = self.sgd_classifier.coef_
            self.intercept_ = self.sgd_classifier.intercept_
        except Exception as e:
            # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            # print('error FLLL training')
            ''
        # return sgd_classifier, coefficients, intercept_

    def Train_sendCoeff(self):
        # self.have_coef = 0
        while (True):
            try:

                # #========
                # # Check if not CM else more
                # #=======
                # if (self.V_state!='CM'):
                #     break

                #==================

                if (self.have_coef == 0):  # for First Time
                    self.coefficients = self.mess_resp['coefficients']  # get coefficients from CH
                    self.intercept_ = self.mess_resp['intercept_']  # get coefficients from CH

                self.Train_Update_local_SGD()
                # print(self.SourceID + '___' + ' Finished Training')
                self.hello_packet = self.create_Hello_packet()


                # print('SendCHCoeff_'+'to__'+str(neighbor))

                # ==== Get Coeff from CH===
                self.consumer_coeff_from_CH = KafkaConsumer('RecieveCHCoeff_' + str(self.SourceID),
                                                            bootstrap_servers=[
                                                                Server_Address])
                self.producer_coeff_to_CH.send('SendCHCoeff_' + str(self.ID_to_CH),
                                               value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))

                self.msg_coef = self.consumer_coeff_from_CH.poll(timeout_ms=20 * 1000)
                if not self.msg_coef:
                    # print('Not Recieve Coeff from CH')
                    ''
                else:
                    for topic_data, consumer_records in self.msg_coef.items():
                        for message in consumer_records:  # each message

                            self.mess_from_CH = json.loads(message.value)
                            # print('nodeCM_' + self.SourceID+ '__recieveCoefficientsFrom___' + 'nodeCH_' + mess_from_CH['SourceID'])

                            # ????????????????????????????????????????????????????
                            # ????????????????????????????????????????????????????
                            # ????????????????????????????????????????????????????
                            try:
                                self.hello_packet['coefficients'] = numpy.asarray(self.mess_from_CH['coefficients'])
                                self.hello_packet['intercept_'] = numpy.asarray(self.mess_from_CH['intercept_'])
                            except:
                                continue
                            # ????????????????????????????????????????????????????
                            # ????????????????????????????????????????????????????
                            # ????????????????????????????????????????????????????

                            # print('gett')
                            self.coefficients = numpy.asarray(self.mess_from_CH['coefficients'])
                            self.intercept_ = numpy.asarray(self.mess_from_CH['intercept_'])
                            self.have_coef = 1

                            #====
                            print('EXITTTT')
                            return 1
                            #====
                # return 1
                time.sleep(5)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                print('error training')




    def SE_Algorithm_OLD(self):
        #===================
        # Algorithm 2 (1 - 17)
        #====================
        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CH'):  # for all CH in vib
                # self.vib_neighbor[mess['SourceID']]['TRY_CONNECT_CH'] = 0
                if (self.vib_neighbor[neighbor]['TRY_CONNECT_CH'] == 0):
                    if (int(self.vib_neighbor[neighbor]['Member_CH']) <= int(self.MAX_Member_CH)):
                        # send Join_REQ
                        Join_Timer = 5
                        self.hello_packet = self.create_Hello_packet()
                        self.consumer_respect_CH = KafkaConsumer('RespectCH_' + str(self.SourceID),
                                                                 bootstrap_servers=[Server_Address]
                                                                 )
                        # self.consumer_respect_CH = KafkaConsumer('RespectCH_' + str(self.SourceID),
                        #                                          bootstrap_servers=[Server_Address])
                        # print('listern ==== '+'RespectCH_' + str(self.SourceID))

                        self.producer_request_CH.send('RequestCH_' + str(neighbor),
                                                      value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))

                        msg_respect = self.consumer_respect_CH.poll(
                            timeout_ms=Join_Timer * 1000)  # wait for JoinTimer (for first msg)
                        # msg = self.consumer_respect_CH.poll()  #wait for JoinTimer (for first msg)
                        if not msg_respect:
                            # print('No response from the correspinding CH')
                            ''
                        else:
                            for topic_data, consumer_records in msg_respect.items():
                                message_resp = consumer_records[
                                    0].value  # only one message is served!!! consumer_records[0]
                                mess_resp = json.loads(message_resp)
                                # print('sad')
                                # print('==================================')
                                # print('node_CM_' + self.SourceID + ' -----> ' + 'node_CH_' + str(neighbor))
                                # print('==================================')

                                self.ID_to_CH = str(neighbor)
                                if (self.V_state == 'SE'):  # vase vare avall hast ke miad!
                                    self.V_state = 'CM'
                                self.mess_resp = mess_resp
                                return 1
                        ######
                        #####
                        #######

                    self.vib_neighbor[neighbor]['TRY_CONNECT_CH'] = 1

        #=====
        if (self.V_state=='CM'):
            print('Modify CM_State___'+str(self.SourceID))
            #====
            self.V_state = 'SE'
            self.ID_to_CH = ''
            self.have_coef = 0
            #====
        #============
        return 0  # exit from SE_Algorithm(self)
        # if CE in VIB : ...




    def SA_State_CMsection(self):
        #===================
        # Algorithm 2 (18 - 34)  # ******** Connect CM to another CM  ********
        #====================
        connectionCM_neighbor = {}
        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CM'):
                connectionCM_neighbor[neighbor]=False

        neighbor_Avg_CoSimCM={}
        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CM'):  # for all CM in vib
                if (connectionCM_neighbor[neighbor]==False and self.HOPE_CM< (self.MAX_HOPs-1)):
                    # send Join_REQ
                    Join_Timer = 10
                    self.hello_packet = self.create_Hello_packet()
                    self.consumer_respect_CH = KafkaConsumer('Join_Response_' + str(self.SourceID),
                                                             bootstrap_servers=[Server_Address]
                                                             )

                    self.producer_request_CH.send('Join_Request_' + str(neighbor),
                                                  value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))

                    msg_respect = self.consumer_respect_CH.poll(timeout_ms=Join_Timer * 1000)  # wait for JoinTimer (for first msg)
                    if not msg_respect:
                        # print('No response from the correspinding CH')
                        ''
                    else:   # Join_Response recieved
                        for topic_data, consumer_records in msg_respect.items():
                            message_resp = consumer_records[0].value  # only one message is served!!! consumer_records[0]
                            self.mess_resp=''
                            self.mess_resp = json.loads(message_resp)
                            #=========================
                            # calculate Avg_CoSimCH  (Select best CH for connect!)
                            #====================
                            # mess_resp['coefficients']
                            speedCM=self.mess_resp['speed']
                            speedK=self.speed
                            thetaCM=self.mess_resp['coefficients']
                            thetaK=self.coefficients
                            Avg_CoSimCM=calculate_Avg_CoSimCH(self.alpha, speedCM, speedK, thetaCM, thetaK)
                            self.vib_neighbor[neighbor]['Avg_CoSimCM']=Avg_CoSimCM
                            connectionCM_neighbor[neighbor]=True
                            neighbor_Avg_CoSimCM[neighbor]=Avg_CoSimCM

        neighbor_Avg_CoSimCM=dict(sorted(neighbor_Avg_CoSimCM.items(), key=lambda item: item[1]))

        #=============
        # Connect to best CM (with HOP)
        #=====================
        for neighbor in self.neighbor_Avg_CoSimCM.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CM'):  # for all CM in vib
                if (connectionCM_neighbor[neighbor]==True):
                    self.consumer_respect_CH = KafkaConsumer('Connect_Response_' + str(self.SourceID),
                                                             bootstrap_servers=[Server_Address])

                    self.producer_request_CH.send('Connect_Request_' + str(neighbor),
                                                  value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))
                    msg_respect = self.consumer_respect_CH.poll(timeout_ms=Join_Timer * 1000)
                    if not msg_respect:
                        ''
                    else:  # Connect_Response recieved
                        for topic_data, consumer_records in msg_respect.items():
                            message_resp = consumer_records[0].value  # only one message is served!!! consumer_records[0]
                            mess_resp = json.loads(message_resp)

                            #================
                            # Connect to (best) CH
                            #============
                            # self.ID_to_CH = str(neighbor)
                            self.ID_to_CM =mess_resp['SourceID']
                            if (self.V_state == 'SE'):
                                self.V_state = 'CM'
                            self.mess_resp = mess_resp
                            return 1
                    ######
                    #####
                    #######
                else:
                    connectionCM_neighbor[neighbor] = False
        return 0

    def SA_State_CHsection(self):

        # ===================
        # Algorithm 2 (1 - 17)
        # ====================
        connectionCH_neighbor = {}
        for neighbor in self.vib_neighbor.keys():
            connectionCH_neighbor[neighbor] = False
        # neighbor_Avg_CoSimCH = {}

        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CH'):  # for all CH in vib
                if (connectionCH_neighbor[neighbor] == False):
                    # send Join_REQ
                    Join_Timer = 5
                    self.hello_packet = self.create_Hello_packet()
                    self.consumer_respect_CH = KafkaConsumer('Join_Response_' + str(self.SourceID),
                                                             bootstrap_servers=[Server_Address]
                                                             )

                    self.producer_request_CH.send('Join_Request_' + str(neighbor),
                                                  value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'))

                    msg_respect = self.consumer_respect_CH.poll(
                        timeout_ms=Join_Timer * 1000)  # wait for JoinTimer (for first msg)
                    if not msg_respect:
                        # print('No response from the correspinding CH')
                        ''
                    else:  # Join_Response recieved
                        for topic_data, consumer_records in msg_respect.items():
                            message_resp = consumer_records[0].value  # only one message is served!!! consumer_records[0]
                            self.mess_resp = ''
                            self.mess_resp = json.loads(message_resp)
                            # =========================
                            # calculate Avg_CoSimCH  (Select best CH for connect!)
                            # ====================
                            # mess_resp['coefficients']
                            speedCH = self.mess_resp['speed']
                            speedK = self.speed
                            # thetaCH=self.vib_neighbor[neighbor]['coefficients']
                            thetaCH = self.mess_resp['coefficients']
                            thetaK = self.coefficients
                            Avg_CoSimCH = calculate_Avg_CoSimCH(self.alpha, speedCH, speedK, thetaCH, thetaK)
                            self.vib_neighbor[neighbor]['Avg_CoSimCH'] = Avg_CoSimCH
                            connectionCH_neighbor[neighbor] = True
                            self.neighbor_Avg_CoSimCH[neighbor] = Avg_CoSimCH

        self.neighbor_Avg_CoSimCH = dict(sorted(self.neighbor_Avg_CoSimCH.items(), key=lambda item: item[1]))

        # =============
        # Connect to best CH
        # =====================
        for neighbor in self.neighbor_Avg_CoSimCH.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CH'):  # for all CH in vib
                if (connectionCH_neighbor[neighbor] == True):
                    self.consumer_respect_CH = KafkaConsumer('Connect_Response_' + str(self.SourceID),
                                                             bootstrap_servers=[Server_Address])

                    self.producer_request_CH.send('Connect_Request_' + str(neighbor),
                                                  value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'))
                    msg_respect = self.consumer_respect_CH.poll(timeout_ms=Join_Timer * 1000)
                    if not msg_respect:
                        ''
                    else:  # Connect_Response recieved
                        for topic_data, consumer_records in msg_respect.items():
                            message_resp = consumer_records[0].value  # only one message is served!!! consumer_records[0]
                            mess_resp = json.loads(message_resp)

                            # ================
                            # Connect to (best) CH
                            # ============
                            # self.ID_to_CH = str(neighbor)
                            self.ID_to_CH = mess_resp['SourceID']
                            if (self.V_state == 'SE'):
                                self.V_state = 'CM'
                            self.mess_resp = mess_resp
                            return 1
                    ######
                    #####
                    #######
                else:
                    connectionCH_neighbor[neighbor] = False
        return 0
    def SA_State_SEsection(self):
        neighbor_Avg_CoSimSE={}
        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'SE'):  # for all CH in vib
               
               thetaSE_t=self.vib_neighbor[neighbor]['coefficients']
               thetaSE_t_1=self.coefficients

               left_sum = self.alpha * (self.vib_neighbor[neighbor]['avg_speed'])
               right_sum = (1 - float(self.alpha)) * (1 - float(cosineSimilarity(thetaSE_t,thetaSE_t_1)))
               
               # sum = left_sum + right_sum
               sum = left_sum
               neighbor_Avg_CoSimSE[neighbor] = sum

        thetaSE_k = self.coefficients
        thetaSE_k_1 = self.coefficients
        left_sum = self.alpha * self.avg_speed
        # right_sum = (1 - self.alpha) * (1 - cosineSimilarity(thetaSE_t, thetaSE_t_1))
        sum_k= left_sum
        try:
            min_neighbor_Avg_CoSimSE=min(list(neighbor_Avg_CoSimSE.values()))
            if (sum_k<=min_neighbor_Avg_CoSimSE):
                self.V_state='CH'
        except:
            ''


    def SE_Algorithm(self):
        pass
        #
        # self.SA_State_CHsection()
        # #=====
        # # dar sorati ke hich node (CH) javabi nadahad!  (ertebat ghat shavad!!!)
        # # Algorithm (18 - 34)
        # #====
        #
        # self.SA_State_CMsection()
        #
        # self.SA_State_SEsection()





        #
        # if (self.V_state=='CM'):
        #     print('Modify CM_State___'+str(self.SourceID))
        #     #====
        #     self.V_state = 'SE'
        #     self.ID_to_CH = ''
        #     self.have_coef = 0
        #     #====
        # #============
        # return 0  # exit from SE_Algorithm(self)
        # # if CE in VIB : ...

    def send_Hello_packet(self):
        # dar ghesmate Send_Hello_packet ===> ma darim position ra taghir midim!!!!!!


        # self.hello_packet['speed'] = self.speed
        # self.hello_packet['avg_speed'] = self.avg_speed
        # self.hello_packet['SourceID'] = self.SourceID
        # self.hello_packet['position_x'] = self.position_x
        # self.hello_packet['position_y'] = self.position_y

        while (True):
            try:
                rnd = random.randint(1, 4)
                time.sleep(rnd)

                #=======================
                # Change position base on SUMO simulation!!!!!!!!!!
                #=============================
                try:
                    self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]
                    self.position_x =float(self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]['x'])
                    self.position_y=float(self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]['y'])
                    self.timeChangePosition=self.timeChangePosition+1
                except:
                    print('')
                    ''
                #===============================================

                self.hello_packet = self.create_Hello_packet()
                try:
                    self.hello_packet['coefficients'].shape[0]
                except:
                    self.hello_packet['coefficients']=''




                #=============
                self.producer.send(public_topicc, value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'))




            except:
                continue


    def recieve_RequestCM(self):
        # print('asd')
        pass




    def recieve_Hello_packet(self):   #  ======= MAIN function ======
        self.consumer = KafkaConsumer(public_topicc, bootstrap_servers=[Server_Address],
                                      consumer_timeout_ms=self.In_TIMER * 1000)
        while (True):
            time1 = datetime.datetime.now()
            # ====
            self.vib_neighbor = {}
            while True:
                try:
                    date2 = datetime.datetime.now()
                    #=====================
                    # if ((date2 - time1).seconds > self.In_TIMER):
                    #     self.consumer = KafkaConsumer(public_topicc, bootstrap_servers=[Server_Address],
                    #                                   consumer_timeout_ms=self.In_TIMER * 1000)
                    #     break
                    self.consumer = KafkaConsumer(public_topicc, bootstrap_servers=[Server_Address])
                    #====================================
                    msg = self.consumer.poll(self.In_TIMER * 1000)
                    if not msg:
                        time.sleep(0.1)
                        continue



                    for topic_data, consumer_records in  msg.items():
                        # for message in self.consumer:
                        for message in consumer_records:  # each message
                            #message = message.value
                            mess = json.loads(message.value)
                            # print(self.SourceID + '<--' + mess['SourceID'] + '--->' + '_Direction_' + mess['direction'] + '  ' +
                            #       mess['timestamp'])
                            if (mess['SourceID']==self.SourceID):
                                continue

                            #=======

                            # ==== Insert vib_neighbor
                            # check is neighbor or NOT!
                            # print(self.SourceID + '----'+mess['SourceID'])
                            point1 = numpy.array((self.position_x, self.position_y))
                            point2 = numpy.array((mess['position_x'], mess['position_y']))
                            distance = float(numpy.linalg.norm(point1 - point2))
                            # if (distance>0):
                            #     print('good')
                            if (float(distance) <= float(self.TRANMISSION_RANGE)):  # is Neighbor
                                if (mess['SourceID'] not in self.vib_neighbor.keys()):
                                    self.vib_neighbor[mess['SourceID']] = {}
                                    self.vib_neighbor[mess['SourceID']]['direction'] = mess['direction']
                                    self.vib_neighbor[mess['SourceID']]['speed'] = mess['speed']
                                    self.vib_neighbor[mess['SourceID']]['number_of_hops_to_CH'] = mess[
                                        'number_of_hops_to_CH']
                                    self.vib_neighbor[mess['SourceID']]['current_clustering_state'] = mess[
                                        'current_clustering_state']
                                    self.vib_neighbor[mess['SourceID']]['distance'] = distance
                                    self.vib_neighbor[mess['SourceID']]['SourceID'] = mess['SourceID']
                                    self.vib_neighbor[mess['SourceID']]['avg_speed'] = float(mess['avg_speed'])
                                    self.vib_neighbor[mess['SourceID']]['V_state'] = str(mess['V_state'])
                                    self.vib_neighbor[mess['SourceID']]['TRY_CONNECT_CH'] = 0
                                    self.vib_neighbor[mess['SourceID']]['HOPE_CM'] = str(mess['HOPE_CM'])
                                    self.vib_neighbor[mess['SourceID']]['Member_CM'] = str(mess['Member_CM'])
                                    self.vib_neighbor[mess['SourceID']]['Member_CH'] = str(mess['Member_CH'])
                                else:  #(Update VIB neighbors)
                                    self.vib_neighbor[mess['SourceID']]['direction'] = mess['direction']
                                    self.vib_neighbor[mess['SourceID']]['speed'] = mess['speed']
                                    self.vib_neighbor[mess['SourceID']]['number_of_hops_to_CH'] = mess[
                                        'number_of_hops_to_CH']
                                    self.vib_neighbor[mess['SourceID']]['current_clustering_state'] = mess[
                                        'current_clustering_state']
                                    self.vib_neighbor[mess['SourceID']]['distance'] = distance
                                    self.vib_neighbor[mess['SourceID']]['SourceID'] = mess['SourceID']
                                    self.vib_neighbor[mess['SourceID']]['avg_speed'] = float(mess['avg_speed'])
                                    self.vib_neighbor[mess['SourceID']]['V_state'] = str(mess['V_state'])
                                    # self.vib_neighbor[mess['SourceID']]['TRY_CONNECT_CH']=0
                                    self.vib_neighbor[mess['SourceID']]['HOPE_CM'] = str(mess['HOPE_CM'])
                                    self.vib_neighbor[mess['SourceID']]['Member_CM'] = str(mess['Member_CM'])
                                    self.vib_neighbor[mess['SourceID']]['Member_CH'] = str(mess['Member_CH'])

                    break

                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                    time.sleep(0.1)
                    continue


            # ====
            # speed avg (For IN-TIMER recieved hello_packet)
            # =====
            sum_minus_speed = 0
            N_i = 0
            if (len(list(self.vib_neighbor.keys())) > 1):
                # print('asd')
                ''

            for neigh in self.vib_neighbor.keys():
                if (self.vib_neighbor[neigh]['direction'] == self.direction):  # dar yek direction bashad!!!
                    if (int(self.vib_neighbor[neigh]['number_of_hops_to_CH']) <= self.MAX_HOPs):  # within MAX_HOP
                        N_i = N_i + 1
                        speed_i = self.speed
                        speed_ij = self.vib_neighbor[neigh]['speed']
                        minus_speed = numpy.abs(speed_i - speed_ij)
                        sum_minus_speed = sum_minus_speed + minus_speed

            if (N_i != 0):
                self.avg_speed = sum_minus_speed / N_i
            else:
                self.avg_speed = self.speed

    def CH_HFL(self):
        t_Collect=0
        wait_recieve_coff_from_CMs = 3
        self.consumer_coeff_from_CM = KafkaConsumer('SendCHCoeff_' + str(self.SourceID),
                                                    bootstrap_servers=[Server_Address])
        round_time = 1
        # ================================*********************=====================
        self.Dic_recieve_coeff_in_CH = {}
        list_CMs_Source_IDs = list()
        # ================================*********************=====================
        # while (True):
        # #===============
        # self.Dic_recieve_coeff_in_CH = {}   # hazf mikonim : choon mikhaim coefficient haye node haye ghabli ra ham dashte bashim!!! (train kamel dashte bashim!)
        # #================

        # time.sleep(1)   # yek time.sleep(1) gharar dadim ke syncchronization dorost anjam shavad!!!
        msg_coff_ch = self.consumer_coeff_from_CM.poll(timeout_ms=wait_recieve_coff_from_CMs * 1000)  # wait from now to timeout_ms for recieving all messages within time
        if not msg_coff_ch:
            ''
        else:
            sum_coeff = 0
            self.tedad = 0

            for topic_data, consumer_records in msg_coff_ch.items():  # All messages
                for message in consumer_records:  # each message
                    mess_coeff_ch = json.loads(message.value)

                    if (mess_coeff_ch['SourceID'] not in self.Dic_recieve_coeff_in_CH.keys()):
                        self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']] = {}
                        self.tedad = self.tedad + 1
                    self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']]['coefficients'] = mess_coeff_ch[
                        'coefficients']
                    self.Dic_recieve_coeff_in_CH[mess_coeff_ch['SourceID']]['intercept_'] = mess_coeff_ch[
                        'intercept_']

                    list_CMs_Source_IDs.append(mess_coeff_ch['SourceID'])

            round_time = round_time + 1
            # === Average Coefficients===
            sum_coeff = 0
            sum_inter = 0
            for agent in self.Dic_recieve_coeff_in_CH.keys():
                try:
                    sum_coeff = sum_coeff + numpy.array(self.Dic_recieve_coeff_in_CH[agent]['coefficients'])
                    sum_inter = sum_inter + numpy.array(self.Dic_recieve_coeff_in_CH[agent]['intercept_'])

                except:
                    sum_coeff = numpy.array(self.Dic_recieve_coeff_in_CH[agent]['coefficients'])
                    sum_inter = numpy.array(self.Dic_recieve_coeff_in_CH[agent]['intercept_'])

            self.avg_coeff = numpy.asarray(sum_coeff) / len(self.Dic_recieve_coeff_in_CH.keys())
            self.intercept_ = numpy.asarray(sum_inter) / len(self.Dic_recieve_coeff_in_CH.keys())
            strr = ''
            for i in self.Dic_recieve_coeff_in_CH.keys():
                strr = strr + ',' + str(i)

        self.accuracy = self.get_accuracy()

        # # =============== ??????? ===================
        # # EPC (Set Coeff Parameters)
        # # =============== ??????? ===================
        # if (self.SourceID not in Dic_CH_Coeff.keys()):
        #     Dic_CH_Coeff[self.SourceID] = {}
        # Dic_CH_Coeff[self.SourceID]['avg_coeff'] = self.avg_coeff
        # Dic_CH_Coeff[self.SourceID]['intercept_'] = self.intercept_
        # # =========



        # =========== send Coefficient to EPC
        self.hello_packet = self.create_Hello_packet()
        self.hello_packet['coefficients']=self.avg_coeff
        self.hello_packet['intercept_']=self.intercept_
        self.coefficients=self.avg_coeff
        self.producer_coeff_to_EPC.send('SendTOEPCCoeff_' + str(EPC_sourceID),
                                        value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'),
                                        )
        # recieve Coefficient from EPC
        self.comsumer_coeff_from_EPC = KafkaConsumer('RecieveFromEPCCoeff_' + str(self.SourceID),
                                                    bootstrap_servers=[Server_Address])
        msg_coff_fromEPC = self.comsumer_coeff_from_EPC.poll(timeout_ms=wait_recieve_coff_from_CMs * 1000)  # wait from now to timeout_ms for recieving all messages within time
        if not msg_coff_fromEPC:
            ''
        else:
            for topic_data, consumer_records in msg_coff_fromEPC.items():  # All messages
                for message in consumer_records:  # each message
                    mess_coeff_EPC = json.loads(message.value)
                    self.avg_coeff=mess_coeff_EPC['coefficients']
                    self.intercept_=mess_coeff_EPC['intercept_']



        # send Coefficient to all CMs
        for CM_ID in list_CMs_Source_IDs:
            self.hello_packet['coefficients'] = preprocess_coeff(self.avg_coeff)
            self.hello_packet['intercept_'] = preprocess_coeff(self.intercept_)
            # print('sendCoeff_'+'From_'+str(CM_ID)+)
            time.sleep(2)
            try:
                self.producer_coeff_to_CM.send('RecieveCHCoeff_' + str(CM_ID),
                                               value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder),
                                                           'utf-8'))
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                print('Error in producer_coeff_to_CM')
                continue


        # break

    def CH_CM_RecieveHelloPacket(self):
        self.vib_neighbor = {}
        while(True):
            try:
                # =======================
                # send Hello Packet
                # =======================
                rnd = random.randint(1, 3)
                time.sleep(rnd)
                # =======================
                # Change position base on SUMO simulation!!!!!!!!!!
                # =============================
                try:
                    self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]
                    self.position_x = float(self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]['x'])
                    self.position_y = float(self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]['y'])
                    self.speed=float(self.dic_vehicl_times[int(self.SourceID)][self.timeChangePosition]['speed'])
                    self.timeChangePosition = self.timeChangePosition + 1
                except:
                    print('')
                    ''
                # ===============================================
                self.hello_packet = self.create_Hello_packet()
                try:
                    self.hello_packet['coefficients'].shape[0]
                except:
                    self.hello_packet['coefficients'] = ''

                # =============
                self.producer.send(public_topicc, value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'))

                # =======================
                # Recieve Hello Packet
                # =======================
                time1 = datetime.datetime.now()
                # ==========

                # while True:
                try:
                    date2 = datetime.datetime.now()
                    self.consumer = KafkaConsumer(public_topicc, bootstrap_servers=[Server_Address])
                    #====================================
                    msg = self.consumer.poll(self.In_TIMER * 1000)

                    if not msg:
                        time.sleep(0.1)
                    else:
                        for topic_data, consumer_records in  msg.items():
                            # for message in self.consumer:
                            for message in consumer_records:  # each message
                                #message = message.value
                                mess = json.loads(message.value)
                                # print(self.SourceID + '<--' + mess['SourceID'] + '--->' + '_Direction_' + mess['direction'] + '  ' +
                                #       mess['timestamp'])

                                #====   ba khodash nabashad!  ====
                                if (mess['SourceID']==self.SourceID):
                                    continue
                                #=======

                                # ==== Insert vib_neighbor
                                # check is neighbor or NOT!
                                # print(self.SourceID + '----'+mess['SourceID'])
                                point1 = numpy.array((self.position_x, self.position_y))
                                point2 = numpy.array((mess['position_x'], mess['position_y']))
                                distance = float(numpy.linalg.norm(point1 - point2))
                                # if (distance>0):
                                #     print('good')
                                if (float(distance) <= float(self.TRANMISSION_RANGE)):  # is Neighbor
                                    if (mess['SourceID'] not in self.vib_neighbor.keys()):
                                        self.vib_neighbor[mess['SourceID']] = {}
                                        self.vib_neighbor[mess['SourceID']]['direction'] = mess['direction']
                                        self.vib_neighbor[mess['SourceID']]['speed'] = mess['speed']
                                        self.vib_neighbor[mess['SourceID']]['number_of_hops_to_CH'] = mess[
                                            'number_of_hops_to_CH']
                                        self.vib_neighbor[mess['SourceID']]['current_clustering_state'] = mess[
                                            'current_clustering_state']
                                        self.vib_neighbor[mess['SourceID']]['distance'] = distance
                                        self.vib_neighbor[mess['SourceID']]['SourceID'] = mess['SourceID']
                                        self.vib_neighbor[mess['SourceID']]['avg_speed'] = float(mess['avg_speed'])
                                        self.vib_neighbor[mess['SourceID']]['V_state'] = str(mess['V_state'])
                                        self.vib_neighbor[mess['SourceID']]['TRY_CONNECT_CH'] = 0
                                        self.vib_neighbor[mess['SourceID']]['HOPE_CM'] = str(mess['HOPE_CM'])
                                        self.vib_neighbor[mess['SourceID']]['Member_CM'] = str(mess['Member_CM'])
                                        self.vib_neighbor[mess['SourceID']]['Member_CH'] = str(mess['Member_CH'])
                                        self.vib_neighbor[mess['SourceID']]['coefficients']=''
                                        self.vib_neighbor[mess['SourceID']]['intercept_']=''




                                    else:  #(Update kardane VIB neighbors)
                                        self.vib_neighbor[mess['SourceID']]['direction'] = mess['direction']
                                        self.vib_neighbor[mess['SourceID']]['speed'] = mess['speed']
                                        self.vib_neighbor[mess['SourceID']]['number_of_hops_to_CH'] = mess[
                                            'number_of_hops_to_CH']
                                        self.vib_neighbor[mess['SourceID']]['current_clustering_state'] = mess[
                                            'current_clustering_state']
                                        self.vib_neighbor[mess['SourceID']]['distance'] = distance
                                        self.vib_neighbor[mess['SourceID']]['SourceID'] = mess['SourceID']
                                        self.vib_neighbor[mess['SourceID']]['avg_speed'] = float(mess['avg_speed'])
                                        self.vib_neighbor[mess['SourceID']]['V_state'] = str(mess['V_state'])
                                        # self.vib_neighbor[mess['SourceID']]['TRY_CONNECT_CH']=0
                                        self.vib_neighbor[mess['SourceID']]['HOPE_CM'] = str(mess['HOPE_CM'])
                                        self.vib_neighbor[mess['SourceID']]['Member_CM'] = str(mess['Member_CM'])
                                        self.vib_neighbor[mess['SourceID']]['Member_CH'] = str(mess['Member_CH'])


                                    # for coefficients
                                    if (self.vib_neighbor[mess['SourceID']]['coefficients'] != ''):
                                        self.vib_neighbor[mess['SourceID']]['coefficients_tMinus1'] = str(
                                            self.vib_neighbor[mess['SourceID']]['coefficients'])
                                        self.vib_neighbor[mess['SourceID']]['intercept_tMinus1'] = str(
                                            self.vib_neighbor[mess['SourceID']]['intercept_'])

                                    self.vib_neighbor[mess['SourceID']]['coefficients'] = str(mess['coefficients'])
                                    self.vib_neighbor[mess['SourceID']]['intercept_'] = str(mess['intercept_'])






                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    time.sleep(0.1)

                # ====
                # speed avg (For IN-TIMER recieved hello_packet)
                # =====
                sum_minus_speed = 0
                N_i = 0
                if (len(list(self.vib_neighbor.keys())) > 1):
                    # print('asd')
                    ''
                for neigh in self.vib_neighbor.keys():
                    if (self.vib_neighbor[neigh]['direction'] == self.direction):
                        if (int(self.vib_neighbor[neigh]['number_of_hops_to_CH']) <= self.MAX_HOPs):  # within MAX_HOP
                            N_i = N_i + 1
                            speed_i = self.speed
                            speed_ij = self.vib_neighbor[neigh]['speed']
                            minus_speed = numpy.abs(speed_i - speed_ij)
                            sum_minus_speed = sum_minus_speed + minus_speed

                if (N_i != 0):
                    self.avg_speed = sum_minus_speed / N_i
                else:
                    self.avg_speed = self.speed

            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                ''

    def CH_changeState(self):

        Join_Timer = 5
        # neighbor_Avg_CoSimCH={}
        try:
            Avg_CoSim_k= min(list(self.neighbor_Avg_CoSimCH.values()))   # minimum Avg_CoSimCH ghablihaa
        except:
            return 1
            Avg_CoSim_k=999999

        connectionCH_neighbor={}
        for neighbor in self.vib_neighbor.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CH'):  # for all CH in vib


                avgSpeedCH=self.vib_neighbor[neighbor]['avg_speed']

                thetaCH = self.vib_neighbor[neighbor]['coefficients']
                try:
                    thetaCH_tminus1=self.vib_neighbor[neighbor]['coefficients_tMinus1']
                except:
                    print('Error in neighbor_Avg_CoSimCH')
                    thetaCH_tminus1=self.coefficients

                Avg_CoSimCH = calculate_Avg_CoSimCH_threeElements(self.alpha, avgSpeedCH,  thetaCH, thetaCH_tminus1)

                self.vib_neighbor[neighbor]['Avg_CoSimCH'] = Avg_CoSimCH
                connectionCH_neighbor[neighbor] = True
                self.neighbor_Avg_CoSimCH[neighbor] = Avg_CoSimCH

        self.neighbor_Avg_CoSimCH = dict(sorted(self.neighbor_Avg_CoSimCH.items(), key=lambda item: item[1]))

        for neighbor in self.neighbor_Avg_CoSimCH.keys():
            if (self.vib_neighbor[neighbor]['V_state'] == 'CH'):
                if (self.neighbor_Avg_CoSimCH[neighbor]<Avg_CoSim_k):
                    # ===============send connect_request ===========
                    if (connectionCH_neighbor[neighbor] == True):
                        self.consumer_respect_CH = KafkaConsumer('Connect_Response_' + str(self.SourceID),
                                                                 bootstrap_servers=[Server_Address])

                        self.producer_request_CH.send('Connect_Request_' + str(neighbor),
                                                      value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder),
                                                                  'utf-8'))
                        msg_respect = self.consumer_respect_CH.poll(timeout_ms=Join_Timer * 1000)
                        if not msg_respect:
                            ''
                        else:  # Connect_Response recieved
                            for topic_data, consumer_records in msg_respect.items():
                                message_resp = consumer_records[0].value  # only one message is served!!! consumer_records[0]
                                mess_resp = json.loads(message_resp)

                                # ================
                                # Connect to (best) CH
                                # ============
                                # self.ID_to_CH = str(neighbor)
                                self.ID_to_CH = mess_resp['SourceID']
                                self.mess_resp = mess_resp
                                if (self.V_state == 'CH'):
                                    self.V_state = 'CM'
                                    return 1


                        ######
                        #####
                        #######



    def CHstate_algorithm(self):
        while(True):
            try:
                self.CH_HFL()    # OK  # send recieve Training theta (Algorithm 6)  - working for Federated Learning ---
                # self.CH_CM_RecieveHelloPacket() # OK   # update VIB  ( dar in ghesmat faghat HelloPacket haro recieve mikonad!!)
                self.CH_changeState()    # OK  # change State ( if State change ---> exit from this function) --- (Algorithm 3)
                if (self.V_state != 'CH'):
                    break
            except:
                continue


    def NoClustering_HFL(self):  # for all nodes train and end back coefficients to EPC
        while(True):
            try:
                time.sleep(random.randint(1,5))

                self.Train_Update_local_SGD()

                # =========== send Coefficient to EPC
                wait_recieve_coff_from_EPC=5
                self.hello_packet = self.create_Hello_packet()
                self.hello_packet['coefficients']=self.coefficients
                self.hello_packet['intercept_']=self.intercept_
                self.producer_coeff_to_EPC.send('SendTOEPCCoeff_' + str(EPC_sourceID),
                                                value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'),
                                                )
                # recieve Coefficient from EPC
                self.comsumer_coeff_from_EPC = KafkaConsumer('RecieveFromEPCCoeff_' + str(self.SourceID),
                                                            bootstrap_servers=[Server_Address])
                msg_coff_fromEPC = self.comsumer_coeff_from_EPC.poll(timeout_ms=wait_recieve_coff_from_EPC * 1000)  # wait from now to timeout_ms for recieving all messages within time
                if not msg_coff_fromEPC:
                    ''
                else:
                    for topic_data, consumer_records in msg_coff_fromEPC.items():  # All messages
                        for message in consumer_records:  # each message
                            mess_coeff_EPC = json.loads(message.value)
                            self.coefficients=mess_coeff_EPC['coefficients']
                            self.intercept_=mess_coeff_EPC['intercept_']

            except:
                continue







        # # =============== ??????? ===================
        # # EPC (Set Coeff Parameters)
        # # =============== ??????? ===================
        # if (self.SourceID not in Dic_CH_Coeff.keys()):
        #     Dic_CH_Coeff[self.SourceID] = {}
        # Dic_CH_Coeff[self.SourceID]['avg_coeff'] = self.avg_coeff
        # Dic_CH_Coeff[self.SourceID]['intercept_'] = self.intercept_
        # # =========

        #
        # self.consumer_EPC = KafkaConsumer('SendTOEPCCoeff_' + str(self.SourceID),
        #                                   bootstrap_servers=[Server_Address])
        # while(True):
        #     try:
        #
        #         msg_coff_EPC = self.consumer_EPC.poll(
        #             timeout_ms=5 * 1000)  # wait from now to timeout_ms for recieving all messages within time
        #         if not msg_coff_EPC:
        #             ''
        #         else:
        #             for topic_data, consumer_records in msg_coff_EPC.items():  # All messages
        #                 # ======== Reviece Coeff from CHs
        #                 for message in self.consumer_EPC :  # each message
        #                     self.mess_from_CH_EPC = json.loads(message.value)
        #                     try:  # momken ast ke 'intercept_' dar self.mess_from_CH vojod nadashte bashad!!!
        #                         node_SourceID=self.mess_from_CH_EPC['SourceID']
        #
        #                         self.hello_packet['coefficients'] = numpy.asarray(self.mess_from_CH_EPC['coefficients'])
        #                         self.hello_packet['intercept_'] = numpy.asarray(self.mess_from_CH_EPC['intercept_'])
        #                     except:  # bazi az message ha 'intercept_ ra nadarand!! (SKIP mikonim!!!!) --- choon male ghabl hastan ke ersal shodand!!!!!
        #                         continue
        #






        #
        #
        #
        #             ## self.Member_CH = self.Member_CH + 1
        #
        #             time.sleep(3)  # hatman takhir bekhorad ta Cosumer amade bashad
        #             try:
        #                 self.producer_respect_CH.send('Join_Response_' + str(json.loads(message.value)['SourceID']),
        #                                           value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'),
        #                                               )
        #             except:
        #                 print('Error Created for producer_respect_CH')
        #                 continue
        #             self.remain_CH=1
        #     except:
        #         continue
        #










    def CM_HFL(self):
        self.have_coef=0
        # recieve Coefficient from CH
        self.consumer_coeff_from_CH = KafkaConsumer('RecieveCHCoeff_' + str(self.SourceID),
                                                    bootstrap_servers=[
                                                        Server_Address])
        self.msg_coef = self.consumer_coeff_from_CH.poll(timeout_ms=20 * 1000)
        if not self.msg_coef:
            # print('Not Recieve Coeff from CH')
            ''
        else:
            for topic_data, consumer_records in self.msg_coef.items():
                for message in consumer_records:  # each message
                    if (self.have_coef==1):
                        break
                    self.mess_from_CH = json.loads(message.value)
                    try:
                        # bayad dobre train shavad ba in Coefficient ha
                        self.coefficients = numpy.asarray(self.mess_from_CH['coefficients'])
                        self.intercept_ = numpy.asarray(self.mess_from_CH['intercept_'])
                        self.have_coef = 1
                    except:
                        continue


                    # ==== (vase tekrare badi)
                    print('EXITTTT')
                    # ====


        # ------ SGD --------  ????????????????
        # if (self.have_coef == 0):  # for First Time
        #     self.coefficients = self.mess_resp['coefficients']  # get coefficients from CH  ?????????????????
        #     self.intercept_ = self.mess_resp['intercept_']  # get coefficients from CH   ???????????????


        self.Train_Update_local_SGD()
        #Send To CH   (OK)
        self.hello_packet = self.create_Hello_packet()
        self.producer_coeff_to_CH.send('SendCHCoeff_' + str(self.ID_to_CH),
                                       value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'))

    def CM_changeState(self):
        TIMER_CM_MAX=5
        if (self.have_coef==1):  # yani Coefficient az tarafe CH recieve shode ast
            self.timer_CM=0
        else:
            self.timer_CM=self.timer_CM+1

        if (self.timer_CM>TIMER_CM_MAX):
            self.V_state='SE'



    def CMstate_algorithm(self):
        while (True):
            self.CM_HFL()  # OK  # send recieve Training theta (Algorithm 7)  - working for Federated Learning ---
            # self.CH_CM_RecieveHelloPacket()  #OK  # update VIB  ( dar in ghesmat faghat HelloPacket haro recieve mikonad!!)
            self.CM_changeState()   #OK  # change State ( if State change ---> exit from this function) --- (Algorithm 3)
            if (self.V_state != 'CM'):
             break
        pass

    # =====
    # Define EPC
    # =====

    def EPC(self):

        # pass
        # ?????????????????????????/
        # ???????????????????????????????????????
        # ????????????????????????????????????
        dic_EPCcoeffiecients = {}
        dic_EPCintercept = {}
        list_accuracy = list()
        while (True):
            try:
                list_CH_recieved=list()
                self.consumer_EPC = KafkaConsumer('SendTOEPCCoeff_' + str(EPC_sourceID),
                                             bootstrap_servers=[Server_Address])
                self.msg_coff_EPC = self.consumer_EPC.poll(
                    timeout_ms=5 * 1000)  # wait from now to timeout_ms for recieving all messages within time
                if not self.msg_coff_EPC:
                    ''
                else:
                    for topic_data, consumer_records in self.msg_coff_EPC.items():  # All messages
                        # ======== Reviece Coeff from CHs
                        for message in consumer_records:  # each message
                            self.mess_from_CH_EPC = json.loads(message.value)

                            dic_EPCcoeffiecients[self.mess_from_CH_EPC['SourceID']] = numpy.asarray(
                                self.mess_from_CH_EPC['coefficients'])
                            dic_EPCintercept[self.mess_from_CH_EPC['SourceID']] = numpy.asarray(
                                self.mess_from_CH_EPC['intercept_'])

                            list_CH_recieved.append(self.mess_from_CH_EPC['SourceID'])

                # === calculate EPC accuracy ====
                avg_coeff_EPC = ''
                avg_intercept_EPC = ''

                # Dic_CH_Coeff_temp=Dic_CH_Coeff.copy()
                for item in dic_EPCcoeffiecients.keys():
                    try:
                        if (avg_coeff_EPC == ''):
                            avg_coeff_EPC = numpy.array(dic_EPCcoeffiecients[item])
                        else:
                            avg_coeff_EPC = numpy.array(avg_coeff_EPC) + numpy.array(dic_EPCcoeffiecients[item])
                    except:
                        continue



                for item in dic_EPCintercept.keys():
                    try:
                        if (avg_intercept_EPC == ''):
                            avg_intercept_EPC = numpy.array(dic_EPCintercept[item])
                        else:
                            avg_intercept_EPC = avg_intercept_EPC + numpy.array(dic_EPCintercept[item])
                    except:
                        continue





                if (len(dic_EPCintercept.keys()) != 0):
                    average_avg_coeff_EPC = numpy.asarray(avg_coeff_EPC) / len(dic_EPCintercept.keys())
                    try:
                        avg_intercept_EPC = numpy.asarray(avg_intercept_EPC) / len(dic_EPCintercept.keys())
                    except:
                        avg_intercept_EPC=average_avg_coeff_EPC



                    sgd_classifier_EPC.coef_ = average_avg_coeff_EPC
                    sgd_classifier_EPC.intercept_ = avg_intercept_EPC
                    # sgd_classifier_EPC.coef_ = Dic_CH_Coeff[list(Dic_CH_Coeff.keys())[0]]['avg_coeff']
                    # sgd_classifier_EPC.intercept_ = Dic_CH_Coeff[list(Dic_CH_Coeff.keys())[0]]['intercept_']

                    try:
                        sgd_classifier_EPC.partial_fit(self.X_data, self.Y_data, classes=numpy.unique(self.Y_data))
                    except:
                        sgd_classifier_EPC.fit(self.X_data, self.Y_data)

                    acc = sgd_classifier_EPC.score(self.X_data_test, self.Y_data_test)

                    if (len(list_accuracy) == 0 or list_accuracy[-1] != acc):
                        list_accuracy.append(acc)
                        # count_round = count_round - 1

                    # lst_str_CH_bodes[0] = ','.join(list(Dic_CH_Coeff_temp.keys()))
                    lst_acc.append(str(acc))

                    # my_table.add_row(
                    #     [str_CH_bodes, str(acc)])
                    # print(my_table)

                    self.coefficients=avg_coeff_EPC
                    self.intercept_=avg_intercept_EPC
                    # =========== send Coefficient to All Reciever Nodes

                    hello_packet = self.create_Hello_packet()
                    hello_packet['coefficients'] = avg_coeff_EPC
                    hello_packet['intercept_'] = avg_intercept_EPC

                    if (hello_packet['coefficients']  == 0):
                        hello_packet['coefficients']  = ''
                    if (hello_packet['intercept_'] == 0):
                        hello_packet['intercept_'] = ''


                    for CHnode in list_CH_recieved:
                        self.producer_EPC_coeff_to_CH.send('RecieveFromEPCCoeff_' + str(CHnode),
                                                   value=bytes(dumps(self.hello_packet, cls=NumpyArrayEncoder), 'utf-8'),
                                                   )

            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                continue

        #
        #
        #
        #             ## self.Member_CH = self.Member_CH + 1
        #             self.hello_packet = self.create_Hello_packet()
        #             time.sleep(3)  # hatman takhir bekhorad ta Cosumer amade bashad
        #             try:
        #                 self.producer_respect_CH.send('Join_Response_' + str(json.loads(message.value)['SourceID']),
        #                                           value=bytes(dumps(self.hello_packet,cls=NumpyArrayEncoder), 'utf-8'),
        #                                               )
        #             except:
        #                 print('Error Created for producer_respect_CH')
        #                 continue
        #             self.remain_CH=1
        #     except:
        #         continue
        #



    def Main_Algorithm(self):
        while(True):

            # self.CH_CM_RecieveHelloPacket()  # OK   # update VIB
            try:
                if (self.V_state=='SE'):   # for V_state=='SE'
                    print('CHsection')
                    try:
                        self.SA_State_CHsection()  # OK
                        time.sleep(random.randint(1,7))
                    except:
                        ''
                    print('CMsection')
                    try:
                        self.SA_State_CMsection()  # OK
                        time.sleep(random.randint(1, 7))
                    except:
                        ''

                    print('SEsection')
                    try:
                        self.SA_State_SEsection()  # OK
                        time.sleep(random.randint(1, 7))
                    except:
                        ''
                else:
                    if (self.V_state=='CH'):
                        try:
                            self.CHstate_algorithm()   # OK
                            time.sleep(random.randint(1, 2))
                        except:
                            ''
                    else:
                        if (self.V_state=='CM'):
                            try:
                                self.CMstate_algorithm()   #OK
                                time.sleep(random.randint(1, 2))
                            except:
                                ''
            except:
                continue

        #????? EPC ??????



        # =====
        # Print results
        # ====
        # print('=========== NODE ' + str(self.SourceID) + ' ============')
        # print('Number_of_neighbors_linked== ' + str(N_i))
        # print('average_spd== ' + str(self.avg_speed))
        # print('V_state== ' + str(self.V_state))
        # for neigh in self.vib_neighbor.keys():
        # print(self.vib_neighbor[neigh]['SourceID'] + '__State__' + str(
        #     self.vib_neighbor[neigh]['V_state']) + ' ---> ' + str(self.vib_neighbor[neigh]['avg_speed']))
        # print('========================================')
        # print('finish === ' + str(avg_speed))

        #
        # time1=datetime.datetime.now()
        # for message in self.consumer:
        #     message = message.value
        #     mess = json.loads(message)
        #     print(
        #         self.SourceID + '<--' + mess['SourceID'] + '--->' + '_Direction_' + mess['direction'] + '  ' + mess[
        #             'timestamp'])
        #     date2=datetime.datetime.now()
        #     if ((date2-time1).seconds>10):
        #         self.consumer=list()
        #         break

        # if ((date2 - time1).seconds > 10):
        #     return
        # self.consumer=list()

        # time.sleep(self.In_TIMER)
        # records = self.consumer.poll(self.In_TIMER*1000)
        # message = self.consumer.poll(10.0)
        # if not message:
        # time.sleep(120) # Sleep for 2 minutes
        # time.sleep(self.In_TIMER)
        # for topic_data, consumer_records in records.items():
        # # for message in self.consumer:
        #     message = consumer_records[0].value
        #     mess = json.loads(message)
        #     print(self.SourceID+'<--'+mess['SourceID']+'--->'+ '_Direction_'+mess['direction']+'  '+mess['timestamp'])

        # ============
        # SE election algorithm (after IN_TIMER pass  --> in SE state insertee)
        # ============
        #if (self.V_state == 'CH'): # digar kari nadashte bashad be SA_ALgorithm



        # ====
        # Training and Coeffient Send
        # ====
        # if (returned_value == 1):
        #     self.Train_sendCoeff()
        #
        # time1 = datetime.datetime.now()
        # time.sleep(self.SE_TIMER)






    # def run_background_recieve(self):
    #     recieve_hello_packet_thread = threading.Thread(target=self.recieve_Hello_packet)
    #     recieve_hello_packet_thread.start()





import time

# send_hello_packet_thread1 = threading.Thread(target=vehicle_VIB,args=(10,30,10,'2'))
# send_hello_packet_thread1.start()
# time.sleep(1)
# send_hello_packet_thread2 = threading.Thread(target=vehicle_VIB,args=(10,30,10,'1'))
# send_hello_packet_thread2.start()
# time.sleep(1)
# send_hello_packet_thread3 = threading.Thread(target=vehicle_VIB,args=(10,30,10,'3'))
# send_hello_packet_thread3.start()
# veh2 = vehicle_VIB(10, 30, 10, '2')
# recieve_hello_packet_thread1 = threading.Thread(target=veh2.recieve_Hello_packet)
# recieve_hello_packet_thread1.start()
# time.sleep(1)



# #=== Delete All topics =====
# #https://stackoverflow.com/questions/36641755/kafka-python-retrieve-the-list-of-topics
# #https://dev.to/sats268842/create-and-delete-kafka-topic-using-python-3ni
# import  kafka
# consumer = kafka.KafkaConsumer(bootstrap_servers=[Server_Address])
# admin_client = kafka.KafkaClient(bootstrap_servers=[Server_Address])
# admin_client.delete_topics(topics='RespectCH_9')
# consumer.topics()
# def delete_topics(topic_names):
#     try:
#         admin_client.delete_topics(topics=topic_names)
#         print("Topic Deleted Successfully")
#     except UnknownTopicOrPartitionError as e:
#         print("Topic Doesn't Exist")
#     except  Exception as e:
#         print(e)



import json
def save_result_Json(Dic_CH_accuracy,lst_acc,numberVehicles):
    dump_Dic_CH_accuracy=json.dumps(Dic_CH_accuracy)
    fp=open('dumpDic_CH_accuracy_NEW'+str(numberVehicles)+'.txt','w',encoding='utf8')
    fp.write(dump_Dic_CH_accuracy)
    fp.close()

    dump_lst_acc=json.dumps(lst_acc)
    fp=open('dumplst_acc_NEW'+str(numberVehicles)+'.txt','w',encoding='utf8')
    fp.write(dump_lst_acc)
    fp.close()

    return
def load_result_json(path='dumpDic_CH_accuracy.txt',path_lst_acc='dumplst_acc.txt'):
    fp1=open(path,'r',encoding='utf8')
    rr=fp1.read()
    diccc=json.loads(rr)

    fp2=open(path_lst_acc,'r',encoding='utf8')
    rr2=fp2.read()
    lst_acc_dic=json.loads(rr2)


    return diccc,lst_acc_dic

def plot_accuracy(Dic_CH_accuracy,lst_acc):
    for CH in Dic_CH_accuracy.keys():
        lst_ch = Dic_CH_accuracy[CH]
        x = [i for i in range(0, len(lst_ch))]
        y = lst_ch
        # plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
        #          marker='o', markerfacecolor='blue', markersize=12)
        plt.plot(x, y, marker='o', label='CH_node' + CH)
        # setting x and y axis range
        # plt.ylim(1, 8)
        # plt.xlim(1, 8)

        # naming the x axis
        plt.xlabel('Communication Rounds')
        # naming the y axis
        plt.ylabel('Accuracy')

        # giving a title to my graph
        plt.title('Comparisons')
        leg = plt.legend()
        # function to show the plot
    plt.show()


    # save as SVG
    image_format = 'svg'  # e.g .png, .svg, etc.
    image_name = 'Comparisons.svg'
    plt.savefig(image_name, format=image_format, dpi=2000)
    # plt.savefig(image_name, format=image_format, dpi=1200)

    # === PLOT EPC
    # === plot accuracy
    x = [i for i in range(0, len(lst_acc))]
    # y = lst_acc
    y = list()
    for j in lst_acc:
        y.append(round(float(j), 2))
    plt.plot(x, y, marker='o', label='EPC_Node')
    plt.xlabel('Communication Rounds')
    plt.ylabel('Accuracy')
    plt.title('EPC results')
    leg = plt.legend()
    plt.show()
    print('Finish Plot')
    # ======

    # print('jh')
    # print(
    #     str(item.SourceID)+'\t'+
    #     str(item.V_state)+'\t'+
    #     str(item.ID_to_CH)+'\t'+
    #     str(AssignedNodes)+'\t'+
    #     str(item.accuracy)
    #
    # )
    # print('==========================')

    # =============================================
    # =============================================
    # =============================================
    #################### Save as SVG ########################
    image_format = 'svg'  # e.g .png, .svg, etc.
    image_name = 'EPC results.svg'
    plt.savefig(image_name, format=image_format)
    #=============================================
    # =============================================
    # =============================================
    # =============================================


import matplotlib.pyplot as plt
# # #====
# # # Load result and Plot the results
# # #=====
# path='dumpDic_CH_accuracy_NEW10.txt'
# path_lst_acc='dumplst_acc_NEW10.txt'
# Dic_CH_accuracy,lst_acc=load_result_json(path=path,path_lst_acc=path_lst_acc)
# plot_accuracy(Dic_CH_accuracy,lst_acc)

import random
list_vehicles = list()
#====== Dynamic delcare number of vehicles
def define_vehicles(list_vehicles,numberOfVehicles,dic_vehicl_times,haveClustering):
    # ===============
    # **** Configure train and test data
    # ===============
    # split train test for ALL dataset
    # split train dataset into Vehicles!!!
    from sklearn.model_selection import train_test_split
    list_data_vehicles_X_data, list_data_vehicles_y_data, all_X_data, all_y_data = load_minist_data(count_vehicles=numberOfVehicles+1)
    X_train, X_test, y_train, y_test = train_test_split(all_X_data, all_y_data, test_size=0.33, random_state=42)
    # print('split)')
    ##===============

    # dic_vehicl_times
    #================

    # change_x=random.randint(10, 50)
    # change_y=random.randint(10, 50)
    # change_delay=random.randint(1,3)
    for i in range(1,numberOfVehicles+1):
        try:
            change_x=float(dic_vehicl_times[i][0]['x'])
            change_y=float(dic_vehicl_times[i][0]['y'])
            change_speed=float(dic_vehicl_times[i][0]['speed'])
            change_delay = random.randint(10, 20)
        except:
            change_x = random.randint(10, 50)
            change_y = random.randint(10, 50)
            change_speed = random.randint(10, 50)
            change_delay = random.randint(10, 20)

        list_vehicles.append(
            vehicle_VIB(change_x, change_y, change_speed, str(i), list_data_vehicles_X_data[i], list_data_vehicles_y_data[i], X_test, y_test,
                        100,dic_vehicl_times,'0',haveClustering))
        time.sleep(change_delay)

    #========================
    # Create EPC
    vehicle_VIB(change_x, change_y, change_speed, '999', X_train, y_train, X_test,
                y_test,
                100, dic_vehicl_times, '1',haveClustering)

    #============================

    return X_train,y_train,X_test, y_test

#======
from Read_XML import get_dic_vehicl_times
numberOfVehicles=10
dic_vehicl_times=get_dic_vehicl_times()
EPC_sourceID = 999
haveClustering='1'
X_train,y_train,X_test, y_test=define_vehicles(list_vehicles,numberOfVehicles,dic_vehicl_times,haveClustering)
# =============

# time.sleep(3)
# veh1 = vehicle_VIB(10, 100, 50, '6')
# recieve_hello_packet_thread2 = threading.Thread(target=veh1.recieve_Hello_packet)
# recieve_hello_packet_thread2.start()
print('finish')

# ===================
# SHOW RESULTs
# =================

# Dic_CH_Coeff
from prettytable import PrettyTable

sgd_classifier_EPC = SGDClassifier(random_state=42, max_iter=100)
lst_str_CH_bodes = list()
lst_str_CH_bodes.append('')

lst_acc = list()
lst_acc.append(0)





def Plot_EPC_Accuracy_Table(X_train,y_train,X_test, y_test):
    my_table = PrettyTable()
    my_table.field_names = ["CH_Nodes", "Accuracy"]

    # training_data=list_data_vehicles_X_data[8]
    # training_y=list_data_vehicles_y_data[8]

    training_data = X_train
    training_y = y_train

    count_round = 100000000
    list_accuracy = list()
    while (True):
        try:
            avg_coeff_EPC = ''
            avg_intercept_EPC = ''
            # sum_coeff = sum_coeff + numpy.array(self.Dic_recieve_coeff_in_CH[agent]['coefficients'])
            Dic_CH_Coeff_temp=Dic_CH_Coeff.copy()
            for item in Dic_CH_Coeff_temp.keys():
                if (avg_coeff_EPC == ''):
                    avg_coeff_EPC = numpy.array(Dic_CH_Coeff_temp[item]['avg_coeff'])

                else:
                    avg_coeff_EPC = numpy.array(avg_coeff_EPC) + numpy.array(Dic_CH_Coeff_temp[item]['avg_coeff'])

                if (avg_intercept_EPC == ''):
                    avg_intercept_EPC = numpy.array(Dic_CH_Coeff_temp[item]['intercept_'])
                else:
                    avg_intercept_EPC = avg_intercept_EPC + numpy.array(Dic_CH_Coeff_temp[item]['intercept_'])

            if (len(Dic_CH_Coeff_temp.keys()) != 0):
                average_avg_coeff_EPC = numpy.asarray(avg_coeff_EPC) / len(Dic_CH_Coeff_temp.keys())
                avg_intercept_EPC = numpy.asarray(avg_intercept_EPC) / len(Dic_CH_Coeff_temp.keys())

                sgd_classifier_EPC.coef_ = average_avg_coeff_EPC
                sgd_classifier_EPC.intercept_ = avg_intercept_EPC
                # sgd_classifier_EPC.coef_ = Dic_CH_Coeff[list(Dic_CH_Coeff.keys())[0]]['avg_coeff']
                # sgd_classifier_EPC.intercept_ = Dic_CH_Coeff[list(Dic_CH_Coeff.keys())[0]]['intercept_']

                try:
                    sgd_classifier_EPC.partial_fit(training_data, training_y, classes=numpy.unique(training_y))
                except:
                    sgd_classifier_EPC.fit(training_data, training_y)

                acc = sgd_classifier_EPC.score(X_test, y_test)

                if (len(list_accuracy) == 0 or list_accuracy[-1] != acc):
                    list_accuracy.append(acc)
                    count_round = count_round - 1

                lst_str_CH_bodes[0] = ','.join(list(Dic_CH_Coeff_temp.keys()))
                lst_acc.append(str(acc))

                # my_table.add_row(
                #     [str_CH_bodes, str(acc)])
                # print(my_table)

                if (count_round == 0):
                    break
            time.sleep(2)
        except:
            continue
    #
    # # === plot accuracy
    # x = [i for i in range(0, len(list_accuracy))]
    # y = list_accuracy
    # plt.plot(x, y, marker='o', label='EPC_Node')
    # plt.xlabel('Comminication Rounds')
    # plt.ylabel('Accuracy')
    # plt.title('EPC results')
    # leg = plt.legend()
    # plt.show()

    # ====


def Plot_CH_Accuracy_Table(numberVehicles):
    # lst_str_CH_bodes, lst_acc
    Dic_CH_accuracy = {}
    count_round = 1000
    while (True):

        #=======
        # Write to File
        #======
        save_result_Json(Dic_CH_accuracy,lst_acc,numberVehicles)
        #==================




        my_table = PrettyTable()
        my_table.field_names = ["SourceID", "State", "CH_Node", "AssignedNodes", "Accuracy", "EPC_CHNodes",
                                "EPC_Accuracy"]
        # my_table.add_row([1, "Bobbbbbbbbbbbbbbbbbbb", 6, 11])
        # my_table.add_row([2, "Freddy", 4, 10])
        # my_table.add_row([3, "John", 7, 13])
        # print(my_table)
        # print('==========================')
        # print('SourceID', '\t', 'State' + '\t' + 'CH_Node' + '\t' + 'AssignedNodes' + '\t' + 'Accuracy')

        for item in list_vehicles:
            try:
                # print('TEDADDDDD==='+str(len(item.Dic_recieve_coeff_in_CH.keys())))
                AssignedNodes = ','.join(item.Dic_recieve_coeff_in_CH.keys())
            except:
                AssignedNodes = '-'
            my_table.add_row(
                [str(item.SourceID), str(item.V_state), str(item.ID_to_CH), str(AssignedNodes), str(item.accuracy),
                 str(lst_str_CH_bodes[0]), str(lst_acc[-1])])
            if (item.V_state == 'CH'):
                if (item.SourceID not in Dic_CH_accuracy.keys()):
                    Dic_CH_accuracy[item.SourceID] = list()
                    Dic_CH_accuracy[item.SourceID].append(0)
                if (Dic_CH_accuracy[item.SourceID][-1] != float(item.accuracy)):
                    Dic_CH_accuracy[item.SourceID].append(float(item.accuracy))
                    count_round = count_round - 1
        if (count_round == 0):
            break

        print(my_table)
        time.sleep(1)

    return Dic_CH_accuracy


# ===== Calling =====
# Important :
# CH === roye self.X_data training mishavad-- vase yekseri data kamm     (dar X_test testing mishavad)
# EPC === roye X_data (koll) training mikonad--- vase kole data training     (dar X_test testing mishavad)


# th_EPC = threading.Thread(target=Plot_EPC_Accuracy_Table,args=(X_train,y_train,X_test, y_test))
# th_EPC.start()


# Plot_EPC_Accuracy_Table(lst_str_CH_bodes,lst_acc)
Dic_CH_accuracy = Plot_CH_Accuracy_Table(numberOfVehicles)
plot_accuracy(Dic_CH_accuracy,lst_acc)

# for ii in ['a','b']:
#     recieve_hello_packet_thread2.join()
#     recieve_hello_packet_thread1.join()


# veh3=vehicle_VIB(10,30,40,'3')
# veh3=vehicle_VIB(10,30,40,'4')
# veh3=vehicle_VIB(10,30,40,'5')
# veh3=vehicle_VIB(10,30,40,'6')
# veh3=vehicle_VIB(10,30,40,'7')

#
# veh2.run_background()
#
# veh1=vehicle_VIB(10,20,10,'1')
# for i in range(0,10):
#     veh1.send_Hello_packet()
#     time.sleep(3)
#
# veh3=vehicle_VIB(10,20,10,'3')
# for i in range(0,10):
#     veh3.send_Hello_packet()
#     time.sleep(2)