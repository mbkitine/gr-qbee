/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
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
#include "qbee_segmentor_impl.h"

namespace gr {
  namespace qbee {

    qbee_segmentor::sptr
    qbee_segmentor::make(int frame_length)
    {
      return gnuradio::get_initial_sptr
        (new qbee_segmentor_impl(frame_length));
    }

    /*
     * The private constructor
     */
    qbee_segmentor_impl::qbee_segmentor_impl(int frame_length)
      : gr::sync_block("qbee_segmentor",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
		       gr::io_signature::make(0, 0, 0)),
	d_frame_length(frame_length)
    {
      set_output_multiple(d_frame_length);

      //Registering output port
      message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    qbee_segmentor_impl::~qbee_segmentor_impl()
    {
    }

    int
    qbee_segmentor_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      int n = 0;
      byte frame;
      while (n < noutput_items)
	{
	  //Storing bits into an array
	  frame.push_back(*in);
    	
	  if (n == d_frame_length - 1)
	    {
	      //Inserting sync marker
	      pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL,pmt::make_blob(frame.data(),
								   frame.size())));
	      message_port_pub(pmt::mp("out"), pdu);
	      frame.clear();
	    }
	  in++;
	  n++;
    	}
      // Tell runtime system how many output items we produced.
      return n;
    }

  } /* namespace qbee */
} /* namespace gr */

