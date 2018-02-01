#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Mode 6 Debug
# Generated: Mon Jan  8 17:03:56 2018
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math,cmath
import nwr
import qbee
import wx


class Mode_6_Debug(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Mode 6 Debug")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.zeta = zeta = 0.7
        self.loop_bw = loop_bw = 0.01
        self.baud_rate = baud_rate = 9600
        self.sps = sps = 5
        self.p_squelch = p_squelch = -100
        self.nfilts = nfilts = 32
        self.mod_index = mod_index = 1/1.5
        self.gain_ant = gain_ant = 30
        self.filter_fc = filter_fc = 1000
        self.filter_bw = filter_bw = baud_rate/2
        self.filter_attenuation = filter_attenuation = 40
        self.denom = denom = (1.0 + 2.0*zeta*loop_bw + loop_bw*loop_bw)
        self.dec = dec = 1
        self.alpha_0 = alpha_0 = 2*math.exp(-zeta*loop_bw)*math.sinh(zeta*loop_bw)
        self.xlating_fc = xlating_fc = filter_fc
        self.xlating_bw = xlating_bw = filter_bw
        self.xlating_attn = xlating_attn = filter_attenuation
        self.squelch = squelch = p_squelch
        self.samp_rate = samp_rate = baud_rate*sps*dec
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, sps, 1.0/float(sps), 0.35, 25*nfilts)
        self.preamble = preamble = '011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110011111100111111001111110'
        self.gf_taps = gf_taps = firdes.gaussian(1,1.0/float(sps),0.35,nfilts*45)
        self.gaussian_taps = gaussian_taps = firdes.gaussian(nfilts, 1.0/float(sps), 0.35, 45*nfilts)
        self.gain = gain = gain_ant
        self.freq = freq = 436.8e6 - 1e6
        self.cut_off = cut_off = baud_rate*(mod_index + 1)
        self.beta_0 = beta_0 = 2 - alpha_0 - math.exp(-zeta*loop_bw)
        self.beta = beta = (4*loop_bw*loop_bw)/denom
        self.alpha = alpha = (4*loop_bw*zeta)/denom

        ##################################################
        # Blocks
        ##################################################
        _xlating_bw_sizer = wx.BoxSizer(wx.VERTICAL)
        self._xlating_bw_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_xlating_bw_sizer,
        	value=self.xlating_bw,
        	callback=self.set_xlating_bw,
        	label='Transition bandwidth',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._xlating_bw_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_xlating_bw_sizer,
        	value=self.xlating_bw,
        	callback=self.set_xlating_bw,
        	minimum=100,
        	maximum=baud_rate,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_xlating_bw_sizer)
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "RX signal")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Filtered Signal")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "PFB")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Binary")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "TX signal")
        self.Add(self.notebook_0)
        _xlating_fc_sizer = wx.BoxSizer(wx.VERTICAL)
        self._xlating_fc_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_xlating_fc_sizer,
        	value=self.xlating_fc,
        	callback=self.set_xlating_fc,
        	label='Filter Fc',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._xlating_fc_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_xlating_fc_sizer,
        	value=self.xlating_fc,
        	callback=self.set_xlating_fc,
        	minimum=-10000,
        	maximum=10000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_xlating_fc_sizer)
        _xlating_attn_sizer = wx.BoxSizer(wx.VERTICAL)
        self._xlating_attn_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_xlating_attn_sizer,
        	value=self.xlating_attn,
        	callback=self.set_xlating_attn,
        	label='Filter Attenuation',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._xlating_attn_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_xlating_attn_sizer,
        	value=self.xlating_attn,
        	callback=self.set_xlating_attn,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_xlating_attn_sizer)
        self.wxgui_fftsink2_4 = fftsink2.fft_sink_f(
        	self.notebook_0.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/5,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        	win=window.blackmanharris,
        )
        self.notebook_0.GetPage(2).Add(self.wxgui_fftsink2_4.win)
        self.wxgui_fftsink2_3 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/dec,
        	fft_size=64,
        	fft_rate=5,
        	average=False,
        	avg_alpha=None,
        	title='Filtered Signal',
        	peak_hold=True,
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_fftsink2_3.win)
        self.wxgui_fftsink2_2 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=20,
        	average=False,
        	avg_alpha=None,
        	title='RX Signal',
        	peak_hold=False,
        	win=window.hamming,
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_2.win)
        _squelch_sizer = wx.BoxSizer(wx.VERTICAL)
        self._squelch_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	label='squelch',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._squelch_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	minimum=-120,
        	maximum=0,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_squelch_sizer)
        self.qbee_qbee_nrzi_decoder_0 = qbee.qbee_nrzi_decoder()
        self.qbee_qbee_demodulator_fsk_0 = qbee.qbee_demodulator_fsk(sps, mod_index)
        self.qbee_qbee_deframer_0 = qbee.qbee_deframer(32, 500)
        self.nwr_symbol_sync_xx_0 = nwr.symbol_sync_ff(nwr.timing_error_detector.TED_MENGALI_AND_DANDREA_GMSK, sps, 0.02, 1.0, 1.5, 1, digital.constellation_bpsk().base(), nwr.interpolating_resampler.IR_MMSE_8TAP, 128, ([]))
        self.low_pass_filter_0 = filter.fir_filter_ccf(dec, firdes.low_pass(
        	1, samp_rate, cut_off, xlating_bw, firdes.WIN_HAMMING, 6.76))
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=70,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(12, (1, ))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, 0.9, 44, 0.0005)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0x000000, 16)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_udp_sink_1 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 5002, 1000, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*12,True)
        self.blocks_socket_pdu_1 = blocks.socket_pdu("UDP_SERVER", '', '5001', 10000, False)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/mbkitine/Desktop/Signals/mode6-576000.bin', False)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qbee_qbee_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.qbee_qbee_deframer_0, 'out'), (self.blocks_socket_pdu_1, 'pdus'))
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_udp_sink_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.qbee_qbee_nrzi_decoder_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.wxgui_fftsink2_3, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.wxgui_fftsink2_2, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qbee_qbee_demodulator_fsk_0, 0))
        self.connect((self.nwr_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.nwr_symbol_sync_xx_0, 0), (self.wxgui_fftsink2_4, 0))
        self.connect((self.qbee_qbee_demodulator_fsk_0, 0), (self.nwr_symbol_sync_xx_0, 0))
        self.connect((self.qbee_qbee_nrzi_decoder_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.qbee_qbee_nrzi_decoder_0, 0), (self.qbee_qbee_deframer_0, 0))

    def get_zeta(self):
        return self.zeta

    def set_zeta(self, zeta):
        self.zeta = zeta
        self.set_denom((1.0 + 2.0*self.zeta*self.loop_bw + self.loop_bw*self.loop_bw))
        self.set_beta_0(2 - self.alpha_0 - math.exp(-self.zeta*self.loop_bw))
        self.set_alpha_0(2*math.exp(-self.zeta*self.loop_bw)*math.sinh(self.zeta*self.loop_bw))
        self.set_alpha((4*self.loop_bw*self.zeta)/self.denom)

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.set_denom((1.0 + 2.0*self.zeta*self.loop_bw + self.loop_bw*self.loop_bw))
        self.set_beta_0(2 - self.alpha_0 - math.exp(-self.zeta*self.loop_bw))
        self.set_beta((4*self.loop_bw*self.loop_bw)/self.denom)
        self.set_alpha_0(2*math.exp(-self.zeta*self.loop_bw)*math.sinh(self.zeta*self.loop_bw))
        self.set_alpha((4*self.loop_bw*self.zeta)/self.denom)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(self.baud_rate*self.sps*self.dec)
        self.set_cut_off(self.baud_rate*(self.mod_index + 1))
        self.set_filter_bw(self.baud_rate/2)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(self.baud_rate*self.sps*self.dec)
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.sps, 1.0/float(self.sps), 0.35, 25*self.nfilts))
        self.set_gf_taps(firdes.gaussian(1,1.0/float(self.sps),0.35,self.nfilts*45))
        self.set_gaussian_taps(firdes.gaussian(self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))

    def get_p_squelch(self):
        return self.p_squelch

    def set_p_squelch(self, p_squelch):
        self.p_squelch = p_squelch
        self.set_squelch(self.p_squelch)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.sps, 1.0/float(self.sps), 0.35, 25*self.nfilts))
        self.set_gf_taps(firdes.gaussian(1,1.0/float(self.sps),0.35,self.nfilts*45))
        self.set_gaussian_taps(firdes.gaussian(self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))

    def get_mod_index(self):
        return self.mod_index

    def set_mod_index(self, mod_index):
        self.mod_index = mod_index
        self.set_cut_off(self.baud_rate*(self.mod_index + 1))

    def get_gain_ant(self):
        return self.gain_ant

    def set_gain_ant(self, gain_ant):
        self.gain_ant = gain_ant
        self.set_gain(self.gain_ant)

    def get_filter_fc(self):
        return self.filter_fc

    def set_filter_fc(self, filter_fc):
        self.filter_fc = filter_fc
        self.set_xlating_fc(self.filter_fc)

    def get_filter_bw(self):
        return self.filter_bw

    def set_filter_bw(self, filter_bw):
        self.filter_bw = filter_bw
        self.set_xlating_bw(self.filter_bw)

    def get_filter_attenuation(self):
        return self.filter_attenuation

    def set_filter_attenuation(self, filter_attenuation):
        self.filter_attenuation = filter_attenuation
        self.set_xlating_attn(self.filter_attenuation)

    def get_denom(self):
        return self.denom

    def set_denom(self, denom):
        self.denom = denom
        self.set_beta((4*self.loop_bw*self.loop_bw)/self.denom)
        self.set_alpha((4*self.loop_bw*self.zeta)/self.denom)

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.set_samp_rate(self.baud_rate*self.sps*self.dec)
        self.wxgui_fftsink2_3.set_sample_rate(self.samp_rate/self.dec)

    def get_alpha_0(self):
        return self.alpha_0

    def set_alpha_0(self, alpha_0):
        self.alpha_0 = alpha_0
        self.set_beta_0(2 - self.alpha_0 - math.exp(-self.zeta*self.loop_bw))

    def get_xlating_fc(self):
        return self.xlating_fc

    def set_xlating_fc(self, xlating_fc):
        self.xlating_fc = xlating_fc
        self._xlating_fc_slider.set_value(self.xlating_fc)
        self._xlating_fc_text_box.set_value(self.xlating_fc)

    def get_xlating_bw(self):
        return self.xlating_bw

    def set_xlating_bw(self, xlating_bw):
        self.xlating_bw = xlating_bw
        self._xlating_bw_slider.set_value(self.xlating_bw)
        self._xlating_bw_text_box.set_value(self.xlating_bw)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_off, self.xlating_bw, firdes.WIN_HAMMING, 6.76))

    def get_xlating_attn(self):
        return self.xlating_attn

    def set_xlating_attn(self, xlating_attn):
        self.xlating_attn = xlating_attn
        self._xlating_attn_slider.set_value(self.xlating_attn)
        self._xlating_attn_text_box.set_value(self.xlating_attn)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self._squelch_slider.set_value(self.squelch)
        self._squelch_text_box.set_value(self.squelch)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_4.set_sample_rate(self.samp_rate/5)
        self.wxgui_fftsink2_3.set_sample_rate(self.samp_rate/self.dec)
        self.wxgui_fftsink2_2.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_off, self.xlating_bw, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*12)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_gf_taps(self):
        return self.gf_taps

    def set_gf_taps(self, gf_taps):
        self.gf_taps = gf_taps

    def get_gaussian_taps(self):
        return self.gaussian_taps

    def set_gaussian_taps(self, gaussian_taps):
        self.gaussian_taps = gaussian_taps

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_cut_off(self):
        return self.cut_off

    def set_cut_off(self, cut_off):
        self.cut_off = cut_off
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cut_off, self.xlating_bw, firdes.WIN_HAMMING, 6.76))

    def get_beta_0(self):
        return self.beta_0

    def set_beta_0(self, beta_0):
        self.beta_0 = beta_0

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha


def main(top_block_cls=Mode_6_Debug, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
