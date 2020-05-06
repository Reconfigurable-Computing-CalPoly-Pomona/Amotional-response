//-----MC-Configuration----//
#include <PIC18F4321.h> 
#pragma config OSC = INTIO2
#pragma config WDT = OFF
#pragma config LVP = OFF
#pragma config BOR = OFF

//-----RGB-LED-COMMANDS----//
#define RED 0x20
#define YELLOW 0x30
#define GREEN 0x10
#define TEAL 0x18
#define BLUE 0x08
#define PURPLE 0x28

//-----DM----COMMANDS----//
#define H1 PORTCbits.RC0
#define H2 PORTCbits.RC5
#define H3 PORTDbits.RD0
#define H4 PORTCbits.RC3
#define H5 PORTDbits.RD7
#define H6 PORTDbits.RD1
#define H7 PORTDbits.RD6
#define H8 PORTDbits.RD3

#define V1 PORTCbits.RC4
#define V2 PORTDbits.RD5
#define V3 PORTDbits.RD4
#define V4 PORTCbits.RC1
#define V5 PORTDbits.RD2
#define V6 PORTAbits.RA2
#define V7 PORTCbits.RC6
#define V8 PORTCbits.RC7

#define ClearC 0x2D
#define ClearD 0xCB
#define ClearA 0x02

//-----SOUND--COMMANDS----//
#define HAPPY PORTBbits.RB2
#define SAD PORTBbits.RB1
#define CONFUSED PORTBbits.RB0
#define NOTHING PORTB


////-----SPI-COMMANDS----//
////#define CS PORTCbits.RC0
//#define MSHUTDOWN 0x0C //matrix power reg
//#define MDigit0 0x01
//#define MDigit1 0x02
//#define MDECODE 0x09 //matrix decode reg
//#define MTEST 0x0F //matrix test reg
//#define SCK PORTCbits.RC3
//#define SDO PORTCbits.RC5 
//#define SDI PORTCbits.RC4
//#define SS PORTAbits.RA7


unsigned int ADCONRESULT, EmoCodeOLD;
void ConfusedFace();
void Happy();
void HappyFace();
void Sad();
void SadFace();
void Nothing();
void NothingFace();
void sendPWM(unsigned char dutyCycle, unsigned int timedelay);
void rainbow(unsigned int timedelay);
void EmotionRead(unsigned int EmoCode);
void delay(unsigned int);
void sendSPI(char);
void initializeMicrocontroller();
void initializeSPI();
void initializeMatrix();
void pinClear();

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

void sendPWM(unsigned char dutyCycle, unsigned int timedelay){
    ConfusedFace();
    switch(dutyCycle){
        case 'R': 
            //sets PWM to 10% 
            CCPR1L = 0x05;
            CCP1CONbits.DC1B = 0x0;
            break;
       case 'M': 
            CCP1CONbits.DC1B = 0x3;   //sets PWM to 5% 
            CCPR1L = 0x03;
            break;
        case 'L': 
            CCP1CONbits.DC1B = 0x0;   //sets PWM to 3% 
            CCPR1L = 0x01;
            break;
        default:
            CCPR1H = 0x0;   //sets PWM to 10% 
            CCPR1L = 0x00;
            break;
    }
    ConfusedFace();
    OSCCON = 0x10; //switches to 125kHz clock
    T2CONbits.TMR2ON = 1;
    delay(timedelay);
    T2CONbits.TMR2ON=0;
    OSCCON=0x70;    //returns clock to 8MHz
}

void EmotionRead(unsigned int EmoCode){
    switch(EmoCode){
        
        case 0x02:  //neutral
            NothingFace();
            PORTAbits.RA3 == 0;
            PORTAbits.RA4 == 0;
            break;
        
        case 0x01: //Happy
            if(EmoCodeOLD == EmoCode){ //prevents song and dance from looping
                HappyFace();
                PORTAbits.RA3 = 0;
            }
            else{
                PORTAbits.RA3 = 1;
                HappyFace();
                sendPWM('L', 2);
                ConfusedFace();
                sendPWM('R', 2);
                ConfusedFace();
                sendPWM('L', 2);
                ConfusedFace();
                sendPWM('R', 2);
                ConfusedFace();
                sendPWM('L', 2);
                ConfusedFace();
                sendPWM('R', 2);
                ConfusedFace();
                HappyFace();
                EmoCodeOLD = EmoCode;
            }
            break;
            
        case 0x00: //Sad
            if(EmoCodeOLD == EmoCode){
                SadFace();
                PORTAbits.RA4 = 0;
            }
            else{
                SadFace();
                PORTAbits.RA4 = 1;
                SadFace();
                SadFace();
                SadFace();
                EmoCodeOLD = EmoCode;
            }
            break;
            
        default:
            break;
    }
}

void delay(unsigned int itime){
    unsigned int i, j;
    for(i = 0; i < itime; i++)
        for(j = 0; j < 255; j++)
            ;
}

void sendSPI(char input){
    unsigned char TempVar;
    TempVar = SSPBUF;  // Clears BF
    SSPBUF = input;
}

void initializeMicrocontroller(){
    TRISA = 0x81; //configure as input
    TRISB = 0x00; //configure as output
    TRISC = 0x00; //configure as output
    TRISD = 0x00; //configure as output
    PORTA = 0x00; //clear ports
    PORTB = 0x00;
    PORTC = 0xFF; 
    PORTD = 0xFF;//used for PWM -> CCP (capture, compare)
    PR2  = 0x3B;    //period set to 30ms
    CCP1CON = 0x0C; //selects RC2 as output
    PIR1bits.TMR2IF = 0; // disables interrupt for Timer 2
    T2CON = 0x02;   //Prescale set to 16
    TMR2 = 0;
    
    ADCON0 = 0x01; //enable ADC
    ADCON1 = 0x00; //using internal voltage for comparison
    ADCON2 = 0x80; //right justified results
}

void initializeSPI(){
    SSPCON1 =0x20; //we need 100ns period, 50ns pulsewidth -> 0.1us and 0.05us
    SSPSTAT =0x00;
}

void initializeMatrix(){
        sendSPI(0x09);
        delay(5);
        sendSPI(0x07);
        delay(5);
        sendSPI(0x09);
        delay(5);
        sendSPI(0x00);
        delay(5);
        sendSPI(0x0C);
        delay(5);
        sendSPI(0x01);
        delay(5);
        sendSPI(0x0F);
        delay(5);
        sendSPI(0x00);
        delay(5);
}

void pinClear(){
    PORTC = ClearC;
    PORTD = ClearD;
    PORTA = ClearA;
}

void Happy(){
            pinClear();
            H2 = 0;
            V3 = 1;
            pinClear();
            H2 = 0;
            V6 = 1;
            pinClear();
            H3 = 0;
            V3 = 1;
            pinClear();
            H3 = 0;
            V6 = 1;
            pinClear();
            H6 = 0;
            V2 = 1;
            pinClear();
            H7 = 0;
            V3 = 1;
            pinClear();
            H7 = 0;
            V4 = 1;
            pinClear();
            H7 = 0;
            V5 = 1;
            pinClear();
            H7 = 0;
            V6 = 1;
            pinClear();
            H6 = 0;
            V7 = 1;
            pinClear();

}

void HappyFace(){
                PORTB = 0x30;
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);
                Happy();
                delay(1);

}

void Sad(){

            H2 = 0;
            V3 = 1;
            pinClear();
            H2 = 0;
            V6 = 1;
            pinClear();
            H3 = 0;
            V3 = 1;
            pinClear();
            H3 = 0;
            V6 = 1;
            pinClear();
            H7 = 0;
            V2 = 1;
            pinClear();
            H6 = 0;
            V3 = 1;
            pinClear();
            H5 = 0;
            V4 = 1;
            pinClear();
            H5 = 0;
            V5 = 1;
            pinClear();
            H6 = 0;
            V6 = 1;
            pinClear();
            H7 = 0;
            V7 = 1;
            pinClear();
}

void SadFace(){
                PORTB = BLUE;
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
                Sad();
                delay(1);
}

void Confused(){
            H2 = 0;
            V3 = 1;
            pinClear();
            H2 = 0;
            V6 = 1;
            pinClear();
            H3 = 0;
            V3 = 1;
            pinClear();
            H3 = 0;
            V6 = 1;
            pinClear();
            H6 = 0;
            V3 = 1;
            pinClear();
            H5 = 0;
            V4 = 1;
            pinClear();
            H7 = 0;
            V4 = 1;
            pinClear();
            H5 = 0;
            V5 = 1;
            pinClear();
            H7 = 0;
            V5 = 1;
            pinClear();
            H6 = 0;
            V6 = 1;
            pinClear();
}

void ConfusedFace(){
    PORTB = PURPLE | 0x01;
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);
                Confused();
                delay(1);    
}

void Nothing(){

            H3 = 0;
            V2 = 1;
            pinClear();
            H3 = 0;
            V3 = 1;
            pinClear();
            H3 = 0;
            V6 = 1;
            pinClear();
            H3 = 0;
            V7 = 1;
            pinClear();
            H6 = 0;
            V2 = 1;
            pinClear();
            H6 = 0;
            V3 = 1;
            pinClear();
            H6 = 0;
            V4 = 1;
            pinClear();
            H6 = 0;
            V5 = 1;
            pinClear();
            H6 = 0;
            V6 = 1;
            pinClear();
            H6 = 0;
            V7 = 1;
            pinClear();
}

void NothingFace(){
        PORTB = 0;
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1);
                Nothing();
                delay(1); 
}

void main(){
    initializeMicrocontroller();
    NothingFace();
    while(1){
        ADCONRESULT = 0;
        ADCON0bits.GO = 1;
        //10-bit ADC, each step is 1/1024 -> 5V == 0x03FF and 0.00097V == 0x0001; 
        while(ADCON0bits.DONE == 1) { 
            ADCONRESULT = ADRESH;
            ADCONRESULT = ADCONRESULT << 8;
            ADCONRESULT |= ADRESL;
            
            if( ADCONRESULT > 0x003f){
                EmotionRead(PORTAbits.RA7);
            }
            else{
                NothingFace();
            }
            
        }
    }
}