# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR
#. ./tasks/environment.sh
# . tasks/environment.sh
# . tasks/variable.sh

killall -9 python qemu-system-x86_64
# Kill python and AVD process
# export SENDER_PASSWORD='hfac mvld ecjx clru'
# export RECEIVER_MAIL="rikenkhadela22@gmail.com"
# export SENDER_MAIL='rikenkhadela777@gmail.com'
# export SYSTEM_NO='RK'
# activate the virtual environment for python
#. env/bin/activate
. env/bin/activate

# update code
# git checkout old-insta-rk
# git stash
# git pull 

# setup database
# python temp/z22.py
# python manage.py update_csv 
# python manage.py delete_avd 
python manage.py update_conf