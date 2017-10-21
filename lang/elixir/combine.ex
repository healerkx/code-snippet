defmodule Combine do

  def combine([]), do: []

  def combine([a]), do: [[a]]

  def combine([a, b]), do: [[], [a], [b], [a,b]]

  def combine(a)  when is_list(a) do
    [head | tail] = a

    s = combine(tail)

    w = Enum.map(s, fn(x)->[head] ++ x end)

    w ++ s

  end

  def start(_, _) do
    'ABCDEF' |> Hello.combine |> IO.inspect 
    {:ok, self()}
  end

end
