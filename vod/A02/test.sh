
#!/bin/sh
 
[ ! -d $PWD ] && mkdir -p $PWD && exit 1
 
for count in `seq 100`
do
    touch $PWD/linux-$count
done
