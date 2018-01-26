#include "FastLED.h"

// How many leds in your strip?
#define NUM_LEDS 1000
#define DELAY 250

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 3
#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    FastLED.setBrightness(50);
}

void loop() {
    // put your main code here, to run repeatedly:
    Do(CRGB::Red);
    delay(DELAY);
    Do(CRGB::White);
    delay(DELAY);
}

void Do(CRGB colour)
{
    SetLEDs(colour);
    FastLED.show();
    delay(DELAY);
}

void SetLEDs(CRGB colour)
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = colour;
  }  
}

