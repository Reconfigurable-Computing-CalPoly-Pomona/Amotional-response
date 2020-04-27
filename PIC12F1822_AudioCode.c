//adapted code from Ray Ring on CircuitSalad.com


#include <PIC12F1822.h>
#pragma config WDTE = 0x00;
#pragma config BOREN = 0x00;

#define A4noteL 0x00 //
#define A4noteH 0x5c //

#define B4noteL 0x00 //
#define B4noteH 0x74 //

#define C5noteL 0x40 //
#define C5noteH 0x6c //

#define D5noteL 0xC0 //
#define D5noteH 0x89 //

#define E5noteL 0xC0 //
#define E5noteH 0x9A //

#define F5noteL 0x00 //
#define F5noteH 0xA4 //

#define G5noteL 0x30 //
#define G5noteH 0xa3 //

const unsigned char sine[256] =
{// sine wave 8 bit resolution scaled to 90% max val
131,132,135,137,140,143,146,149,152,155,157,160,163,166,168,171,
174,176,179,181,184,186,189,191,194,196,198,200,202,205,207,209,
211,212,214,216,218,219,221,223,224,226,227,228,229,231,232,233,
234,234,235,236,237,237,238,238,239,239,239,239,240,240,240,239,
239,239,239,238,238,237,237,236,236,235,234,233,232,231,230,229,
227,226,225,223,222,220,219,217,216,214,212,210,208,206,204,202,
200,198,196,194,192,189,187,185,182,180,177,175,173,170,167,165,
162,160,157,154,152,149,146,144,141,138,135,133,130,127,124,122,
119,116,113,111,108,105,103,100, 97, 95, 92, 89, 87, 84, 82, 79,
77, 74, 72, 69, 67, 64, 62, 60, 58, 55, 53, 51, 49, 47, 45, 43,
41, 39, 37, 36, 34, 32, 31, 29, 28, 26, 25, 24, 22, 21, 20, 19,
18, 17, 16, 15, 15, 14, 13, 13, 12, 12, 12, 11, 11, 11, 11, 11,
11, 11, 11, 12, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 19, 21,
22, 23, 24, 26, 27, 29, 30, 32, 33, 35, 37, 39, 41, 43, 45, 47,
49, 51, 53, 56, 58, 60, 63, 65, 68, 70, 73, 75, 78, 81, 83, 86,
89, 92, 94, 97, 100,103,106,108,111,114,117,120,123,126,129,130};

long PhaseAccum, PhaseShift;

void delay(unsigned int);

void delay(unsigned int itime){
    unsigned int i, j;
    for(i = 0; i < itime; i++)
        for(j = 0; j < 255; j++)
            ;
}

void Init_Main(){
//PIC12F1822 specific configuration
OPTION_REG = 0b10000000; // disable internal pull ups
OSCCON = 0b11110000; //8MHz clock //32MHz pll
TRISA = 0b00111001; // configure IO/a2d(gpio0) and mclr set as inputs
ANSELA = 0; //no analog
T2CON = 0b00000100;// TMR2 ON, postscale 1:1, prescale 1:1
PR2 = (0x50);// sets PWM rate to approx 98.5KHz with 32Mhz internal oscillator
CCP1CON = 0b00001111;// CCP1 ON, and set to simple PWM mode
ADCON0 = 0b00100101; // configure ADC
ADCON1 = 0b00100000; // configure ADC
}

void SoundGen(int noteL, int noteH, int timing){
    int max = 0;
    PhaseShift = 0x00FFFFFF;//frequency values loaded into
    while (max < timing){
    while(PIR1bits.TMR2IF != 1);// wait for TMR2 cycle to restart
    
    CCPR1L = (sine[((char *)&PhaseAccum)[3]]) >> 2;// load MSbits 7-2 duty cycle value into CCPRIL
    CCP1CON ^=((sine[((char *)&PhaseAccum)[3]]) & 0x03) << 4;// load in bits 1-0 into 5 and 4 of CCP1CON
        //delay(1);
    //////duty cycle value byte is now loaded for next cycle coming//////
    if(PIR1bits.ADIF == 0)
      ADCON0bits.GO = 1; //start ADC here to get value into PhaseShift to change Freq
//    //will have to go around the loop one time before ready flag is high
    if(PIR1bits.ADIF != 0){ //if ADC read complete load values and clear flag
        ((char *)&PhaseShift)[1] = noteL; //load ADRESL into PhaseShift // higher means faster
        //1bit == 0.0048V, 440Hz == 2.02V // increased ADRESH bits means faster
        ((char *)&PhaseShift)[2] = noteH; //load ADRESH into PhaseShift
        PIR1bits.ADIF = 0;//clear flag so next time ADC can run
        }
    PhaseAccum = PhaseAccum + ((PhaseShift << 5) + 1);
    PORTAbits.RA0 = ((char *)&PhaseAccum)[3];
    PIR1bits.TMR2IF = 0x00; // clear TMR2 int flag
    max += 1;
    }
}

void main() {
    int change = 1;
Init_Main();//configure part
    while(1){ //alway do this
        if(PORTAbits.RA0 == 1){
            if(change == 1){
                PORTAbits.RA1 = 1;
                SoundGen(C5noteL, C5noteH, 2500); //627
                delay(35);                     //523
                SoundGen(C5noteL, C5noteH, 1500); //627
                delay(35);                     //523
                SoundGen(G5noteL, G5noteH, 10000); //784
                delay(100);                     //784
                change = 0;
                PORTAbits.RA1 = 0;
                }
            }
        
        if(PORTAbits.RA4 == 1){
            if(change == 1){
                PORTAbits.RA1 = 1;
                SoundGen(G5noteL, G5noteH, 2500); //627
                delay(35);                     //523
                SoundGen(G5noteL, G5noteH, 1500); //627
                delay(35);                     //523
                SoundGen(C5noteL, C5noteH, 10000); //784
                delay(100);                     //784
                change = 0;
                PORTAbits.RA1 = 0;
                }
            }
        
        if((PORTAbits.RA0 == 0) || (PORTAbits.RA4 == 0)) {
            change = 1;
            }
    }
}