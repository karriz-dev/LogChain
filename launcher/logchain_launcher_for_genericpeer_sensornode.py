import logging
import sys
from PyQt5 import QtWidgets
from peerproperty import nodeproperty
from peerproperty import set_peer
from storage import file_controller
from communication.p2p import receiver
from service.blockmanager import genesisblock
from communication.msg_dispatch import dispatch_queue_list
from communication.msg_dispatch import t_type_queue_thread
from communication.msg_dispatch import b_type_queue_thread
from communication.msg_dispatch import v_type_queue_thread
from communication.peermgr import peerconnector
from monitoring import monitoring
from supplychain.supplychain_ui import main_ui



# Logchain launcher function for GenericPeer
# GenericPeer performs the role of PeerConnector in parallel.
def initialize_process_for_generic_peer():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    monitoring.log("log.Start Logchain launcher for TrustPeer...")

    initialize()

    monitoring.log('log.Run processes for PeerConnector.')

    if not peerconnector.start_peerconnector():
        monitoring.log('log.Aborted because PeerConnector execution failed.')
        return


    set_peer.set_my_peer_num()
    monitoring.log("log.My peer num: " + str(nodeproperty.My_peer_num))

    'Genesis Block Create'
    genesisblock.genesisblock_generate()

    monitoring.log("log.Start a thread to receive messages from other peers.")
    recv_thread = receiver.ReceiverThread(
        1, "RECEIVER", nodeproperty.My_IP_address, nodeproperty.My_receiver_port)
    recv_thread.start()
    monitoring.log("log.The thread for receiving messages from other peers has started.")


    t_type_qt = t_type_queue_thread.TransactionTypeQueueThread(
        1, "TransactionTypeQueueThread",
        dispatch_queue_list.T_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    t_type_qt.start()

    v_type_qt = v_type_queue_thread.VotingTypeQueueThread(
        1, "VotingTypeQueueThread",
        dispatch_queue_list.V_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    v_type_qt.start()

    b_type_qt = b_type_queue_thread.BlockTypeQueueThread(
        1, "BlockTypeQueueThread",
        dispatch_queue_list.B_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    b_type_qt.start()


def initialize():
    monitoring.log('log.Start the blockchain initialization process...')
    file_controller.remove_all_transactions()
    file_controller.remove_all_blocks()
    file_controller.remove_all_voting()
    monitoring.log('log.Complete the blockchain initialization process...')
    set_peer.init_myIP()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = main_ui.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    initialize_process_for_generic_peer()

    sys.exit(app.exec_())




