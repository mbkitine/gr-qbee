/* -*- c++ -*- */
/* 
 * Copyright 2017 Moses Browne Mwakyanjala.
 * E-mail: moses.browne.mwakyanjala@ltu.se
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "qbee_nrzi_decoder_impl.h"
#include <gnuradio/digital/diff_decoder_bb.h>
#include <gnuradio/blocks/not_bb.h>
#include <gnuradio/blocks/and_const_bb.h>
namespace gr {
  namespace qbee {

    qbee_nrzi_decoder::sptr
    qbee_nrzi_decoder::make()
    {
      return gnuradio::get_initial_sptr
        (new qbee_nrzi_decoder_impl());
    }

    /*
     * The private constructor
     */
    qbee_nrzi_decoder_impl::qbee_nrzi_decoder_impl()
      : gr::hier_block2("qbee_nrzi_decoder",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      /*
	Implementing NRZ-I decoder as a concatenation of a differential decoder and 
        an inverter (not + and const) 
       */
      //Differential decoder
      gr::digital::diff_decoder_bb::sptr diff(gr::digital::diff_decoder_bb::make(2));
      
      //Not
      gr::blocks::not_bb::sptr negate(gr::blocks::not_bb::make(1));

      //And const
      gr::blocks::and_const_bb::sptr logical_and(gr::blocks::and_const_bb::make(0x01));

      //Connecting blocks
      connect(self(), 0, diff, 0);
      connect(diff, 0, negate, 0);
      connect(negate, 0, logical_and, 0);
      connect(logical_and, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    qbee_nrzi_decoder_impl::~qbee_nrzi_decoder_impl()
    {
    }


  } /* namespace qbee */
} /* namespace gr */

