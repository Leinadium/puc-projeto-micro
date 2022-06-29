#include <Wire.h>
#include <VL53L0X.h>
#include "FastLED.h"
#include <TimerOne.h>

#define NUM_LEDS 30
#define VMAX 500
#define NNOTAS 500
#define DIVISOR 100
#define TIPO floa
#define TEMPO 300

// Cria uma instancia do sensor
VL53L0X sensor;
int tempo1;
/*
 * SDA -> aref+1
 */
bool ligado=false;
bool flag1=true;
CRGB leds[NUM_LEDS];
void flag1true(){
  flag1=true;
}
bool sem1=true;
void acendeledsg(int ini,int fim){
  while (ini<fim){
    leds[ini] = CRGB::Green;
    FastLED.show();
    ini=ini+1;
  }
  tempo1=millis();
}
void acendeledsr(int ini,int fim){
  while (ini<fim){
    leds[ini] = CRGB::Red;
    FastLED.show();
    ini=ini+1;
  }
  tempo1=millis();
}
void apagaleds(){
  int cnt=0;
  while (cnt<NUM_LEDS){
    leds[cnt] = CRGB::Black;
    FastLED.show();
    cnt=cnt+1;
  }
  
}
void acertanota(int nota){
  apagaleds();
  int cntmax=nota*NUM_LEDS/(NNOTAS/DIVISOR);
  int cnt=(nota-1)*NUM_LEDS/(NNOTAS/DIVISOR);
  acendeledsg(cnt,cntmax);
}
void erranota(int nota){
  apagaleds();
  int cntmax=nota*NUM_LEDS/(NNOTAS/DIVISOR);
  int cnt=(nota-1)*NUM_LEDS/(NNOTAS/DIVISOR);
  acendeledsr(cnt,cntmax);
}
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
  delay(2000);
  ligado=true;
}
void loop() {
  String rec;
  int arg1;
  int arg2;
  if (ligado){
  Serial.println(String((float) nota(sensor.readRangeSingleMillimeters())/DIVISOR)+"; "+String(digitalRead(13)));
  } if (Serial.available()){
    rec=Serial.readString();
    arg1=rec.substring(0,1).toInt();
    arg2=rec.substring(2,3).toInt();
    if (arg1==1){
      acertanota(arg2);
    }if (arg1==0){
      erranota(arg2);
    }
  }
  if (millis()-tempo1>TEMPO){
    apagaleds();
  }
}
