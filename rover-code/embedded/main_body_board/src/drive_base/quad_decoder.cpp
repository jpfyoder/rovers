#include "../../include/quad_decoder.h"


QuadratureDecoder* QuadratureDecoder::instance = nullptr;

QuadratureDecoder::QuadratureDecoder(enc_A_pins enc_A_pin, enc_B_pins enc_B_pin) : m_encoder(enc_A_pin, enc_B_pin), m_count(0), enc_A_pin(enc_A_pin), enc_B_pin(enc_B_pin) {
  instance = this;
}

void QuadratureDecoder::begin() {
  m_encoder.write(0);
  IntervalTimer timer;
  timer.begin([]() { updateCount(); }, 1000);  // Update count every 1000 microseconds
}

long QuadratureDecoder::getCount() {
  return instance->m_count;
}

void QuadratureDecoder::updateCount() {
  instance->m_count += instance->m_encoder.read();
  instance->m_encoder.write(0);
}