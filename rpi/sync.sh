# Script to sync some directory with RPi
# to develop on Windows and automatically push changes to RPi.

# Can be used with RSA key (identity_file). Otherwise rsync asks for password after every change.
# Usage: ./sync.sh [path_to_identity_file]

REMOTE_IP="192.168.1.51"
DIR_TO_SYNC="./test-rsync"

function sync_with_remote() {
  rsync -avz -e "$1" $DIR_TO_SYNC pi@$REMOTE_IP:~/Desktop --delete
}

[[ -z $1 ]] && ssh_args="" || ssh_args="-i $1"
ssh_command="ssh $ssh_args"

sync_with_remote "$ssh_command"
while inotifywait -r -e modify,create,delete,move $DIR_TO_SYNC; do
  sync_with_remote "$ssh_command"
done