#include<iostream>
#include<string>
using namespace std;
struct Student
{
    string name;
    int age;
};

int main()
{
    int aaqq = 122;
    int xaxa = 234;
    if(aaqq==xaxa)
    	aaqq = -xaxa;
    	if(xaxa==32)
    		xaxa=33;
    	else
    		xaxa=10001;
    cout<<aaqq<<endl;

    return 0;
}