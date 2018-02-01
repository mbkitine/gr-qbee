#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Reed-Solomon Testing
# Author: Moses Browne Mwakyanjala
# Generated: Thu Feb  1 15:45:44 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import qbee
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Reed-Solomon Testing")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Reed-Solomon Testing")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.qbee_qbee_segmentor_0 = qbee.qbee_segmentor(81)
        self.qbee_qbee_deframer_0 = qbee.qbee_deframer(32, 500)
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb('')
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", '', '5001', 10000, False)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/mbkitine/Dropbox/Lulea/GRC/qbee/gr-qbee/examples/qbee_packets/qbee.bin', True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qbee_qbee_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.qbee_qbee_deframer_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.qbee_qbee_segmentor_0, 'out'), (self.digital_hdlc_framer_pb_0, 'in'))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qbee_qbee_segmentor_0, 0))
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.qbee_qbee_deframer_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
