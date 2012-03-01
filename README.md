# plumbum - pb

Python 3.x based pastebin implementation.

## Dependencies

* [Pygments](http://pygments.org/)
* [Bottle](http://bottlepy.org/docs/dev/)
* [Kyoto Cabinet](http://fallabs.com/kyotocabinet/)

## Authors

Initially developed at [FIXME](http://hackerspaces.org/wiki/FIXME) the Lausanne
hackerspace during [First Coding Night](https://fixme.ch/wiki/CodingNight1).

gcmalloc <gcmalloc@gmail.com>
Valentin Haenel <valentin.haenel@gmx.de>
Nicholas Wolff <nwolff@gmail.com>
Dan Kalotay <d.kalotay@gmail.com>
Rorist <aubort.jeanbaptiste@gmail.com>
carre <carre@lenimac15.(none)>
speredenn <jbc@gmx.se>

## Installation

Bottle is provided with the framework. Pygments and Kyoto are optional. If
Pygments can not be found, no coloring is provided. If Kyoto can not be found a
simple in-memory dictionary is used for storage.

## Running

Just run:

    ./plumbum.py

This will attempt to start the http and socket servers using a suitable configuration.
The http server WON'T support load, you should go to apache as the default one is just a dev http.
