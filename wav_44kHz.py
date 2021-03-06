#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: WAV 44.1KHz file streamer 
# Author: Daniel Estevez
# Description: Streams a WAV 44.1kHz file
# Generated: Fri Jan 20 12:37:53 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class wav_44kHz(gr.top_block):

    def __init__(self, destination='localhost', input_file='', port=7355):
        gr.top_block.__init__(self, "WAV 44.1KHz file streamer ")

        ##################################################
        # Parameters
        ##################################################
        self.destination = destination
        self.input_file = input_file
        self.port = port

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=160,
                decimation=147,
                taps=None,
                fractional_bw=None,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, 48000,True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_udp_sink_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_float_to_short_0, 0))    

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_input_file(self):
        return self.input_file

    def set_input_file(self, input_file):
        self.input_file = input_file

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port


def argument_parser():
    description = 'Streams a WAV 44.1kHz file'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--destination", dest="destination", type="string", default='localhost',
        help="Set localhost [default=%default]")
    parser.add_option(
        "-f", "--input-file", dest="input_file", type="string", default='',
        help="Set file [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set port [default=%default]")
    return parser


def main(top_block_cls=wav_44kHz, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(destination=options.destination, input_file=options.input_file, port=options.port)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
