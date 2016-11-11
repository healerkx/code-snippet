

object MergeSort {

    def printArray(a: Array[Int]) {
        a.foreach((x) => print(x + " "))
    }

    // b is the temp space for sorting
    def merge(a: Array[Int], b: Array[Int], first: Int, mid: Int, last: Int) {
        var i = first
        var j = mid
        var k = 0
        // Merge into a new array from two array
        while (i < mid && j < last) {
            if (a(i) < a(j)) {
                b(k) = a(i)
                i += 1
            } else {
                b(k) = a(j)
                j += 1
            }
            k += 1
        }
        
        // copy the remains to the new array's tail
        while (i < mid) {
            b(k) = a(i)
            k += 1; i += 1
        }

        while (j < last) {
            b(k) = a(j)
            k += 1; j += 1
        }

        // Write the sorted sequence back
        var v = 0
        while (v < k) {
            a(first+ v) = b(v)
            v += 1
        }
    }

    def sort(a: Array[Int], b: Array[Int], first: Int, last: Int) {
        if (first + 1 < last) {
            val mid = (first + last) / 2
            sort(a, b, first, mid)
            sort(a, b, mid, last)
            
            merge(a, b, first, mid, last)
        }
    }



    def main(args: Array[String]): Unit = {
        
        val l = List(1, 2, 4, 3, 5, 8, 6, 7, 0, 9, 10, 12, 11, 1, 2, 3)
        var unsorted = l toArray
        var sorted = l.toArray.clone
        sort(unsorted, sorted, 0, l.length)

        printArray(unsorted)
        print("\n")
        printArray(sorted)
        
    }
}


