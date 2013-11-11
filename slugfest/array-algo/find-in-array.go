package main

import (
	"fmt"
)

func Min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

/**
 * Find the value in the array, returns the value's index.
 */
func FindValueInArray(value int, array []int) int {
	len := len(array)
	i := 0
	j := len

	for {
		m := array[(i+j)/2]
		if value < m {
			j = (j + i) / 2
		} else {
			i = (j + i) / 2
		}
		fmt.Print(i, j, "\n")
		if j-i == 1 {
			break
		}
	}
	if array[i] == value {
		return i
	} else if array[j] == value {
		return j
	}
	return -1
}

/**
 * Find mid value in two arrays, which has the same length, and ordered.
 * return the mid value
 */
func FindNthValueIn2Array(a []int, b []int) int {
	fmt.Print(a, b, "\n")
	if len(a) == 1 {
		return Min(a[0], b[0])
	}
	n := len(a)
	m := 0
	if n%2 == 0 {
		m = 1
	}
	h := n / 2
	m1 := a[h-m]
	m2 := b[h-m]

	if m1 < m2 {
		return FindNthValueIn2Array(a[h:n], b[0:n-h])
	}

	return FindNthValueIn2Array(a[0:n-h], b[h:n])
}

func main() {

	a := []int{1, 2, 3, 4, 5, 12}
	b := []int{6, 7, 8, 9, 10, 13}
	fmt.Print(FindNthValueIn2Array(a, b), "\n")

	a = []int{1, 2, 3, 4, 5, 12, 14}
	b = []int{6, 7, 8, 9, 10, 13, 15}
	fmt.Print(FindNthValueIn2Array(a, b), "\n")

	a = []int{1, 3, 5, 7, 9}
	b = []int{2, 4, 6, 8, 10}
	fmt.Print(FindNthValueIn2Array(a, b), "\n")

	a = []int{1, 3, 5, 7, 9, 11}
	b = []int{2, 4, 6, 8, 10, 12}
	fmt.Print(FindNthValueIn2Array(a, b), "\n")

	r := FindValueInArray(5, []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
	fmt.Print(r)
}
