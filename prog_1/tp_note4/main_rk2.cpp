#include <iostream>
#include <cmath>
using namespace std;

#include "class_rk2_ode.hpp"

double f(double t, double x) 
{
  return x*(1 - exp(t))/(1 + exp(t));
}

double x(double t) 
{
  return 12*exp(t)/(pow((1+exp(t)),2));
}

// Fonction qui affiche l'erreur numerique
double numerical_error(double t_ini,double t_end,size_t N,double* resultat, double x_0){
  double h = (t_end - t_ini)/N;
  double t_k;
  double sum = 0.;
  for (int kk=1;kk<N+1;kk++){
      t_k = t_ini + kk*h;
      sum += abs(x(t_k)-resultat[kk]); // resultat[kk] correspond donc à x_k
  }
  return sum;
}



int main()
{

  // EXPLICIT RK2 METHOD
  double t_init = 0.;
  double t_max  = 2.;
  double x_init = 3.;

  size_t N = 100;

  rk2_odeSolver test(t_init, x_init, t_max, f);
  double* soln = test.solve_equation(N);

  double erreur = numerical_error(t_init,t_max,N,soln,x_init);
  
  N = 1000;
  rk2_odeSolver test2(t_init, x_init, t_max, f);
  double* soln2 = test2.solve_equation(N);
  double erreur2 = numerical_error(t_init,t_max,N,soln2,x_init);

  // L'erreur est bien en h2
  cout << "Erreur N=100 " << erreur << endl;
  cout << "Erreur N=1000 " << erreur2 << endl;


  delete[] soln;
  delete[] soln2;
}
