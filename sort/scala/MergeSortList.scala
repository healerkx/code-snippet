

object MergeSort {

   def msort[T](less: (T, T) => Boolean)(xs: List[T]): List[T] = { 
        def merge(xs: List[T], ys: List[T], acc: List[T]): List[T] = 
            (xs, ys) match { 
            case (Nil, _) => ys.reverse ::: acc 
            case (_, Nil) => xs.reverse ::: acc
            case (x :: xs1, y :: ys1) => 
                if (less(x, y)) merge(xs1, ys, x :: acc) 
                else merge(xs, ys1, y :: acc) 
            }
        
        val n = xs.length / 2 
        if (n == 0) 
            xs 
        else {
            val (ys, zs) = xs splitAt n 
            merge(msort(less)(ys), msort(less)(zs), Nil).reverse
        } 
    } 
    
    def main(args: Array[String]): Unit = {
        // println("Hello, world!")
        val comp = (a: Int, b : Int) => a < b
        val l = List(1, 2, 4, 5, 6, 7, 3, 0, 9, 8)
        val imsort =  msort(comp)_
        println(imsort(l))
    }
}


