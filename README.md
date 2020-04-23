# Tool for collection of neural data related to conscious hand activity 
## Install
Tool requires python3.
* `cd src`
* `python3 setup.py install`
## Run 
* `python3 main.py`
## Record gestures dataset
### Instruction
1. Open "fixed" plugin
2. Select the folder in which dataset should be written
3. Select and configure sensor (can be simulated for testing)
4. Configure filters for hand activity signal
5. Record each gesture, follow the tips
6. Select the new folder to record the next dataset

Each gesture can be recorded more than 1 time for the session, but the file will be rewritten.

### Gestures
1. Nothing
2. Rock
3. Scissors
4. Paper
5. Ok
6. Horns
7. Shaka
8. Gun
9. Thumb up

### Output
File with sEMG signal is recorded for each gesture in csv format.
Each row contains signal values from sensors at the same time.

![alt text](https://github.com/kyr7/vizzero/blob/master/screen-fixed.png "Fixed")