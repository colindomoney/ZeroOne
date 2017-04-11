#define DELAY 250

void Veracode01_Setup(int numLEDs, CRGB *leds);
void Veracode01_Fade(CRGB colour, int fromBrightness, int toBrightness, int duration);
void Veracode01_BlankAll();
void Veracode01_ShowAll(CRGB colour, int brightness = 0);

void SetAllLEDs(CRGB colour);
void Do(CRGB colour);