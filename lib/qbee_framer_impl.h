/* -*- c++ -*- */
/* 
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_QBEE_QBEE_FRAMER_IMPL_H
#define INCLUDED_QBEE_QBEE_FRAMER_IMPL_H

#include <qbee/qbee_framer.h>
#include <pmt/pmt.h>
namespace gr {
  namespace qbee {

    class qbee_framer_impl : public qbee_framer
    {
     private:
      std::vector<std::vector<unsigned char> > d_leftovers;
        pmt::pmt_t d_frame_tag, d_me;
        unsigned int crc_ccitt(std::vector<unsigned char> &data);
        std::vector<unsigned char> unpack(std::vector<unsigned char> &pkt);
        void stuff(std::vector<unsigned char> &pkt);
        void rs_encode(std::vector<unsigned char> &pkt);

     public:
      qbee_framer_impl(const std::string frame_tag_name);
      ~qbee_framer_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace qbee
} // namespace gr

#endif /* INCLUDED_QBEE_QBEE_FRAMER_IMPL_H */

