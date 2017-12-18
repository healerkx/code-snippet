package main


type I interface {
	f()
}

type Aa struct {

}
type Bb struct {

}

func (a *Aa) f() {
	print("A")
}

func (a *Bb) f() {
	print("B")
}

func Get() I {
	if !true {
		return &Aa{}	
	} else {
		return &Bb{}	
	}
}

func main() {
	var a I = Get()
	a.f()
}
