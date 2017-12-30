## babyvm

su
ln -s /flag /vagrant/flag
umount vagrant
rmmod vboxsf
modprobe vboxsf follow_symlinks=1
mount -t vboxsf vagrant /vagrant
cat /vagrant/flag


## babyvm2

Stay tuned... :>
