Adding a Logical Volume
================

Each of the batches is living in a logical volume of its own.  This was done for the purposes of making the backup process less painful.  This means when you [add a new batch](./new_batch), you will likely first need to create a new volume for it.

Determine your volume group.  It should be `vg_batches` but there is no harm in double checking.

    vgdisplay

Now create a new logical volume inside of that group.  The naming conventions were based roughly on the batch names in the network drives, but if in doubt just use nbu as the prefix, since all of our batches have that awardee code.  If this is a particularly large batch, 200G may not be big enough.  Try to determine how big your batch is before you create the volume, if possible.

    lvcreate -L 200G -n nbu_name vg_batches
    
Make a new filesystem.  Your new volume is probably in `/dev/vg_batches/` but the path may have changed if you found that your volume group was not `vg_batches` as advertised above.

    mkfs.ext3 /dev/vg_batches/nbu_name
    
Mount your filesystem.

    mkdir /batches/nbu_name
    mount /dev/vg_batches/nbu_name /batches/nbu_name
    
You are also going to need to make sure that your new volume is automatically mounted when the server is booted.
Open fstab and add your batch to the list, following the examples of those wise ones who have gone before you.
Press `i` to type.
```
    vim /etc/fstab

    # You should see something like the following
    /dev/mapper/vg_cors1303-lv_root /                       ext4    defaults        1 1
    UUID=6d601634-37f4-4233-a262-5229c1fad7e2 /boot         ext4    defaults        1 2
    /dev/mapper/vg_cors1303-lv_home /home                   ext4    defaults        1 2
    /dev/mapper/vg_cors1303-lv_swap swap                    swap    defaults        0 0
    tmpfs                           /dev/shm                tmpfs   defaults        0 0
    devpts                          /dev/pts                devpts  gid=5,mode=620  0 0
    sysfs                           /sys                    sysfs   defaults        0 0
    proc                            /proc                   proc    defaults        0 0
    /dev/vg_data/lv_data		        /data                   ext3	  defaults        1 2
    /dev/vg_batches/nbu_bravo       /batches/nbu_bravo      ext3	  defaults        1 2
    /dev/vg_batches/ne_alliance     /batches/ne_alliance    ext3	  defaults        1 2
    /dev/vg_batches/nbu_pound		    /batches/nbu_pound      ext3	  defaults        1 2
    /dev/vg_batches/nbu_abbott      /batches/nbu_abbott     ext3    defaults        1 2
```

Double check that you didn't make any typos.  Triple check.  Great, now save and exit with `:wq` and press enter.
If you want to find out if you have made a typo now rather than wondering what is going wrong in 8 months when the server goes down, reboot it right away.  Ask Jason or one of the other CORS sysadmins before doing this!  You may need their immediate help if there is something wrong with the fstab file, but at the very least there might not be a lot of good will if you just restart their server without asking first.

    shutdown -r now
    
Now you should have a happy little volume in which you can put your new batch!  Continue with the instructions for [adding a new batch](./new_batch.md).
