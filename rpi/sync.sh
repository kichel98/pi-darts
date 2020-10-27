# Script to sync some directory with RPi
# to develop on Windows and automatically push changes to RPi.

# Can be used with RSA key (identity_file). Otherwise rsync asks for password after every change.
# Usage: ./sync.sh ip_number [path_to_identity_file]

REMOTE_IP=$1
DIR_TO_SYNC="../rpi"

function sync_with_remote() {
  rsync -avz -e "$1" $DIR_TO_SYNC pi@"$REMOTE_IP":~/Desktop/pi-darts --delete --exclude test/test-images
}

[[ -z $2 ]] && ssh_args="" || ssh_args="-i $2"
ssh_command="ssh $ssh_args"

sync_with_remote "$ssh_command"
while inotifywait -r -e modify,create,delete,move $DIR_TO_SYNC; do
  sync_with_remote "$ssh_command"
done