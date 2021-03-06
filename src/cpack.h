#include<iostream>

// how to use the program
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

// updating the flowers
void flowers_update(int interior, int boundary, double **flowers, double *a, int **complex)
{  
  for (int i = 0; i < interior; i++)
    for (int j = 0; j < interior + boundary - 1; j++)
      if (complex[i][j] >= 0)
	flowers[i][j] = a[complex[i][j]];
  }

// defining boundary conditions
double *boundary_fun(int boundary, double a[], int flag)
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

// calculating the value of the angle
double angle(double v, double u, double w)
{
  return 2 * asin(sqrt(u / (u + v) * w / (w + v))) * 180 / M_PI;
}

// evaluating the angle sum
double angle_sum(int interior, int boundary, int& rep, double a[], int index, double **b, double **angles)
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
