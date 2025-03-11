#pragma once

class point
{
protected:
    static const int Ndim=2;
    double coord[Ndim];
public:
    // get coordinates
    double icord(int ii) const;
    static const int getNdim() { return Ndim;}

    // setters
    void zero();
    void set(int i, const double& a);

    // Constructors
    point(double xx);
    point(double coo[Ndim]);
    point();
    point(const point& p); // Constructor copy

    // Destructor
    ~point();

    const point& operator=(const point& p);  //Definir un point à partir d'un autre

    const double operator[](int i) const; // read ieme coord
    double& operator[]( int i );  // Assign ieme coord

    friend const point operator-(const point& p); // Donne -la valeur du point donné en entrée
    friend const point operator+(const point& p); // Donne valeur absolue du point donné en entrée

    const point& operator+=(const point& p);
    const point& operator-=(const point& p); 

    friend const point operator+(const point& p, const point& q); // Sum of two point
    friend const point operator-(const point& p, const point& q); // Subtract

};