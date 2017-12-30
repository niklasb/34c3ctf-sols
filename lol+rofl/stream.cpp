#include <bits/stdc++.h>
using namespace std;

struct RNG {
    random_device dev;
    mt19937_64 rng;
    RNG() : dev(), rng(dev()) {}
    RNG(uint64_t seed) : rng(seed) {}

    bool next_bit() { return rng() & 1; }

    // For when we want to hide the RNG state
    uint64_t next_qword_safe() {
        uint64_t res = 0;
        for (int i = 0; i < 64; ++i)
            res |= next_bit() << i;
        return res;
    }

    // For when we don't care about security
    uint64_t next_qword_fast() {
        return rng();
    }
};

int main() {
    RNG rng(0);
    for (;;)
        cout << rng.next_qword_fast() << endl;
}
