#!/bin/bash
python app.py templates/20_2.fsm nokia/*.log
# python app.py templates/20_3.fsm nokia/*.log
# python app.py templates/20_4.fsm nokia/*.log
python app.py templates/20_5.fsm nokia/*.log
python app.py templates/20_6.fsm nokia/*.log
python app.py templates/20_7.fsm nokia/*.log
python app.py templates/20_8.fsm nokia/*.log
python app.py templates/20_9.fsm nokia/*.log

zip scenerys17_19-27.zip *.csv
exit
