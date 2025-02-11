#pragma once
#include<iostream>
using namespace std;

double euler_method( double t_ini, double i_sol, double t_end, double (*sfn)(double t, double x), size_t N);