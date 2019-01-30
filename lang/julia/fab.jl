


fab(::Val{1}) = 1
fab(::Val{2}) = 1
fab(::Val{N}) where N = fab(Val(N-1)) + fab(Val(N-2))
fab(x::Int) = fab(Val(x))

println(fab(100))
