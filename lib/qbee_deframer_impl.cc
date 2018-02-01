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
#include "qbee_deframer_impl.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "rs_decode.h"
namespace gr {
  namespace qbee {

    qbee_deframer::sptr
    qbee_deframer::make(int length_min,int length_max)
    {
      return gnuradio::get_initial_sptr
        (new qbee_deframer_impl(length_min, length_max));
    }

    /*
     * The private constructor
     */
    qbee_deframer_impl::qbee_deframer_impl(int length_min = 32,int length_max = 500)
      : gr::sync_block("qbee_deframer",
		       gr::io_signature::make(1, 1, sizeof(unsigned char)),
		       gr::io_signature::make(0, 0, 0)),
	d_length_min(length_min),
        d_length_max(length_max)
    {
      set_output_multiple(length_max*2);
      message_port_register_out(pmt::mp("out"));
      d_bytectr=0;
      d_bitctr=0;
      d_ones=0;
      d_pktbuf = new unsigned char[length_max+2];
      d_icdbuf = new unsigned char[length_max+2+4+1];
      d_rsbuf  = new unsigned char[length_max];
    }

    inline void extract_rs(unsigned char *ax25_with_crc,unsigned char *ax25_without_crc,int len)
    {
      for(int i = 16; i <len-2;i++)
	{
	  ax25_without_crc[i] = ax25_with_crc[i];
	}
      return;
    }
    
    inline void icd_wrapper(unsigned char *icd_pkt, unsigned char *buf_pkt, int len)
    {
      unsigned char size = len & 0xFF;
      const unsigned int sync_word = 0x1DFCCF1A;
      memcpy(&icd_pkt[0], &sync_word, 4);
      memcpy(&icd_pkt[4], &size, 1);
      for(int i = 0; i <len;i++)
	{
	  icd_pkt[i+5] = buf_pkt[i];
	}
      return;
    }
    
    //Hexdump function : For debugging 
    inline void hexdump(void *ptr, int buflen) {
      unsigned char *buf = (unsigned char*) ptr;
      int i, j;
      for (i = 0; i < buflen; i += 16) {
	printf("%06x: ", i);
	for (j = 0; j < 16; j++)
	  if (i + j < buflen)
	    printf("%02x ", buf[i + j]);
	  else
	    printf("   ");
	printf(" ");
	for (j = 0; j < 16; j++)
	  if (i + j < buflen)
	    printf("%c", isprint(buf[i + j]) ? buf[i + j] : '.');
	printf("\n");
      }
    }
    /*
     * Our virtual destructor.
     */
    qbee_deframer_impl::~qbee_deframer_impl()
    {
      delete[] d_pktbuf;
      delete[] d_icdbuf;
      delete[] d_rsbuf;
    }

    int
    qbee_deframer_impl::work(int noutput_items,
			     gr_vector_const_void_star &input_items,
			     gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char bit;
      int n=0;
      int rs_res;
      
      unsigned char size;
      //memset(d_icdbuf,0x00,d_length_max);
      while (n < noutput_items) {
	bit=*in;
	if(d_ones>=5) {
	  if(bit) { //six ones is a frame delimiter
	    if(d_bytectr >= d_length_min) {
	      //Error control coding, packet forwarding
		      
	      int len = d_bytectr; //make Coverity happy

	      //Extracting RS codeword by stripping AX.25 header and CRC
	      extract_rs(d_pktbuf,d_rsbuf,len);
	      len -=(2 + 16);
	      hexdump(d_rsbuf,len);
	      //ICD wrapper
	      // icd_wrapper(d_icdbuf,d_pktbuf,len);
	      
	      rs_res = decode_rs_8(&d_rsbuf[0], NULL, 0, 255 - len + 1);
	      printf("\n Result= %d\n",rs_res);
	      if (rs_res >= 0)
		{
		  pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL,
					   pmt::make_blob(d_rsbuf, len)));//len - 32
		  message_port_pub(pmt::mp("out"), pdu);
		}
			  
	    } else {
	    }
	    d_bitctr=0;
	    d_bytectr=0;
	  } else { //unstuff
	  }
	} else { //not 5+ continuous ones
	  if(d_bytectr > d_length_max) {
	    d_bytectr=0;
	    d_bitctr=0;
	  } else {
	    d_pktbuf[d_bytectr]>>=1;
	    if (bit) d_pktbuf[d_bytectr] |= 0x80;
	    d_bitctr++;
	    if (d_bitctr==8) {
	      d_bitctr=0;
	      d_bytectr++;
	    }
	  }
	}
	d_ones = (bit) ? d_ones+1 : 0;
	in++;
	n++;
      }
      return n;
    }

  } /* namespace qbee */
} /* namespace gr */

