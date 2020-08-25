#include<iostream>
#include<iomanip>
#include<cmath>
#include<cstdlib>
#include "cpack.h"

using namespace std;

// DIFFERENCES wrt cpack_01.cc:
// boundary conditions are here chosen randomly

// first of all we have to describe the complex K

const double A = 360; // fixing same branching for all the points at this stage (functions will require values in radians)

int main(int argc, char *argv[])
{
  // getting from stdin the structure of the complex
  int BOUNDARY = 0;
  int INTERIOR = 0;
  cin >> BOUNDARY;
  cin >> INTERIOR;

  // creating matrix where I will store the structure of the complex
  int **complex = new int*[INTERIOR];
  for (int i = 0; i < INTERIOR; i++)
    complex[i] = new int[INTERIOR + BOUNDARY - 1]; // maximum number of neighbors a vertex can have

  // initializing the complex
  for (int i = 0; i < INTERIOR; i++)
    for (int j = 0; j < INTERIOR + BOUNDARY -1; j++)
      {
	scanf("%d", &complex[i][j]);
	
	if (complex[i][j] < 0)
	  break;
      }

  // ------------------------------------------------------------------------
  
  int flag = 0;
  usage(flag, argc, argv);
  
  // printing number of internal and boundary vertices
  printf("%d %d\n", INTERIOR, BOUNDARY);
  
  double *vert = new double[BOUNDARY + INTERIOR]; // vertices array
  vert = boundary_fun(BOUNDARY, vert, flag); // imposing b.c. (the first vertices are boundary)

  // printing boundary conditions for the vertices (in order)
  for (int i = 0; i < BOUNDARY; i++)
    printf("%.3f ", vert[i]);
  printf("\n");
      
  // initializing internal labels
  for(int i = 0; i < INTERIOR; i++) 
    vert[BOUNDARY + i] = 1; 

  // creating flowers matrix
  double **flowers = new double*[INTERIOR];
  for (int i = 0; i < INTERIOR; i++)
    flowers[i] = new double[INTERIOR + BOUNDARY - 1]; // maximum number of neighbors a vertex can have

  // creating angles matrix
  double **angs = new double*[INTERIOR];
  for (int i = 0; i < INTERIOR; i++)
    angs[i] = new double[INTERIOR + BOUNDARY - 1]; // maximum number of neighbors a vertex can have

  // counting neighbours
  int n_neigh[INTERIOR] = {0}; 
  for (int i = 0; i < INTERIOR; i++)
    {
      int count = 0;
      for (int j = 0; j < INTERIOR + BOUNDARY - 1; j++)
	if (complex[i][j] >= 0)
	  count++;
	else
	  break;
      n_neigh[i] = count;
    }

  // printing neighbours for each internal vertex (in order)
  for (int i = 0; i < INTERIOR; i++)
    {
      for (int j = 0; j < n_neigh[i]; j++)
	printf("%d ", complex[i][j]);
      printf("\n");
    }

  //----------------------------------------------------

  int k = 0;
  double e = 0;
  double E = 1;
  double tolerance = pow(10., -3.);
  int call = 0;
  int j = 0;
  double sum = 0;

  do
    {
      j = 0;
      E = 0;
      sum = 0;

      for(j; j < INTERIOR; j++) // looping on the internal vertices
	{
	  flowers_update(INTERIOR, BOUNDARY, flowers, vert, complex);
	  sum = angle_sum(INTERIOR, BOUNDARY, k = 0, vert, j, flowers, angs);

	  // print the value of the radius for this flower
	  printf("%.5f\n", vert[BOUNDARY + j]);
	  
	  // print the vale of the angles for this flower
	  for (int a = 0; a < k; a++)
	    printf("%.5f ", angs[j][a]);
	  printf("\n");

	  // print the vale of the partial angle sum for this flower
	  double p_sum = 0;
	  for (int a = 0; a < k; a++)
	    {
	      printf("%.5f ", angs[j][a] + p_sum);
	      p_sum += angs[j][a];
	    }
	  printf("\n");
	    
	  //cerr << "Angle_Sum(" << j << "): " << sum;
	  //cerr << "  " << k << endl;

	  double beta = sin(sum / (2 * k) * M_PI / 180);
	  double delta = sin(A / (2 * k) * M_PI / 180);

	  double u = ((1 - delta) / delta) * (beta / (1 - beta)) * vert[BOUNDARY + j];
	  vert[BOUNDARY + j] = u; // updating label for that internal vertex

	  e += pow(sum - A, 2.);
	  
	}

      E = sqrt(e);

      //cerr << "\nError E = " << E << "\n" << endl;
      e = 0;
      call++;
            
    } while(E > tolerance);

  //cerr << "\nNumber of calls: " << call << endl;

  return 0;
}

