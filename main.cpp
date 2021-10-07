
#include <stdio.h>
#include <string.h>
// https://www.cplusplus.com/reference/functional/hash/
// https://www.cplusplus.com/reference/set/set/
// https://www.cplusplus.com/reference/queue/queue/
#include <vector>
#include <queue>
#include <functional>
#include <iostream>
#include <string>
#include <set>
#include <queue>

using namespace std;

template <typename T>
class HashSet: public set<int> {
    hash<T> m_hash;

public:
    bool insert(const T &x) {
        int h = m_hash(x);
        return set<int>::insert(h).second;
    }
};

class State {
public:
    string m_level;
    string m_path;
    int m_ppos;
    State(const string &level, const string &path, int ppos):m_level(level), m_path(path), m_ppos(ppos) {}
};

bool is_ok(const string &line) {
    return line.find('2') == string::npos;
}

char map_1(char a) {
    char r = 0;
    switch (a) {
        case '0':
            r = '2';
        break;
        case '2':
            r = '4';
        break;
        case '3':
            r = '5';
        break;
        case '4':
            r = '0';
        break;
        case '5':
            r = '6';
        break;
        case '6':
            r = '3';
        break;
    }
    return r;
}

char map_2(char a) {
    char r = 0;
    switch (a) {
        case '0':
            r = '4';
        break;
        case '3':
            r = '6';
        break;
        case '4':
            r = '0';
        break;
        case '6':
            r = '3';
        break;
    }
    return r;
}

void breadth_first_search(const char *level) {
    int ppos;
    for(int i = 0; i < 11 * 10; i++) {
        if (level[i] == '4' || level[i] == '6') {
            ppos = i;
            break;
        }
    }

    int dirs[] = {-10, 10, 1, -1};
    char cdirs[] = {'u', 'd', 'r', 'l'};
    queue<State> states;
    states.push(State(level, "", ppos));
    // set<string> visi;
    HashSet<string> visi;
    visi.insert(level);
    int c = 0;
    while (!states.empty()) {
        State &state = states.front();

        c ++;
        if (c % 100000 == 0) {
            printf("%04d\n", state.m_path.length());
        }

        for(int i = 0; i < 4; i++) {
            ppos = state.m_ppos;
            int cpos = ppos + dirs[i];
            int npos = cpos + dirs[i];
            if ((state.m_level[cpos] == '2' || state.m_level[cpos] == '5') && \
                (state.m_level[npos] == '0' || state.m_level[npos] == '3')) {
                string new_line(state.m_level);
                new_line[ppos] = map_1(new_line[ppos]);
                new_line[cpos] = map_1(new_line[cpos]);
                new_line[npos] = map_1(new_line[npos]);
                if (visi.insert(new_line)) {
                    string path(state.m_path);
                    path.push_back(cdirs[i]);

                    if(is_ok(new_line)) {
                        cout<<path<<endl;
                        return;
                    }

                    states.push(State(new_line, path, cpos));
                }
            } else if (state.m_level[cpos] == '0' || state.m_level[cpos] == '3') {
                string new_line(state.m_level);
                new_line[ppos] = map_2(new_line[ppos]);
                new_line[cpos] = map_2(new_line[cpos]);
                if (visi.insert(new_line)) {
                    string path(state.m_path);
                    path.push_back(cdirs[i]);
                    states.push(State(new_line, path, cpos));
                }
            }
        }
        states.pop();
    }
}

const char *level = "01111100000100011110010000001011105510101001505410100050111010011001001100000100013210010001001111000111100000";
// const char *level = "1111111111111111111111100011111110221111111420111111111001111111300111111330011111111111111111111111";


int main()
{
    breadth_first_search(level);
    return 0;
}
