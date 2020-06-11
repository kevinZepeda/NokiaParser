# Nokia Parser


This is a very useful tool to parse some data from Nokia Router
Devices, actually this is an experiment, that is useless for you
and the code is so bad, you can't use it in PROD.

### Features in this Version

Modules:
*  **Stage1**.
*  **Stage5**.
*  **Stage6**.
*  **Stage7**.
*  **Stage8**.

Debugger:
* TextFSM Library
* Visual Debugger



## Requirements
*This is the last testing working*

* [Python3.8](https://www.python.org/)
* [TextFSM](https://pypi.org/project/textfsm/)
  ```sh
  $ pip install textfsm
  ```




## How It Works

1. The Library contains an automation to parse text into a file `.cvs`.
   The parsing use a FSM based on textfsm.
2. Parser Need some `args` to work: `--stage-x`,`Template`,`[Files]`.
   Args.
   * `--stage-x` : This is an option to select Module into CLI.
   * `Template`  : This is a Finite State Machine (fsm) to make parsing.
   * `[Files]`   : This is a list of files to parse.
3. When files are processed, the method `.stageX()` return an object with:
    *  **`message`** : Message from parse, and healthy status
    *  **`status`**  : Status Code, `200` its OK, `400` fail and `404` Not found
    *  **`data`**    : Data files into a JSON

4. Debugger
    * TextFSM Library Native `$ python parser.py template [files]`
    * Visual Debugger generate HTML file to see pased data.
      * `$ python parser.py --visual-debug template [files]`
## Usage

  ```sh
  $ python app.py [--options] template [files]
  ```
Output
```sh
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508053', 'VER-7030', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508054', 'VER-7041', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508055', 'VER-7103', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508056', 'VER-7135', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508057', 'VER-7186', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
  ['PUEMTX-PUE7020-SB', '7450', '10.190.2.114', 'epipe', '508058', 'VER-7174', '2', '1/2/18', '2000', '2000', '25.00', '25.00', '30.00', '30.00']
```
