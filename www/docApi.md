Javascript & Python
===================
Boilerplates
------------
### HTML & JS boilerplates
This is html boilerplate for WeIO. WeIO includes dependencies : jQuery, sockJS and weioApi.

```html
<!DOCTYPE html>
<html lang="en">
<script data-main="weioLibs/weio" src="weioLibs/require.js"></script>

  <head >
    <title>My first Web app</title>
  </head>

  <body>

    <p>Hello world!</p>
    
    <script>
        function onWeioReady() {
            console.log("DOM is loaded, websocket is opened");
        }
    </script>

  </body>
</html>
```
### onWeioReady()
This function is called when the DOM is fully loaded and websocket to WeIO is fully opened. Main difference between .ready() function from jQuery is that jQuery don't open websockets as they are not part of it's architecture. When using onWeioReady function, websocket communication with WeIO board is guaranteed, otherwise is not possible to send messages to the server before it fully opens it's websockets. It's recommended to use onWeioReady() as a replacement for .ready() from jQuery
```javascript
function onWeioReady() {
 console.log("DOM is loaded, websocket is opened");
}
```
### Python boilerplate
This is "Hello world" program written in Python. It prints "hello world" on console and blinks LED.
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")

```

Digital I/O
-----------
### digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground.

In index.html add one button in the body section
```html
<button type="button" id="myButton">ON</button>
```
In Javascript we can bind one event to this button and then turn one pin HIGH or LOW. Pin 20 is connected to green LED on WeIO board. You will see green LED turning ON and OFF by clicking to button in your interface.
```javascript
// actual state of html button, true - ON, false - OFF
var buttonState = false;

function onWeioReady() {
  $( "#myButton" ).click(function() {
     if (buttonState) {
         digitalWrite(20,HIGH);
         $( "#myButton" ).html("ON");
     } else {
         digitalWrite(20,LOW);
         $( "#myButton" ).html("OFF");
     }
     buttonState = !buttonState;
    });
}
```

However you can make automatic blinking LED with calling setInterval JS function like this

```javascript
var led = false; // false LOW, true HIGH

function onWeioReady() {
  setInterval(function() {
    // Do something every half second
    if (led)
        digitalWrite(20,HIGH);
    else
        digitalWrite(20,LOW);
    // inverts variable state
    led = !led;
    }, 500);
}
```

The same example done in Python 

```python
from weioLib.weio import *

def setup() :
    attach.process(blinky)

def blinky() :
    while True:
        digitalWrite(20, HIGH)
        delay(500)
        digitalWrite(20, LOW)
        delay(500)
```


### digitalRead(pin, callback)
Reads actual voltage on corresponding pin. WeIO inputs are 5V TOLERANT. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected. If only digitalRead function is provided, pin will be in HIGH Z state. See pinMode(pin,mode) function for more options.

In Javascript DigitalRead asks to provide callback function that will be called when WeIO board finish reading state on the pin. Callback function arguments will be populated with dictionary that provides pin number and pin state as information. This example with setInterval pooling is useful to check time to time pin state, if immediate reaction is needed than see attachInterrupt function.
```javascript
function onWeioReady() {
    console.log("hello");
    setInterval(function() {
    // Do something every 100ms
    //pinCallback will be called when data arrives from server
    digitalRead(0,pinCallback);
    }, 100);
}

function pinCallback(data) {
    $("#phrase").html("DigitalRead Value on the pin 0 is "+ data.data);
    $("body").css("background","white");
    $("#phrase").css("color","black");
}
```

Here is Python example
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    pin = 0
    while True:
        a = digitalRead(pin)
        print "Value on the pin ", pin, " = ", a
        delay(100)
```

### pinMode(pin, mode)

Sets state on the pin. Available modes are : PULL_UP, PULL_DOWN, INPUT, OUTPUT
This function activates pullups, pulldowns or high Z state (only INPUT) on declared pins. If pinMode function is not called and digitalRead is performed pin state will be in high Z by default
```javascript
function onWeioReady() {
  // sets pulldown resistor on pin 13
  inputMode(13,INPUT_PULLDOWN);
  digitalRead(13, pinCallback);
}

function pinCallback(pinInput) {
    console.log("Pin number " + String(pinInput.pin) + " is in state " +  String(pinInput.data));
    if (pinInput.data===0) {
        $('body').css('background', 'black');
    } else {
        $('body').css('background', 'white');
    }
}
```
Analog I/O
----------
### analogRead(pin, callback)
Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023.

AnalogRead asks to provide callback function that will be called when WeIO board finish reading state on the pin. Callback function arguments will be populated with dictionary that provides pin number and ADC value as information.
```javascript
function onWeioReady() {
 setInterval(function() {
    // Do something every 100ms
        //analogCallback will be called when data arrives from server
        analogRead(30, analogCallback);
    }, 100);

}

function analogCallback(pinInput) {
    console.log("Pin number " + String(pinInput.pin) + " ADC value " +  String(pinInput.data));
    if (pinInput.data > 512) {
        $('body').css('background', 'black');
    } else {
        $('body').css('background', 'white');
    }
}
```

### pwmWrite(pin, value)
Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 1000us and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature please refer to functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1.
```javascript
var count = 0;
var mode = true; // fade in - true, fade out - false
function onWeioReady() {
  setInterval(function() {
    // Do something every 20ms
    fader();
    }, 20);
}

function fader() {
    if (mode) {
        if (count < 255) {
            count++;
        } else {
            mode = !mode;
        }
    } else {
        if (count > 0) {
            count--;
        } else {
            mode = !mode;
        }
    }
    pwmWrite(20,count);
}
```

### setPwmPeriod(period)
Overrides default value of 1000us to set new period value for whole 6 PWM pins. Period value must be superior than 0 and inferior than 65535.
```javascript
var count = 0;
var mode = true; // fade in - true, fade out - false

function onWeioReady() {
  setPwmPeriod(4000);
  setInterval(function() {
    // Do something every 20ms
    fader();
    }, 20);
}

function fader() {
    if (mode) {
        if (count < 255) {
            count++;
        } else {
            mode = !mode;
        }
    } else {
        if (count > 0) {
            count--;
        } else {
            mode = !mode;
        }
    }
    pwmWrite(20,count);
}
```

### setPwmLimit(limit)
Overrides default limit of 8bits for PWM precision. This value sets PWM counting upper limit and it's expressed as decimal value. This limit will be applied to all 6 PWM pins.
```javascript
var count = 0;
var mode = true; // fade in - true, fade out - false

function onWeioReady() {
  setPwmLimit(512);
  setInterval(function() {
    // Do something every 20ms
    fader();
    }, 20);
}

function fader() {
    if (mode) {
        if (count < 512) {
            count++;
        } else {
            mode = !mode;
        }
    } else {
        if (count > 0) {
            count--;
        } else {
            mode = !mode;
        }
    }
    pwmWrite(20,count);
}
```


### startPackaging() and stopPackage()
Activate instruction buffering. In some cases it's more optimized to put a lot of instructions in one package and than send package. In that case for example instead sending 8 separate messages one packet will be send that contains 8 messages packed together. To start package buffering call startPackage() function. To send a package call sendPackage()
```javascript
startPackaging();
for (var j=0; j<7; j++) {
    if (id>=j) {
        digitalWrite(pins[j], HIGH);
    } else {
        digitalWrite(pins[j], LOW);
    }
}
sendPackage();
```

Client-server I/O
-----------------
### getConnectedUsers(callback)
This function returns array of all connected users to the server. It's specially useful for communication between clients using WeIO as bridge. However as this function discovers some of client information user can ban it or overload it to specify output information from python code. If function is banned then message warning message is sent to console.log.

GetConnectedUsers asks to provide callback function that will be called once WeIO board sent client information. Callback function arguments will be populated with dictionary that provides client information. See example below for all possible keys. These information are got from JS navigator object from each client, keys uuid and ip are provided by server and added to the dictionary.
```javascript
function onWeioReady() {
  $( "#myButton" ).click(function() {
     getConnectedUsers(printUsers);
    });
}

function printUsers(data) {
    var connections = data.data;
    for (var i in connections) {
        var connection = connections[i];
        console.log("");
        console.log("Client appCodeName ",  connection.appCodeName);
        console.log("Client appName ",      connection.appName);
        console.log("Client appVersion ",   connection.appVersion);
        console.log("Client cookieEnabled ",connection.cookieEnabled);
        console.log("Client ip ",           connection.ip);
        console.log("Client onLine ",       connection.onLine);
        console.log("Client platform ",     connection.platform);
        console.log("Client userAgent ",    connection.userAgent);
        console.log("Client uuid ",         connection.uuid);
    }
}
```
### getMyUuid()
Gets unique uuid number generated for this connection. This number is used by server to identify each client and can be used to address other clients that are connected. See getConnectedUsers for example.

GetMyUuid can be called once WeIO is ready for communication.
```javascript
function onWeioReady() {
  console.log(getMyUuid());
}
```
### talkTo(uuid, data)
TalkTo delivers json object to connected client with specific uuid. In this example message is sent to itself.
```javascript
function onWeioReady() {
    var myName = getMyUuid();
    data = {};
    data.info = "hello to myself";
    talkTo(myName, data);
}

function onReceiveMessage(data) {
    console.log("Received from ", data.from);
    console.log("Contents ", data.data);
}
```

### onReceiveMessage(data)
onReceiveMessage is callback function that will be called when some client sends message to actual uuid. This function works in pair with talkTo. onReceiveMessage is receiving callback and talkTo sender function. In this example message is sent to itself.
```javascript
function onWeioReady() {
    var myName = getMyUuid();
    data = {};
    data.info = "hello to myself";
    talkTo(myName, data);
}

function onReceiveMessage(data) {
    console.log("Received from ", data.from);
    console.log("Contents ", data.data);
}
```