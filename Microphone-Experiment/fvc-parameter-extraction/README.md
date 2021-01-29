

## Collecting FVC Manuver Data Using Arduino
We will Use Edge Impulse combined with Arduino to collect data for MVC manuver. We underline the steps below

### Set up the mask
We are using atleast two mask (N95 and Cloth). Refer the pictures below to affix the microcontroller into the mask.
![Microcontroller](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/arduino-1.jpg)
![enter image description here](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/arduino-2.jpg)
![enter image description here](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/n95-mask.jpg)
![enter image description here](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/cloth-mask.jpg)

### Edge Impulse For Arduino
1. Sign up for [Edge Impulse](https://docs.edgeimpulse.com/docs/arduino-nano-33-ble-sense) and deploy it in Arduino Nano 33 BLE Sense. The [Edge Impulse Studio](https://studio.edgeimpulse.com) would looks something like below. Select **Sensor** as `Built-In Microphone`, **Frequency** as `16000Hz` and **Sample length** as `10000`ms.
![enter image description here](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/edge-impulse-1.png)
2. **Record the Audio:** The person will wear the microcontroller retrofitted mask. Click on **Start Sampling**. Once the timer begins, the user should take a deep inhale and exhale forcefully, untill no more air can he exhaled. 
3. The FVC manuver recording would look something like below.
![enter image description here](https://github.com/rishi-a/SmartMask-Project/blob/main/Microphone-Experiment/fvc-parameter-extraction/images/edge-impulse-2.png)
4. Download the audio file as json and send it over for further processing.




