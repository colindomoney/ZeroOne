#include "FastLED.h"
#include "Veracode01.h"

// How many leds in your strip?
#define NUM_LEDS 750

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 3
#define CLOCK_PIN 13

#define BRIGHTNESS_MIN 0
#define BRIGHTNESS_MAX 164
#define FADE_DELAY 800

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
    Veracode01_Setup(NUM_LEDS, leds);
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    FastLED.setBrightness(0);
}

void loop() {

    //Veracode01_ShowAll(CRGB::White, 164);
    //delay(4000);
    
    DoColour(CRGB::Red);
    DoColour(CRGB::White);
    DoColour(CRGB::Blue);
    DoColour(CRGB::Green);
    DoColour(CRGB::Purple);

    Veracode01_BlankAll();
    delay(100);

}
    
void DoColour(CRGB colour)
{
    Veracode01_Fade(colour, BRIGHTNESS_MIN, BRIGHTNESS_MAX, FADE_DELAY);
    Veracode01_Fade(colour, BRIGHTNESS_MAX, BRIGHTNESS_MIN, FADE_DELAY);
    delay(50);
}

