/***************************************************************************************************
 *
 * Copyright (C) 2017 Fabrice Salvaire
 * Contact: http://www.fabrice-salvaire.fr
 *
 * This file is part of CodeReview.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

/**************************************************************************************************/

#include <string.h>
#include <stdio.h>

/**************************************************************************************************/

int
min2(int a, int b)
{
  return a <= b ? a : b;
}

int
min3(int a, int b, int c)
{
  return min2(a, min2(b, c));
}

/**************************************************************************************************/

// https://en.wikipedia.org/wiki/Levenshtein_distance

// Fixme: Check code !!!

int
levenshtein_distance(const char * string1, const char * string2)
{
  int length_string1 = strlen(string1);
  int length_string2 = strlen(string2);

  // Check for empty string
  if (length_string1 == 0)
    return length_string2;
  if (length_string2 == 0)
    return length_string1;

  int distance_matrix[length_string1 + 1][length_string2 + 1];
  memset(distance_matrix, 0, (length_string1 + 1)*(length_string2 + 1));

  // source prefixes can be transformed into empty string by dropping all characters
  for (int i = 1; i <= length_string1; i++)
    distance_matrix[i][0] = i;

  // target prefixes can be reached from empty source prefix by inserting every character
  for (int j = 1; j <= length_string2; j++)
    distance_matrix[0][j] = j;

  const int equal_cost = -1; // To favour long match
  const int substitution_cost = 1;
  const int deletion_cost = 1;
  const int insertion_cost = 1;

  for (int j = 1; j <= length_string2; j++)
    for (int i = 1; i <= length_string1; i++) {
      int cost = string1[i-1] == string2[j-1] ? equal_cost : substitution_cost;
      int value = min3(distance_matrix[i-1][j] + deletion_cost,
                       distance_matrix[i][j-1] + insertion_cost,
                       distance_matrix[i-1][j-1] + cost
                       );
      distance_matrix[i][j] = value;
    }

  /*
  for (int i = 0; i <= length_string1; i++) {
    printf("%i| ", i);
    for (int j = 0; j <= length_string2; j++)
      printf("%i ", distance_matrix[i][j]);
    printf("\n");
  }
  */

  return distance_matrix[length_string1][length_string2];
}

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
