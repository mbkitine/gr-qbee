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
      d_ax25headerbuf = new unsigned char[16];
    }

    inline void rs_dewrapper(unsigned char *ax25_pkt,unsigned char *ax25_header, unsigned char* rs_pkt, int len)
    {
      int index = 0;
      
      //Extracting ax_25 header
      memcpy(&ax25_header[0],&ax25_pkt[0],16);

      //Extracting rs_pkt
      memcpy(&rs_pkt[0], &ax25_pkt[16], len - (16 + 2));
      /*
	for(int i = 16; i <len-2;i++)
	{
	ax25_without_crc[i-16] = ax25_with_crc[i];
	}*/
      return;
    }
    
    inline void icd_wrapper(unsigned char *icd_pkt, unsigned char *ax25_header_pkt,
			    unsigned char *rs_pkt, int rs_pkt_len,int errors,int &total_frame_length)
    {
      /*ICD packet
	-------------------------------------------------------------------------------
	| SYNC WORD (4) | lENGTH (1) | ERRORS_CORRECTED (1) | DATA(X) |
	-------------------------------------------------------------------------------
      */
      int index = 0;
      //Inserting SYNC WORD (4 Bytes)
      const unsigned int sync_word = 0x1DFCCF1A;
      memcpy(&icd_pkt[index], &sync_word, 4);
      index += 4;

      //Inserting frame LENGTH (1 Byte)
      unsigned char size = (rs_pkt_len + 16 + 1) & 0xFF;
      memcpy(&icd_pkt[index], &size, 1);
      index += 1;

      //Inserting number of errors corrected by RS decoder
      unsigned char d_errors = errors & 0xFF;
      memcpy(&icd_pkt[index], &d_errors, 1);
      index += 1;

      //Inserting AX.25 header field
      memcpy(&icd_pkt[index], &ax25_header_pkt[0], 16);
      index += 16;

      //Inserting data
      memcpy(&icd_pkt[index],&rs_pkt[0], rs_pkt_len);

      //Calculating total frame length
      total_frame_length = 4 + 1 + 1 + 16 + rs_pkt_len;
      
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
      delete[] d_ax25headerbuf;
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
      int d_icdbuf_len;
      
      unsigned char size;
      //memset(d_icdbuf,0x00,d_length_max);
      while (n < noutput_items) {
	bit=*in;
	if(d_ones>=5) {
	  if(bit) { //six ones is a frame delimiter
	    if(d_bytectr >= d_length_min) {
	      //Error control coding, packet forwarding
		      
	      int len    = d_bytectr; //make Coverity happy
	      int rs_len = len - (2 + 16); // length of RS codeword after removing AX25 header and CRC

	      //Extracting RS codeword by stripping AX.25 header and CRC
	      rs_dewrapper(d_pktbuf,d_ax25headerbuf, d_rsbuf,len);
	      
	      //extract_rs(d_pktbuf,d_rsbuf,len);
	      //len -= (2 + 16) ;
	      //printf("AX.25 header\n");
	      //hexdump(d_ax25headerbuf,16);
	      //printf("RS codeword\n");
	      //hexdump(d_rsbuf,rs_len);
	      
	      //ICD wrapper
	      // icd_wrapper(d_icdbuf,d_pktbuf,len);

	      //Reed-Solomon decoding
	      rs_res = decode_rs_8(&d_rsbuf[0], NULL, 0, 255 - rs_len + 1);
	     
	      if (rs_res >= 0)
		{
		  printf("\n Reed solomon errors corrected = %d\n",rs_res);
		  //ICD wrapper
		  icd_wrapper(d_icdbuf,d_ax25headerbuf,d_rsbuf,rs_len - 32,rs_res,d_icdbuf_len);
		  pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL,
					   pmt::make_blob(d_icdbuf, d_icdbuf_len)));
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

