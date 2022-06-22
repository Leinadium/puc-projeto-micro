#include <Wire.h>
#include <VL53L0X.h>
#include "FastLED.h"
#define NUM_LEDS 30

#define VMAX 500
#define NNOTAS 500
#define DIVISOR 100
#define TIPO floa

// Cria uma instancia do sensor
VL53L0X sensor;
/*
 * SDA -> aref+1
 */
bool ligado=false;
CRGB leds[NUM_LEDS];
int nota(int dist){ //Retorna nota
  int cnt1=0;
  int cnt2=0;
  
  while (cnt2<VMAX){
    if (cnt2+VMAX/NNOTAS>=dist){
      return cnt1+1;
    }
    cnt2=cnt2+VMAX/NNOTAS;
    cnt1=cnt1+1;
  }
  if (VMAX*1.1>=dist){
    return cnt1;
  }
  return -DIVISOR; //nenhuma nota selecionada
}
void setup() {
  Serial.begin(9600);
  Wire.begin();
  sensor.init();
  sensor.setTimeout(500);
  int cnt3=0;
  pinMode(13,INPUT);
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS);
  //Teste para a função nota()
  /*
  while (cnt3<=1001){
    Serial.println();
    Serial.print("cnt3=");
    Serial.print(cnt3);
    Serial.print("; nota=");
    Serial.print(nota(cnt3));
    
    cnt3=cnt3+1;
  }
  */
  delay(1000);
  ligado=true;
}
void loop() {
  int cnt=0;
  int tmp=1;
  while (cnt<NUM_LEDS){
  leds[cnt] = CRGB::Red; FastLED.show(); delay(tmp);
  cnt=cnt+1;
  }
  cnt=0;
  while (cnt<NUM_LEDS){
  leds[cnt] = CRGB::Green; FastLED.show(); delay(tmp);
  cnt=cnt+1;
  }
  cnt=0;
  while (cnt<NUM_LEDS){
  leds[cnt] = CRGB::Blue; FastLED.show(); delay(tmp);
  cnt=cnt+1;
  }
  if (ligado){
  Serial.println(String((float) nota(sensor.readRangeSingleMillimeters())/DIVISOR)+"; "+String(digitalRead(13)));
  }
}
