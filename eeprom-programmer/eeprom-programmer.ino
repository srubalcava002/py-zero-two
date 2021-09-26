#define WRITE_ENABLE 22     //BOTH ACTIVE LOW
#define OUTPUT_ENABLE 23

#define ADDRESS_BEGIN 24
#define ADDRESS_END 39

#define DATA_BEGIN 40
#define DATA_END 48

//  ADDRESS IS LATCHED BEFORE DATA, SO SET ADDRESS BEFORE THE FALLING EDGE WRITE PULSE AND DATA BEFORE RISING EDGE

byte listenForData() {
    // READ BYTE FROM SERIAL PORT
    return Serial.read();
}

void latchAddress(int address) {
    // CONVERT ADDRESS/CURRENT BYTE TO PINS
    addressToPins(address);

    digitalWrite(WRITE_ENABLE, LOW);
}

void latchData(byte data) {
    // CONVERT DATA TO PINS
    dataToPins(data);
    digitalWrite(WRITE_ENABLE, HIGH);
}

void dataPolling() { // ATTEMPT TO READ LAST BYTE WRITTEN TO MAKE DATA VALID
    digitalWrite(OUTPUT_ENABLE, LOW); // ENABLE OUTPUT AFTER SETTING ADDRESS. LAST ADDRESS SHOULD ALREADY BE SET FROM LAST BYTE WRITTEN?
    delayMicroseconds(50);
    digitalWrite(OUTPUT_ENABLE, HIGH);
}

void addressToPins(int current_address) {
    current_address = current_address & 0b111111111111111;

    for (int i = ADDRESS_BEGIN; i < ADDRESS_END; i++) {
        if (current_address & 1 == 1) {
            digitalWrite(i, HIGH);
        }
        else {
            digitalWrite(i, LOW);
        }

        current_address = current_address >> 1;
    }
}

void dataToPins(byte current_data) {
    for (int i = DATA_BEGIN; i < DATA_END; i++) {
        if (current_data & 1 == 1) {
            digitalWrite(i, HIGH);
        }
        else {
            digitalWrite(i, LOW);
        }

        current_data = current_data >> 1;
    }
}

void readEeprom() {
    digitalWrite(OUTPUT_ENABLE, LOW);
    
}

void setup() {
    for (int i = WRITE_ENABLE; i <= DATA_END; i++) {
        pinMode(i, OUTPUT);
    }

    digitalWrite(OUTPUT_ENABLE, HIGH);
    digitalWrite(LED_BUILTIN, LOW);

    Serial.begin(57600);

    byte byte_write;

    if (Serial.available() <= 0) {
        Serial.write("A");
        while (Serial.available() <= 0) {
            delay(100);
        }
    }

    for (int current_byte = 0; current_byte < 32768; current_byte++) {
        Serial.write("C");
        Serial.flush();

        while(Serial.available() <= 0) {
            delay(100);
        }

        byte_write = Serial.read();
        delay(100);
        latchAddress(current_byte);
        latchData(byte_write);

        Serial.write("Q");
        Serial.flush();
        delay(100);        
    }
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}