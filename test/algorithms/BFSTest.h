//
// BFSTest.h -- definition of the namespace "BFSTest".
//
//    This file is part of the featsel program
//    Copyright (C) 2017  Marcelo S. Reis
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

#ifndef BFSTEST_H_
#define BFSTEST_H_

#include "../../src/algorithms/BFS.h"
#include "../../src/functions/CFS.h"

namespace BFSTest
{

  bool it_should_store_all_the_visited_subsets ();

  bool it_should_give_the_number_of_the_visited_subsets ();

}

#endif /* BFSTEST_H_ */
