package gpass

import (
    "fmt"
    "time"

	"html/template"
    "net/http"
    //"appengine"
    //"appengine/datastore"
    //"appengine/user"
)

type Entry struct {
    Name		string
    Value		string
    Comment  	string
    Date 		time.Time
}




func init() {
    http.HandleFunc("/", handler)
    http.HandleFunc("/list", list)
    http.HandleFunc("/addnew", addnew)
    http.HandleFunc("/add", add)
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, world!")
}

func list(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Show list")
}



func addnew(w http.ResponseWriter, r *http.Request) {
	t := template.New("addnew")
	t, err := t.ParseFiles("./templates/addnew.tmpl")
	if err != nil {
		fmt.Fprint(w, err)
	}

	err = t.ExecuteTemplate(w, "addnew.tmpl", nil)
	if err != nil {
		fmt.Fprint(w, err)
	}
}

func add(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Add entry")
}