// RandomChainTest.cpp automatically generated by bin/add_new_algorithm.pl
// in Mon Feb 13 22:37:25 2017.

//
// RandomChainTest.cpp -- implementation of the namespace "RandomChainTest".
//
//    This file is part of the featsel program
//    Copyright (C) 2016 Marcelo S. Reis
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#include "RandomChainTest.h"

namespace RandomChainTest
{

  bool it_should_store_all_the_visited_subsets ()
  {
    ElementSet set ("S1", 3, 1);    // |S1| = 3
    RandomChain t;
    string list;
    SubsetSum c (&set);
    t.set_parameters (&c, &set, true);
    t.get_minima_list (1);
    list = t.print_list_of_visited_subsets ();

    //
    // For 2^3 it should have 4 elements, including the empty set and the
    // complete set!
    //
    if ((list.find ("<000>") != string::npos) &&
        (list.find ("<111>") != string::npos))
      return true;
    else
      return false;
  }


  bool it_should_give_the_number_of_the_visited_subsets ()
  {
    ElementSet set ("S1", 3, 1);    // |S1| = 3
    RandomChain t;
    SubsetSum c (&set);
    t.set_parameters (&c, &set, true);
    t.get_minima_list (1);
    if (t.get_list_of_visited_subsets ()->size () == 4)
      return true;
    else
      return false;
  }


} // end of namespace
