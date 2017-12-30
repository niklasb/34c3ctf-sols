let plain = _ARY5_
let tables = _ARY6_
tables.push(_ARY7_)

let sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11];
let shift_rows = ary => sr.map(i => ary[i]);

let t1 = _ARY1_
let t2 = _ARY2_
let t3 = _ARY3_
let t4 = _ARY4_

let mix = x => [
    t1[x[0]] ^ t2[x[15]] ^ t3[x[10]] ^ t4[x[5]],
    t1[x[5]] ^ t2[x[0]] ^ t3[x[15]] ^ t4[x[10]],
    t1[x[10]] ^ t2[x[5]] ^ t3[x[0]] ^ t4[x[15]],
    t1[x[15]] ^ t2[x[10]] ^ t3[x[5]] ^ t4[x[0]],

    t1[x[4]] ^ t2[x[3]] ^ t3[x[14]] ^ t4[x[9]],
    t1[x[9]] ^ t2[x[4]] ^ t3[x[3]] ^ t4[x[14]],
    t1[x[14]] ^ t2[x[9]] ^ t3[x[4]] ^ t4[x[3]],
    t1[x[3]] ^ t2[x[14]] ^ t3[x[9]] ^ t4[x[4]],

    t1[x[8]] ^ t2[x[7]] ^ t3[x[2]] ^ t4[x[13]],
    t1[x[13]] ^ t2[x[8]] ^ t3[x[7]] ^ t4[x[2]],
    t1[x[2]] ^ t2[x[13]] ^ t3[x[8]] ^ t4[x[7]],
    t1[x[7]] ^ t2[x[2]] ^ t3[x[13]] ^ t4[x[8]],

    t1[x[12]] ^ t2[x[11]] ^ t3[x[6]] ^ t4[x[1]],
    t1[x[1]] ^ t2[x[12]] ^ t3[x[11]] ^ t4[x[6]],
    t1[x[6]] ^ t2[x[1]] ^ t3[x[12]] ^ t4[x[11]],
    t1[x[11]] ^ t2[x[6]] ^ t3[x[1]] ^ t4[x[12]]]

let block = plain;
for (let r = 0; r < 9; ++r) {
  block = block.map((i, x) => tables[r][x][i]);
  block = mix(block)
}
block = shift_rows(block);
block = block.map((i, x) => tables[9][x][i]);
console.log(block);

let pos = 0; // execute once for 0, 1, 2, 3
for (let dfa = 0; dfa < 40; ++dfa) {
  // DFA attack
  block = plain;
  for (let r = 0; r < 9; ++r) {
    block = block.map((i, x) => tables[r][x][i]);
    block = mix(block)
    if (r == 7)
      block[pos] = (
        Math.floor(Math.random()*256));
  }
  block = shift_rows(block);
  block = block.map((i, x) => tables[9][x][i]);
  foo.append(plain + ' ' + block + '\n')
}
