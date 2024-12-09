#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: wspr-tx
# Author: Aaron Heller
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
import math
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip
import threading



class wspr_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "wspr-tx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("wspr-tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "wspr_tx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rf = samp_rate_rf = 2e6
        self.samp_rate = samp_rate = 12000
        self.wspr_gain_dB = wspr_gain_dB = 40
        self.interpolation_rate = interpolation_rate = samp_rate_rf/samp_rate
        self.dial_frequency = dial_frequency = 28124.6e3
        self.wspr_offset = wspr_offset = 0
        self.rf_gain = rf_gain = 40
        self.rf_freq_offset = rf_freq_offset = 1
        self.rf_amp = rf_amp = 0
        self.low_pass_filter_taps = low_pass_filter_taps = firdes.low_pass(10**(wspr_gain_dB/20), samp_rate_rf, samp_rate_rf/(interpolation_rate*2),samp_rate_rf/(interpolation_rate*4), window.WIN_HAMMING, 6.76)
        self.display = display = dial_frequency

        ##################################################
        # Blocks
        ##################################################

        self._wspr_offset_range = qtgui.Range(-100, +100, 1, 0, 200)
        self._wspr_offset_win = qtgui.RangeWidget(self._wspr_offset_range, self.set_wspr_offset, "WSPR Offset [Hz]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._wspr_offset_win)
        self._rf_gain_range = qtgui.Range(0, 47, 1, 40, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "'rf_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        self._rf_amp_choices = {'Pressed': 1, 'Released': 0}

        _rf_amp_toggle_button = qtgui.ToggleButton(self.set_rf_amp, 'RF Amp +14', self._rf_amp_choices, False, 'value')
        _rf_amp_toggle_button.setColors("default", "default", "default", "default")
        self.rf_amp = _rf_amp_toggle_button

        self.top_layout.addWidget(_rf_amp_toggle_button)
        # Create the options list
        self._dial_frequency_options = [28124600.0, 21094600.0, 14095600.0]
        # Create the labels list
        self._dial_frequency_labels = ['10m', '15m', '20m']
        # Create the combo box
        self._dial_frequency_tool_bar = Qt.QToolBar(self)
        self._dial_frequency_tool_bar.addWidget(Qt.QLabel("'dial_frequency'" + ": "))
        self._dial_frequency_combo_box = Qt.QComboBox()
        self._dial_frequency_tool_bar.addWidget(self._dial_frequency_combo_box)
        for _label in self._dial_frequency_labels: self._dial_frequency_combo_box.addItem(_label)
        self._dial_frequency_callback = lambda i: Qt.QMetaObject.invokeMethod(self._dial_frequency_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._dial_frequency_options.index(i)))
        self._dial_frequency_callback(self.dial_frequency)
        self._dial_frequency_combo_box.currentIndexChanged.connect(
            lambda i: self.set_dial_frequency(self._dial_frequency_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._dial_frequency_tool_bar)
        self._wspr_gain_dB_range = qtgui.Range(20, 60, 1, 40, 200)
        self._wspr_gain_dB_win = qtgui.RangeWidget(self._wspr_gain_dB_range, self.set_wspr_gain_dB, "WSPR Gain [dB]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._wspr_gain_dB_win)
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate_rf)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, (dial_frequency -rf_freq_offset))
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', rf_amp)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(rf_gain, 0.0), 47.0))
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(int(interpolation_rate), low_pass_filter_taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self._display_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Dial Freq', min_freq_hz=0, max_freq_hz=30e6, parent=self, thousands_separator=",", background_color="black", fontColor="white", var_callback=self.set_display, outputmsgname='freq')
        self._display_msgdigctl_win.setValue(dial_frequency)
        self._display_msgdigctl_win.setReadOnly(False)
        self.display = self._display_msgdigctl_win

        self.top_layout.addWidget(self._display_msgdigctl_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('wspr.wav', True)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*(rf_freq_offset+wspr_offset)/samp_rate)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_freqshift_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "wspr_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate_rf(self):
        return self.samp_rate_rf

    def set_samp_rate_rf(self, samp_rate_rf):
        self.samp_rate_rf = samp_rate_rf
        self.set_interpolation_rate(self.samp_rate_rf/self.samp_rate)
        self.set_low_pass_filter_taps(firdes.low_pass(10**(self.wspr_gain_dB/20), self.samp_rate_rf, self.samp_rate_rf/(self.interpolation_rate*2), self.samp_rate_rf/(self.interpolation_rate*4), window.WIN_HAMMING, 6.76))
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate_rf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_interpolation_rate(self.samp_rate_rf/self.samp_rate)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.rf_freq_offset+self.wspr_offset)/self.samp_rate)

    def get_wspr_gain_dB(self):
        return self.wspr_gain_dB

    def set_wspr_gain_dB(self, wspr_gain_dB):
        self.wspr_gain_dB = wspr_gain_dB
        self.set_low_pass_filter_taps(firdes.low_pass(10**(self.wspr_gain_dB/20), self.samp_rate_rf, self.samp_rate_rf/(self.interpolation_rate*2), self.samp_rate_rf/(self.interpolation_rate*4), window.WIN_HAMMING, 6.76))

    def get_interpolation_rate(self):
        return self.interpolation_rate

    def set_interpolation_rate(self, interpolation_rate):
        self.interpolation_rate = interpolation_rate
        self.set_low_pass_filter_taps(firdes.low_pass(10**(self.wspr_gain_dB/20), self.samp_rate_rf, self.samp_rate_rf/(self.interpolation_rate*2), self.samp_rate_rf/(self.interpolation_rate*4), window.WIN_HAMMING, 6.76))

    def get_dial_frequency(self):
        return self.dial_frequency

    def set_dial_frequency(self, dial_frequency):
        self.dial_frequency = dial_frequency
        self._dial_frequency_callback(self.dial_frequency)
        self._display_msgdigctl_win.setValue(self.dial_frequency)
        self.soapy_hackrf_sink_0.set_frequency(0, (self.dial_frequency -self.rf_freq_offset))

    def get_wspr_offset(self):
        return self.wspr_offset

    def set_wspr_offset(self, wspr_offset):
        self.wspr_offset = wspr_offset
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.rf_freq_offset+self.wspr_offset)/self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(self.rf_gain, 0.0), 47.0))

    def get_rf_freq_offset(self):
        return self.rf_freq_offset

    def set_rf_freq_offset(self, rf_freq_offset):
        self.rf_freq_offset = rf_freq_offset
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.rf_freq_offset+self.wspr_offset)/self.samp_rate)
        self.soapy_hackrf_sink_0.set_frequency(0, (self.dial_frequency -self.rf_freq_offset))

    def get_rf_amp(self):
        return self.rf_amp

    def set_rf_amp(self, rf_amp):
        self.rf_amp = rf_amp
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', self.rf_amp)

    def get_low_pass_filter_taps(self):
        return self.low_pass_filter_taps

    def set_low_pass_filter_taps(self, low_pass_filter_taps):
        self.low_pass_filter_taps = low_pass_filter_taps
        self.interp_fir_filter_xxx_0.set_taps(self.low_pass_filter_taps)

    def get_display(self):
        return self.display

    def set_display(self, display):
        self.display = display




def main(top_block_cls=wspr_tx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
