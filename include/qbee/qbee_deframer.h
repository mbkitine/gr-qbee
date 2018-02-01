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


#ifndef INCLUDED_QBEE_QBEE_DEFRAMER_H
#define INCLUDED_QBEE_QBEE_DEFRAMER_H

#include <qbee/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace qbee {

    /*!
     * \brief <+description of block+>
     * \ingroup qbee
     *
     */
    class QBEE_API qbee_deframer : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<qbee_deframer> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of qbee::qbee_deframer.
       *
       * To avoid accidental use of raw pointers, qbee::qbee_deframer's
       * constructor is in a private implementation
       * class. qbee::qbee_deframer::make is the public interface for
       * creating new instances.
       */
      static sptr make(int length_min=32,int length_max=500);
    };

  } // namespace qbee
} // namespace gr

#endif /* INCLUDED_QBEE_QBEE_DEFRAMER_H */

