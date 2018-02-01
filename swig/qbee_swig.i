/* -*- c++ -*- */

#define QBEE_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "qbee_swig_doc.i"

%{
#include "qbee/qbee_demodulator_fsk.h"
#include "qbee/qbee_nrzi_decoder.h"
#include "qbee/qbee_deframer.h"
#include "qbee/qbee_segmentor.h"
%}


%include "qbee/qbee_demodulator_fsk.h"
GR_SWIG_BLOCK_MAGIC2(qbee, qbee_demodulator_fsk);
%include "qbee/qbee_nrzi_decoder.h"
GR_SWIG_BLOCK_MAGIC2(qbee, qbee_nrzi_decoder);
%include "qbee/qbee_deframer.h"
GR_SWIG_BLOCK_MAGIC2(qbee, qbee_deframer);
%include "qbee/qbee_segmentor.h"
GR_SWIG_BLOCK_MAGIC2(qbee, qbee_segmentor);
