#include <iostream>
#include<bits/stdc++.h>

using namespace std;

int main() {
    string str;
    cin>>str;
    int longest = 1, curr = 1;
    for(int i=1; i<str.length(); i++){
        (str[i]==str[i-1])?curr++:curr=1;
        longest = max(curr, longest);
    }
    cout<<longest;
}