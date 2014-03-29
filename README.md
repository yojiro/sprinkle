sprinkle
========

# what it is.

very simple solenoid driver for automatic splinkling


# requirement

- rasberry pi
- solenoid driver cirtucit like that
```
   raspberry pi
 --GPIO port 25
      |  
      +---3.3Kohm----LED --------+
      |                          | 
      |          +------+       ===GND
      |          |      |
      +-4.7Kohm--+1    6+-----------------------+
                 |      |                       | 
            +----+2    4+-+-o  o---+---o+  -o---+
            |    |      | | 24Vout |   24Vin    |
           ===   +------+ |        |            | 
           GND            |        |   +        |
                          +-Diode--+---||-------+---+ 
                            A   K     cap 100uF     |
                                      50V          ===GND 

  --GPIO port 23 ---+---10Kohm --- VCC
                    |
                   switch
                    |
                   === GND

 = Opt MOS relay: AQV215 or compatible

```

# how to use

## test
- just run it.
- if you want to specify sprinking time, use -t option.
 
## dairy operation
- locate this scrpit to proper location (e.g. /usr/local/bin)
- edit crontab like `0 7 * * *       root    cd / && /usr/local/bin/sprinkle -t 60 &` 
- check /var/log/message 




