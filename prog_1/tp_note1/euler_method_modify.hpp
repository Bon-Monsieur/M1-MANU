#pragma once
#include<iostream>
using namespace std;

void euler_method_modify( double t_ini, double i_sol, double t_end, double (*sfn)(double t, double x), size_t N,double* resultat);