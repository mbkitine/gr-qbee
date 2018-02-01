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
#include "qbee_demodulator_fsk_impl.h"
#include <math.h>
#include <gnuradio/analog/quadrature_demod_cf.h>
namespace gr {
  namespace qbee {

    qbee_demodulator_fsk::sptr
    qbee_demodulator_fsk::make(float sps, float modulation_index)
    {
      return gnuradio::get_initial_sptr
        (new qbee_demodulator_fsk_impl(sps, modulation_index));
    }

    /*
     * The private constructor
     */
    qbee_demodulator_fsk_impl::qbee_demodulator_fsk_impl(float sps, float modulation_index)
      : gr::hier_block2("qbee_demodulator_fsk",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(float)))
    {
      //Calculating quadrature demod gain
      float gain = sps/(M_PI*modulation_index);
      gr::analog::quadrature_demod_cf::sptr fm(gr::analog::quadrature_demod_cf::make(gain));
      
      connect(self(), 0, fm, 0);
      // connect other blocks
      connect(fm, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    qbee_demodulator_fsk_impl::~qbee_demodulator_fsk_impl()
    {
    }


  } /* namespace qbee */
} /* namespace gr */

