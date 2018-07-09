**UPDATE:** I uploaded sources & exploit for the WCTF version of the challenge to https://github.com/niklasb/elgoog/

There were (at least) two bugs:

1. Pool overflow when compressing an index, if a posting list has duplicate
   entries. In elgoog1, this overflow was unbounded, but in elgoog2, it was
   only a one-byte overflow.

2. Type confusion between compressed and uncompressed index in
   `elgoog_compress_index()`. It didn't check the flag.
   This was unintended and [exploited by shiki7][1] from Tea Deliverers to solve
   both challenges (it is harder in elgoog2 though due to low integrity).

Will release my exploit for the first bug soon, once I cleaned it up a bit.

[1]: https://gist.github.com/marche147/6e7bb92d376a0f209b1b301aff418e88
