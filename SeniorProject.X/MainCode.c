#include <PIC18F4321.h> //include necessary header
#pragma config OSC = INTIO2
#pragma config WDT = OFF
#pragma config LVP = OFF
#pragma config BOR = ON

//-----RGB-LED-COMMANDS----//
#define RED 0x04
#define YELLOW 0x06
#define GREEN 0x02
#define TEAL 0x03
#define BLUE 0x01
#define PURPLE 0x05

//-----SPI-COMMANDS----//
#define CS PORTCbits.RC0
#define MSHUTDOWN 0x0C //matrix power reg
#define MDigit0 0x01
#define MDigit1 0x02
#define MDECODE 0x09 //matrix decode reg
#define MTEST 0x0F //matrix test reg

unsigned int ADCONRESULT, clear;
//unsigned int GRID[10] = {1,0,0,1,0,0,0,1,0,0};
unsigned int DATA = 0x00; //data
unsigned int ADDRESS = MTEST;
unsigned int MESSAGE = 0x0F00;//((ADDRESS<<8) | DATA);

void delay(unsigned int);
void sendSPI(unsigned int);
void intializeSPI();
void rainbow(unsigned int timedelay){
        delay(timedelay);
        PORTB = RED;
        delay(timedelay);
        PORTB = YELLOW;
        delay(timedelay);
        PORTB = GREEN;
        delay(timedelay);
        PORTB = TEAL;
        delay(timedelay);
        PORTB = BLUE;
        delay(timedelay);
        PORTB = PURPLE;
}


void initializeSPI(){
    //PORTCbits.RC3 == SCK
    //PORTCbits.RC5 == SDO
    //PORTCbits.RC4 == SDI
    //PORTAbits.RA7 == SS
    SSPCON1= 0x22;
    SSPSTAT =0x80; 
}

void sendSPI(unsigned int input){
    //delay(5);
   //clear = SSPBUF;
    CS = 0;
    SSPBUF = input;
    //while(!SSPSTATbits.BF); // wait for transfer to complete
    CS = 1;
    //delay(5);
    clear = SSPBUF;
}

void delay(unsigned int itime){
    unsigned int i, j;
    for(i = 0; i < itime; i++)
        for(j = 0; j < 255; j++)
            ;
}

void main(){
    TRISA = 0xFF; //configure as input
    TRISB = 0x00; //configure as output
    TRISC = 0x00; //configure as output
    TRISD = 0x00; //configure as output
    PORTA = 0x00; //clear ports
    PORTB = 0x00;
    PORTC = 0x00; //used for PWM -> CCP (capture, compare)
    PORTD = 0x00;
    //ADCON0 = 0x01; //enable ADC
    //ADCON1 = 0x00; //using internal voltage for comparison
    //ADCON2 = 0x80; //right justified results
    //CS = 1;
    //PR2  = 249;
   // CCPR1L = 124;
    //CCP1CON = 0x20;
    //TRISCbits.TRISC2 = 0;
    //CCP1CON = 0x2C;
    //TMR2 = 0;
    //initializeSPI();
    
    //sendSPI(MESSAGE);
    //delay(15);
    //sendSPI(DATA);
    //delay(15);
    
    while(1){
        rainbow(25);
       // PIR1bits.TMR2IF = 0;
       // T2CONbits.TMR2ON = 1;
       // while(PIR1bits.TMR2IF == 0){
            
       // }
    }
    
    
    //while(1){
        //ADCONRESULT = 0;
        //ADCON0bits.GO = 1;
        //10-bit ADC, each step is 1/1024 -> 5V == 0x03FF and 0.00097V == 0x0001; 
        /*while(ADCON0bits.DONE == 1) { 
            ADCONRESULT = ADRESH;
            ADCONRESULT = ADCONRESULT << 8;
            ADCONRESULT |= ADRESL;
            
            if( ADCONRESULT > 0x00FF){
                PORTB = 0xFF;
            }
            if( ADCONRESULT > 0x007F){
                PORTB = 0x7F;
            }    
            if( ADCONRESULT > 0x003F){
                PORTB = 0x3F;    
            }
            if( ADCONRESULT > 0x001F){
                PORTB = 0x1F;
            }    
            if( ADCONRESULT > 0x000F){
                PORTB = 0x0F;
            }    
            if( ADCONRESULT > 0x0007){
                PORTB = 0x07;
            }   
            if( ADCONRESULT > 0x0003){
                PORTB = 0x03;
            }
            if( ADCONRESULT > 0x0001){
                PORTB = 0x01;
            }
            else
                PORTB = 0x00;
        }*/
    //}
    
}
