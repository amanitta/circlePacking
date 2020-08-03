#include<iostream>
#include<iomanip>
#include<cmath>

using namespace std;

// devo innanzitutto descrivere il complesso K da cui parto: qua stabilisco solo n. di vertici interni ed esterni, il resto definito nel main

const int interior = 9;
const int boundary = 12;
const double A = 360; // metto branching uguale ad ogni punto, qua uso gradi ma funzioni richiederanno poi radianti

void boundary_fun(double a[]) // mi pone le condizioni al bordo
{
  for(int i = 0; i < boundary; i++)
    {
      a[i] = 2;
    }
}

double angle(double v, double u, double w)
{
  return 2 * asin(sqrt(u/(u + v) * w/(w + v))) * 180 / M_PI;
}

double angle_sum(int& rep, double vint[], int vin, double b[][10])
{
  double sum = 0;
  
  for(int i = 0; i < 100; i++)
    {
      if(b[vin][i + 1] == 0)
	{
	  rep++;
	  sum += angle(vint[vin],b[vin][i],b[vin][0]);
	  //cout << rep << "  " << vin << "  " << vint[vin] << "  " << b[vin][i] << "  " << b[vin][i+1] << "  " << setw(8) << angle(vint[vin],b[vin][i],b[vin][i+1]) << "  " << setw(8) << sum << endl;
	   
	  i = 100;

	}
      else
	{
	  rep++;
	  sum += angle(vint[vin],b[vin][i],b[vin][i+1]);

	  //cout << rep << "  " << vin << "  " << vint[vin] << "  " << b[vin][i] << "  " << b[vin][i+1] << "  " << setw(8) << angle(vint[vin],b[vin][i],b[vin][i+1]) << "  " << setw(8) << sum << endl;
	}
    }
 
  return sum;
}


int main()
{

  double R[boundary + interior] = {0}; // label di partenza

  for(int i = 0; i < boundary + interior; i++) 
    R[i] = 1; // inizializzo tutto il label a 1

  boundary_fun(R); // pongo le condizioni al contorno

  double bd[boundary]; // vettore dei vertici esterni

  for(int i = 0; i < boundary; i++)
    {
      bd[i] = R[i];
    }

  double in[interior]; // vettore dei vertici interni

  cout << "Raggi interni iniziali: " << endl;
  for(int i = 0; i < interior; i++) 
    {
      in[i] = R[boundary + i];
      cout << in[i] << endl;
    }
  cout << "\n" << endl;  

  //----------------------------------------------------

  int k = 0;
  double e = 0;
  double E = 1;
  double tolerance = pow(10.,-3.);
  int call = 0;
  int j = 0;

  while(E > tolerance)
    {
      j = 0;
      E = 0;

      for(j; j < interior; j++) // ciclo sui vertici interni
	{

	  double flower[interior][10] =
	    {
	      {bd[0],in[1],in[4],in[5],bd[10],bd[11]},
	      {bd[1],bd[2],in[2],in[4],in[0],bd[0]},
	      {bd[2],bd[3],bd[4],in[3],in[4],in[1]},
	      {in[2],bd[4],in[8],in[4]},
	      {in[1],in[2],in[3],in[8],in[7],in[6],in[5],in[0]},
	      {in[0],in[4],in[6],bd[10]},
	      {in[5],in[4],in[7],bd[8],bd[9],bd[10]},
	      {in[4],in[8],bd[6],bd[7],bd[8],in[6]},
	      {in[3],bd[4],bd[5],bd[6],in[7],in[4]}
	    }; // vettore (matrice) dei fiori, metto qui dentro perche' almeno viene ogni volta modificata quando cambio i raggi
	    
	  cout << "Angle_Sum(" << j << "): " << angle_sum(k = 0,in,j,flower);
	  cout << "  " << k << endl;

	  double beta = sin(angle_sum(k = 0,in,j,flower)/(2 * k)*M_PI/180);
	  double delta = sin(A / (2 * k)*M_PI/180);

	  double u = ((1 - delta)/delta) * (beta/(1 - beta)) * in[j];
	  in[j] = u;

	  e += pow(angle_sum(k = 0,in,j,flower) - A, 2.);
	  
	}

      E = sqrt(e);

      cout << "\nErrore E = " << E << "\n" << endl;
      e = 0;
      call++;
            
    }

  cout << "\nRaggi interni finali:" << endl; 
  for(int i = 0; i < interior; i++) 
    {
      cout << setprecision(5) << setw(5) << in[i] << endl;
    }
  cout << "\nNumero di chiamate: " << call << endl;

  return 0;
}

