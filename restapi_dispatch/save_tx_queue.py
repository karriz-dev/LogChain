import threading
import logging
from queue import Queue
import time
from restapi_dispatch import queue_strategy
import json
from service.transactionmanager import transaction
from communication.p2p import sender
from peerproperty import nodeproperty
from monitoring import monitoring


class SaveTxQueueThread(threading.Thread):
    def __init__(self, p_thrd_id, p_thrd_name, p_inq):
        threading.Thread.__init__(self)
        self.thrd_id = p_thrd_id
        self.thrd_name = p_thrd_name
        self.inq = p_inq

    def run(self):
        receive_event(self.thrd_name, self.inq)

    # def save_sensorinfo(self, p_sensorinfo_json):
    #     monitoring.log('log.Request(save sensor info) rcvd...')
    #     self.inq.put(p_sensorinfo_json)
    #     monitoring.log("log."+str(self.inq))
    #     monitoring.log("log."+self.inq.qsize())




def receive_event(p_thrd_name, p_inq):
    total_tx_count = 1
    while True:
        monitoring.log("log.Wait for transaction creation request.")

        dequeued = p_inq.get()

        tx = transaction.Transaction(dequeued)
        # temp = json.dumps(
        #     tx, indent=4, default=lambda o: o.__dict__, sort_keys=True)

        # for try
        temp = json.dumps(tx, default=lambda o: o.__dict__, sort_keys=True)


        # sender.send_to_all(temp)
        sender.send_to_all_peers(temp,nodeproperty.My_receiver_port)

        monitoring.log("log.Transaction creation request - rcvd: "+str(dequeued))
        monitoring.log("log.Transaction creation request - rcvd(json): "+str(temp))
        monitoring.log("log.Total number of transaction creation request: "+str(total_tx_count ))
        # monitoring.log("log."+str(p_inq.qsize()))
        total_tx_count = total_tx_count + 1
        # time.sleep(queue_strategy.SAVE_TX_DEQUEUE_INTERVAL)
