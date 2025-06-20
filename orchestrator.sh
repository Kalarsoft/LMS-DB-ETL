#!/bin/zsh
source venv/bin/activate;

pip install -r requirements.txt;

python3 src/extract.py &>> lms-etl.log;

ret=$?
if [[ $ret -ne 1 ]]; then
python3 src/transform.py &>> lms-etl.log;
fi

ret=$?
if [ $ret -ne 1 ]; then
    python3 src/load.py &>> lms-etl.log;
fi

ret=$?
if [ $ret -ne 1 ]; then
    rm  output/*;
fi