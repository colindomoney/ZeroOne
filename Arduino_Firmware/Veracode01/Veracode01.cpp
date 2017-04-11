#include "FastLED.h"
#include "Veracode01.h"

static int _numLEDs = 0;
static CRGB *_leds = NULL;

void Veracode01_Setup(int numLEDs, CRGB *leds)
{
  _numLEDs = numLEDs;
  _leds = leds;
}

#define FADE_DELAY 50

void Veracode01_Fade(CRGB colour, int fromBrightness, int toBrightness, int duration)
{
    int _timeSteps = duration/FADE_DELAY;
    int _brightnessStep = (toBrightness - fromBrightness)/_timeSteps;
    int brightness = fromBrightness;

    Veracode01_ShowAll(colour, fromBrightness);

    for (int i = 0; i <= _timeSteps; i++, brightness += _brightnessStep)
    {
        Veracode01_ShowAll(colour, brightness);
        delay(FADE_DELAY);
    }

    Veracode01_ShowAll(colour, toBrightness);    
}

void Veracode01_BlankAll()
{
  SetAllLEDs(CRGB::Black);  
  FastLED.show();
}

void Veracode01_ShowAll(CRGB colour, int brightness)
{
  SetAllLEDs(colour);
  FastLED.setBrightness(brightness);
  FastLED.show();
}

void Do(CRGB colour)
{
    SetAllLEDs(colour);
    FastLED.show();
    delay(DELAY);
}

void SetAllLEDs(CRGB colour)
{
  for (int i = 0; i < _numLEDs; i++)
  {
    *(_leds + i) = colour;
  }  
}