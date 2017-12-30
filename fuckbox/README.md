Solution:

1. `python2 solve.py` will produce `payload2.js`
2. `js-beautify payload2.js > payload3.js`
3. Manually added EXPR X ... END markers to payload3.js
4. `python2 solve2.py` will produce `payload4{,_vars}.js`
5. Copied and reversed in payload5.js
6. Open `fault.html` in browser to run DFA attack in payload5.js
   with different `pos` values (0,1,2,3),
   copy text output to traces.txt, run `python3 crack.py` each time, note
   results in reverse.py
7. Run `python2 reverse.py` and enjoy
