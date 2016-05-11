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
    int a = 1>=2;
    int b = 2;
    if(a==b)
    	a = -b;
    	if(b==3)
    		b=3;
    	else
    		b=1;
    cout<<"HelloWorld"<<endl;

    Student* student;
    cout<<student->name>>endl;
    return 0;
}