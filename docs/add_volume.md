Adding a Logical Volume
================

Each of the batches is living in a logical volume of its own.  This was done for the purposes of making the backup process less painful.  This means when you [add a new batch](./new_batch), you will likely first need to create a new volume for it.  If one exists but it's not big enough, skip to the bottom to see how to resize it.

Determine your volume group.  It should be `vg_batches` but there is no harm in double checking.

    vgdisplay

Now create a new logical volume inside of that group.  The naming conventions were based roughly on the batch names in the network drives, but if in doubt just use nbu as the prefix, since all of our batches have that awardee code.  If this is a particularly large batch, 200G may not be big enough.  Try to determine how big your batch is before you create the volume, if possible.

To determine the size of your batch with OSX and linux, respectively (without tiffs):

    du -sh -I "*.tif" batch_name
    du -sh --exclude="*.tif" batch_name
    
Create a logical volume on the newspaper server:

    lvcreate -L 200G -n nbu_name vg_batches
    
Make a new filesystem.  Your new volume is probably in `/dev/vg_batches/` but the path may have changed if you found that your volume group was not `vg_batches` as advertised above.

    mkfs.ext4 /dev/vg_batches/nbu_name
    
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

Resizing a Volume
================

Your volume exists but it's not big enough.  Perhaps you originally were only using jp2s but now you've decided to use tiffs instead (this issue is totally hypothetical and probably didn't happen to us).  Don't worry, it's pretty easy to change the size if you have a bit of time.

First doublecheck that you know where the volume you want to change lives:

    lvdisplay

That will give you a whole list of all your volumes and you should see information like 

```
    --- Logical volume ---
    LV Path                /dev/vg_batches/czech_newspapers
    LV Name                czech_newspapers
    VG Name                vg_batches
    LV UUID                7NNMcs-1JVe-fcs5-fU4i-UpUM-c6XD-aYhpgm
    LV Write Access        read/write
    LV Creation host, time cors1303.unl.edu, 2015-04-23 12:26:59 -0500
    LV Status              available
    # open                 1
    LV Size                750.00 GiB
    Current LE             192000
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:39
```

Great.  Now that you're sure you know where the volume is, unmount it.

```shell
    umount /dev/vg_batches/czech_newspapers
```

Now you can actually resize it.  There are a few variations on this command, so feel free to look it up if you want to specifically say "it should be 400GB total" versus the below which is more like "I want it to be 40GB bigger than it currently is."  You could also opt for reducing the volume, if that's what you're in the mood to do.

```shell
    lvresize -L +40G /dev/vg_batches/czech_newspapers
```

Assuming that all went well there, run e2fsck, which just czechs that the filesystem is still doing okay.

```shell
    e2fsck -f /dev/vg_batches/czech_newspapers
```

The above will probably take at least a couple minutes, but it could be a substantial chunk of time if you already have a big file system in place.  Once it is done (hopefully successfully), then you can actually resize the file system.

```shell
    resize2fs /dev/vg_batches/czech_newspapers
```

Once that is done, remount the volume and you're good to go!

    mount /dev/vg_batches/czech_newspapers /batches/czech_newspapers/

