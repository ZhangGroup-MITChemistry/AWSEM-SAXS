#include <cmath>
#include <ios>

#include "colvarmodule.h"
#include "colvarvalue.h"
#include "colvarparse.h"
#include "colvar.h"
#include "colvarcomp.h"

/*
 * pr_bias to bias toward SAXS data
 */

colvar::prbias::prbias (std::string const &conf)
    : cvc (conf)
{
    function_type = "prbias";
    atoms = parse_group (conf, "atoms");
    atom_groups.push_back (atoms);

    atoms->b_center = false;
    // N is number of atoms
    N = atoms->size();

    prbias_flag      = 0;

    // get prbias flag
    get_keyval (conf, "prbias",      prbias_flag, false);
    if (prbias_flag) cvm::log("PrBias flag on\n");

    if (prbias_flag)
        get_keyval (conf, "cutoff", cutoff, 1);

    // read in experimental p(r)
    std::string pr_file_name;
    std::string alpha_file_name;
    double temp;
    length=0;


    int counter=0; // Start at 1 to not divide by 0
    if ( get_keyval (conf, "PrFile", pr_file_name, std::string("")) ) {

        std::ifstream in_pr(pr_file_name.c_str());
        if (!in_pr.good()) cvm::fatal_error("Error: File pr_exp.dat can't be read!!! \n");
        while (in_pr >> temp) {//While loop to read in data
                if (length % 2 == 0) {
                    r.push_back(temp);
                } else {
                    f_exp.push_back(temp);
                };
                length++;
            }

        in_pr.close();
    } else {
        cvm::fatal_error ("Error: P(r) data file not set!!! \n");
    }

    if ( get_keyval (conf, "alpha", alpha_file_name, std::string("")) ) {

        std::ifstream in_alpha(alpha_file_name.c_str());
        if (!in_alpha.good()) cvm::fatal_error("Error: Alpha file can't be read!!! \n");
        int count=0;
        while (in_alpha >> temp) {//While loop to read in data
            alpha.push_back(temp);
        };
        in_alpha.close();
        if (alpha.size()!=length/2) cvm::fatal_error("Error: Alpha vector should be equal to the number of pr data points in the sample!!! \n");
    } else {
        cvm::fatal_error ("Error: P(r) alpha file not set!!! \n");
    }

if ( prbias_flag)
get_keyval (conf, "prindex", index, 1);  
r1=r[index];
interval=r[1]-r[0];
r2=r1+interval;
alpha1=alpha[index];


 x.type (colvarvalue::type_scalar);

}

colvar::prbias::prbias()
    : cvc ()
{ 
  function_type = "prbias";
  x.type (colvarvalue::type_scalar);
}

void colvar::prbias::calc_value()
{   
    x.real_value = 0.0;
    eta=7.0;

    // Calculate list of distances
    std::vector< double > dist_list;

    int i,j;
    for (i=0;i<N-1;i++) {
        for (j=i+cutoff;j<N;j++) {
            cvm::rvector const dx=(*atoms)[i].pos - (*atoms)[j].pos;
            double dist = sqrt(dx[0]*dx[0]+dx[1]*dx[1]+dx[2]*dx[2]);
            dist_list.push_back(dist);
        }
    }

    // Create histogram of experimental distances
    for (int i=0;i<dist_list.size();i++){
		if (dist_list[i] > r1-5.0 && dist_list[i] < r2+5.0) {
            x.real_value+=0.25*( ( 1.0+tanh ( eta* (dist_list[i]-r1) ) ) * ( 1.0+tanh(eta*(r2-dist_list[i]) ) ) );
        }
    }

}

void colvar::prbias::calc_gradients() {
    eta=7.0;

    double force_mag;
    for (int i = 0; i < N-1; i++) {
        for (int j = i + cutoff; j < N ; j++) {
                // Magnitude of the force is equal to the derivative of the potential
                cvm::rvector const dx = (*atoms)[i].pos - (*atoms)[j].pos;
                double dist = sqrt(dx[0]*dx[0]+dx[1]*dx[1]+dx[2]*dx[2]);
                if (dist > r1-5.0 && dist < r2+5.0) {
			    force_mag = alpha1 * 0.25 * eta * // (1/sum)*
                            (pow((1.0 / cosh(eta * (dist - r1))), 2) * (tanh(eta * (r2 - dist)) + 1) -
                             pow((1.0 / cosh(eta * (r2 - dist))), 2) * (tanh(eta * (dist - r1)) + 1));
}
else {
force_mag=0;
}
                (*atoms)[i].grad += force_mag * dx;
                (*atoms)[j].grad += -force_mag * dx;
        }
    }
}

void colvar::prbias::calc_force_invgrads()
{
    cvm::fatal_error ("Error: Inverse gradients for prbias is not implemented !!! \n");
}

void colvar::prbias::calc_Jacobian_derivative()
{
    cvm::fatal_error ("Error: Jacobian for prbias is not implemented !!! \n");
}

void colvar::prbias::apply_force (colvarvalue const &force)
{
    if (!atoms->noforce)
        atoms->apply_colvar_force (force.real_value);
}
