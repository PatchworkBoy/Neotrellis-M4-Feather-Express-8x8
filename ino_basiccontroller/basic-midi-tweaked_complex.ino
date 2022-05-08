/* 
This example shows basic usage of the
MultiTrellis object controlling an array of
NeoTrellis boards

As is this example shows use of two NeoTrellis boards
connected together with the leftmost board having the
default I2C address of 0x2E, and the rightmost board
having the address of 0x2F (the A0 jumper is soldered)

Any noteOn on ch16 will advance column highlight.
Any noteOn on ch15 will advance row highlight.
Any noteOn on ch14 will reset row / column highlight to pos 0.
Any noteOn on other channels will illuminate associated key.
On a Feather M4 Express, 420bpm seems to be rough limit on 
incoming msgs before things start to get buffered.
*/
#include <memory>
#include <map>
#include <Arduino.h>
#include <Adafruit_TinyUSB.h>
#include <Adafruit_NeoTrellis.h>
#include <MIDI.h>

//class Page
//{
//protected:
//  Page();
//
//public:
//  virtual ~Page();
//
//  virtual String name() const = 0;
//
//  virtual bool update(unsigned long seconds);
//  virtual bool onKey(uint8_t x, uint8_t y, bool isReleased) = 0;
//  virtual uint32_t cellColor(uint8_t x, uint8_t y) const = 0;
//};

// USB MIDI object
Adafruit_USBD_MIDI usb_midi;

// Create a new instance of the Arduino MIDI Library,
// and attach usb_midi as the transport.
MIDI_CREATE_INSTANCE(Adafruit_USBD_MIDI, usb_midi, MIDI);

// Variable that holds the current position in the sequence.
uint32_t previous = 0;
uint32_t color = 0;
int row = 0;
int lastrow = 0;
int col = 0;
int lastcol = 0;

// Array of midi-note values to be mapped top left to bottom right - C0 thru D#5 = 24 thru 87
byte note_sequence[] = {
  24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
  48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,
  75,76,77,78,79,80,81,82,83,84,85,86,87
};

// Array of midi-cc IDs to be mapped top left to bottom right
byte control_sequence[] = {
  24,25,26,27,28,29,30,31,
  32,33,34,35,36,37,38,39,
  40,41,42,43,44,45,46,47,
  48,49,50,51,52,53,54,55,
  56,57,58,59,60,61,62,63,
  64,65,66,67,68,69,70,71,
  72,73,74,75,76,77,78,79,
  80,81,82,83,84,85,86,87
};

#define Y_DIM 8 //number of rows of key
#define X_DIM 8 //number of columns of keys
#define maincolor seesaw_NeoPixel::Color(0,0,10)

//create a matrix of trellis panels
Adafruit_NeoTrellis t_array[Y_DIM/4][X_DIM/4] = {
  
  { Adafruit_NeoTrellis(0x30), Adafruit_NeoTrellis(0x2E) },
  { Adafruit_NeoTrellis(0x2F), Adafruit_NeoTrellis(0x31) }
  
};

//pass this matrix to the multitrellis object
Adafruit_MultiTrellis trellis((Adafruit_NeoTrellis *)t_array, Y_DIM/4, X_DIM/4);

// Input a value 0 to 255 to get a color value.
// The colors are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return seesaw_NeoPixel::Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return seesaw_NeoPixel::Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return seesaw_NeoPixel::Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  return 0;
}

//std::shared_ptr<Page> createP1(){
//  return nullptr;
//}
//std::shared_ptr<Page> createP2(){
//  return nullptr;
//}
//std::shared_ptr<Page> createP3(){
//  return nullptr;
//}
//std::shared_ptr<Page> createP4(){
//  return nullptr;
//}
//void showPage(){}

std::map<uint16_t, unsigned long> pressedKeys;
//std::shared_ptr<Page> pagePtr;

//define a callback for key presses
TrellisCallback onKey(keyEvent evt){
  auto const now = millis();
  auto const keyId = evt.bit.NUM;
  bool isReleased;

  switch (evt.bit.EDGE)
  {
  case SEESAW_KEYPAD_EDGE_RISING:
    pressedKeys[keyId] = now;
    isReleased = false;
    trellis.setPixelColor(evt.bit.NUM, Wheel(map(evt.bit.NUM, 0, X_DIM*Y_DIM, 0, 255))); //on rising
    MIDI.sendNoteOn(note_sequence[evt.bit.NUM], 127, 1);
    
    // make monophonic - comment out following 3 lines for polyphonic
    if(previous!=evt.bit.NUM)
      MIDI.sendNoteOff(note_sequence[previous], 0, 1);
    previous = evt.bit.NUM;
    
    break;
  case SEESAW_KEYPAD_EDGE_FALLING:
    if (pressedKeys.count(keyId) > 2)
    {
      auto const pressedAt(pressedKeys[keyId]);
      auto const duration(now - pressedAt);

      pressedKeys.erase(keyId);

//      Serial.print("****** ");
//      Serial.print(keyId);
//      Serial.print(" ");
//      Serial.print(duration);
//      Serial.println(" ****** ");

      if (duration > 3000)
      {
        Serial.println(" *MENU* ");
      }
    }
    isReleased = true;
    color = maincolor;
    trellis.setPixelColor(evt.bit.NUM, color); //off falling
    MIDI.sendNoteOff(note_sequence[evt.bit.NUM], 0, 1);
    break;
  }  
  trellis.show();
  return nullptr;
}

void setup() {
#if defined(ARDUINO_ARCH_MBED) && defined(ARDUINO_ARCH_RP2040)
  TinyUSB_Device_Init(0);
#endif

  // Initialize MIDI, and listen to all MIDI channels
  // This will also call usb_midi's begin()
  MIDI.begin(MIDI_CHANNEL_OMNI);

  // Attach the handleNoteOn function to the MIDI Library. It will
  // be called whenever the Neotrellis receives MIDI Note On messages.
  MIDI.setHandleNoteOn(handleNoteOn);

  // Do the same for MIDI Note Off messages.
  MIDI.setHandleNoteOff(handleNoteOff);

  Serial.begin(115200);
  
  while( !TinyUSBDevice.mounted() ) delay(1);
  
  if(!trellis.begin()){
    Serial.println("failed to begin trellis");
    while(1) delay(1);
  }
  
  Serial.print("Init...");

  /* the array can be addressed as x,y or with the key number */
  for(int i=0; i<Y_DIM*X_DIM; i++){
      trellis.setPixelColor(i, Wheel(map(i, 0, X_DIM*Y_DIM, 0, 255))); //addressed with keynum
      trellis.show();
      delay(20);
  }
  
  for(int y=0; y<Y_DIM; y++){
    for(int x=0; x<X_DIM; x++){
      //activate rising and falling edges on all keys
      trellis.activateKey(x, y, SEESAW_KEYPAD_EDGE_RISING, true);
      trellis.activateKey(x, y, SEESAW_KEYPAD_EDGE_FALLING, true);
      trellis.registerCallback(x, y, onKey);
      trellis.setPixelColor(x, y, maincolor); //addressed with x,y
      trellis.show(); //show all LEDs
      delay(20);
    }
  }
  Serial.println(" Ready!");
}

void loop() {
  trellis.read();
  MIDI.read();
}

void handleNoteOn(byte channel, byte pitch, byte velocity)
{ 
  switch (channel)
  {
    case 16:
      lightCol(col);
      col = col < (X_DIM-1) ? col+1 : 0;
      break;
    case 15:
      lightRow(row);
      row = row < (Y_DIM-1) ? row+1 : 0;
      break;
    case 14:
      reset();
      break;
    default:
      for(int i=0; i<Y_DIM*X_DIM; i++){
        if (pitch == note_sequence[i]) {
         trellis.setPixelColor(i,Wheel(map(i, 0, X_DIM*Y_DIM, 0, 100)));
         if (i+1<Y_DIM*X_DIM)
          if(((i+1) % X_DIM) > 0){
            trellis.setPixelColor(i+1,Wheel(map(i, 0, X_DIM*Y_DIM, 0, 100)));
          }
         if (i-1>1)
          if(((i-1) % X_DIM) > 0){
            trellis.setPixelColor(i-1,Wheel(map(i, 0, X_DIM*Y_DIM, 0, 100)));
          }
         if (i+Y_DIM<Y_DIM*X_DIM)
          trellis.setPixelColor(i+Y_DIM,Wheel(map(i, 0, X_DIM*Y_DIM, 0, 100)));
         if (i-Y_DIM>0)
          trellis.setPixelColor(i-Y_DIM,Wheel(map(i, 0, X_DIM*Y_DIM, 0, 100)));
         trellis.show();
         break;
        } 
      }
      break;
  }
}

void handleNoteOff(byte channel, byte pitch, byte velocity)
{
  for(int i=0; i<Y_DIM*X_DIM; i++){
    if (pitch == note_sequence[i]) {
     trellis.setPixelColor(i,maincolor);
     if (i+1<Y_DIM*X_DIM)
      trellis.setPixelColor(i+1,maincolor);
     if (i-1>1)
      trellis.setPixelColor(i-1,maincolor);
     if (i+X_DIM<Y_DIM*X_DIM)
      trellis.setPixelColor(i+X_DIM,maincolor);
     if (i-X_DIM>0)
      trellis.setPixelColor(i-X_DIM,maincolor);//addressed with keynum
     trellis.show();
     break;
    } 
  }
}

void lightRow(int row){
  if (lastrow!=row){
      dimRow(lastrow);
  }
  for(int i=(row*X_DIM); i<((row*X_DIM)+X_DIM); i++){
    trellis.setPixelColor(i,seesaw_NeoPixel::Color(10,0,0));
  }
  lastrow = row;
  trellis.show();
}
void dimRow(int row){
  for(int i=(row*X_DIM); i<((row*X_DIM)+X_DIM); i++){
    trellis.setPixelColor(i,maincolor);
  }
  //trellis.show();
}
void lightCol(int col){
  dimCol(lastcol);
  for(int i=col; i<Y_DIM*X_DIM; i++){
    if((i%4)==0) { // assuming 4/4 timing
      trellis.setPixelColor(i,seesaw_NeoPixel::Color(35,35,35));
    } else {
      trellis.setPixelColor(i,seesaw_NeoPixel::Color(10,10,10));
    }
    i=i+(Y_DIM-1);
  }
  lastcol = col;
  trellis.show();
}
void dimCol(int col){
  for(int i=col; i<X_DIM*Y_DIM; i++){
    trellis.setPixelColor(i,maincolor);
    i=i+(Y_DIM-1);
  }
  //trellis.show();
}

void allOff(){
  for(int i=0; i<Y_DIM*X_DIM; i++){
   trellis.setPixelColor(i,maincolor);
  }
  trellis.show(); 
}

void reset(){
  col = 0;
  row = 0;
  allOff();
}
