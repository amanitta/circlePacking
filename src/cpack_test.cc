#include<iostream>
#include<iomanip>
#include<cmath>
#include<cstdlib>

using namespace std;

// first of all we have to describe the complex K

const int interior = 9; // n. of interior vertices
const int boundary = 12; // n. of boundary vertices
const double A = 360; // fixing same branching for all the points at this stage (functions will require values in radians)

// The structure of the complex is hard-coded here
const int complex[interior][interior + boundary] = {
  // -1 to indicate the end of the array
  {0, 1, 13, 20, 19, 11, -1},
  {12, 1, 14, 20, -1},
  {1, 2, 3, 15, 20, 13, -1},
  {14, 3, 4, 5, 16, 20, -1},
  {20, 15, 5, 6, 7, 17, -1},
  {20, 16, 7, 18, -1},
  {19, 20, 17, 7, 8, 9, -1},
  {11, 12, 20, 18, 9, 10, -1},
  {12, 13, 14, 15, 16, 17, 18, 19, -1}
};

void flowers_update(double *flowers[interior + boundary - 1], double *a) // updating the flowers
{  
  for (int i = 0; i < interior; i++)
    for (int j = 0; j < interior + boundary - 1; j++)
      if (complex[i][j] >= 0)
	flowers[i][j] = a[complex[i][j]];
  }

double *boundary_fun(double a[], int flag) // defining boundary conditions
{  
  //srand48(time(NULL));
  srand48(123456);// 123 already shows 'problem' with the boundary

  for (int i = 0; i < boundary; i++)
    {
      double mult = 1;

      if (flag)
	mult = drand48();
      
      a[i] = 2 * mult;
    }
  
  return a;
}

double angle(double v, double u, double w)
{
  return 2 * asin(sqrt(u / (u + v) * w / (w + v))) * 180 / M_PI;
}

double angle_sum(int& rep, double a[], int index, double **b, double **angles)
{
  double sum = 0;
  int j;
  double ang;
  
  for(int i = 0; i < interior + boundary - 1; i++) // there won't be any vertex with more than (interior + boundary - 1) neighbours... not very pretty though
    {
      j = i;
      rep++; // this counts the number of neighbours 'processed'

      if (b[index][i + 1] == 0) // check if it is the last petal of the flower
	i = interior + boundary - 1;

      ang = angle(a[boundary + index], b[index][j], b[index][(i + 1) % (interior + boundary)]); // computing the angle
      sum += ang; // updating the sum
      
      angles[index][j] = ang; // updating the list of angles for the flower
    }
 
  return sum;
}

void usage(int &flag, int argc, char *argv[])
{
  if (argc > 1)
    {
      if (argv[1][0] == '-')
	{
	  switch (argv[1][1])
	    {
	    case 'r':
	      flag = 1;
	      break;
	    case 'f':
	      break;
	    default:
	      printf("USAGE: cpack [OPTION]\n-r for random boundary conditions\n-f for fixed boundary conditions (default)\n");
	      exit(-1);
	    }
	} else {
	printf("Use '-' before option parameter\n");
	exit(-1);
      }
    }

}

int main(int argc, char *argv[])
{
  int flag = 0;
  usage(flag, argc, argv);
  
  // printing number of internal and boundary vertices
  printf("%d %d\n", interior, boundary);
  
  double *vert = new double[boundary + interior]; // vertices array
  vert = boundary_fun(vert, flag); // imposing b.c. (the first vertices are boundary)

  // printing boundary conditions for the vertices (in order)
  for (int i = 0; i < boundary; i++)
    printf("%.3f ", vert[i]);
  printf("\n");
      
  // initializing internal labels
  for(int i = 0; i < interior; i++) 
    vert[boundary + i] = 1; 

  // creating flowers matrix
  double **flowers = new double*[interior];
  for (int i = 0; i < interior; i++)
    flowers[i] = new double[interior + boundary - 1]; // maximum number of neighbors a vertex can have

  // creating angles matrix
  double **angs = new double*[interior];
  for (int i = 0; i < interior; i++)
    angs[i] = new double[interior + boundary - 1]; // maximum number of neighbors a vertex can have

  // counting neighbours
  int n_neigh[interior] = {0}; 
  for (int i = 0; i < interior; i++)
    {
      int count = 0;
      for (int j = 0; j < interior + boundary - 1; j++)
	if (complex[i][j] >= 0)
	  count++;
	else
	  break;
      n_neigh[i] = count;
    }

  // printing neighbours for each internal vertex (in order)
  for (int i = 0; i < interior; i++)
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

      for(j; j < interior; j++) // looping on the internal vertices
	{
	  flowers_update(flowers, vert);
	  sum = angle_sum(k = 0, vert, j, flowers, angs);

	  // print the value of the radius for this flower
	  printf("%.5f\n", vert[boundary + j]);
	  
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

	  double u = ((1 - delta) / delta) * (beta / (1 - beta)) * vert[boundary + j];
	  vert[boundary + j] = u; // updating label for that internal vertex

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

