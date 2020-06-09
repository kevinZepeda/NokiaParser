# Nokia Parser


This is a very useful tool to parse some data from Nokia Router
Devices, actually this is an experiment, that is useless for you
and the code is so bad, you can't use it in PROD.

### Features in this Version
* Module **Stage1**.
* Module **Stage5**.
* Module **Stage6**.


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
2. Parser Need some `args` to work: `--stage-x`,`Template`,`[Files]`,`Name`.
   Args
   `--stage-x` : This is an option to select Module into CLI.
   `Template`  : This is a Finite State Machine (fsm) to make parsing.
   `[Files]`   : This is a list of files to parse.
   `Name`      : Name for output, this file is creating in the work folder from CLI.
3. When files are processed, the method `.stageX()` return an object with:
      **`message`** : Message from parse, and healthy status
      **`status`**  : Status Code, `200` its OK, `400` fail and `404` Not found
      **`data`**    : Data files into a JSON

## Usage

  ```sh
  $ python parser.py --stage-1 templates/1.fsm nokia-samples/*.log nokia-devices
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
