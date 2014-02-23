package gpass

import (
    "fmt"
    "time"

	"html/template"
    "net/http"
    "appengine"
    "appengine/datastore"
    //"appengine/log"
    "appengine/user"
)

type Entry struct {
    Name		string
    Value		string
    Comment  	string
    Date 		time.Time
}




func init() {
    http.HandleFunc("/", welcome)
    http.HandleFunc("/list", list)
    http.HandleFunc("/addnew", addnew)
    http.HandleFunc("/add", add)
}

func welcome(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    u, err := user.CurrentOAuth(c, "")
    url, err := user.LoginURL(c, "list")
    if err != nil {
        fmt.Fprintf(w, "<a href='%s'>%s</a>", url, "Login")
        return
    }
    if !u.Admin {
        // http.Error(w, "Admin login only", http.StatusUnauthorized)
        fmt.Fprintf(w, "<a href='%s'>%s</a>", url, "Login")
        return
    }
    fmt.Fprintf(w, `Welcome, admin user %s!`, u)
}

func list(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    u, _ := user.CurrentOAuth(c, "")

    c.Infof("Current Account: %v", u.Email)
    if u.Email != "healer.kx.yu@gmail.com" {
        url, _ := user.LoginURL(c, "list")
        http.Redirect(w, r, url, http.StatusMovedPermanently)
        // fmt.Fprintf(w, "<a href='%s'>%s</a>", url, "Login")
        return
    }

    t := template.New("listall")
    t, err := t.ParseFiles("templates/listall.html")
    if err != nil {
        fmt.Fprint(w, err)
    }
    
    err = t.ExecuteTemplate(w, "listall.html", u)
    if err != nil {
        fmt.Fprint(w, err)
    }}



func addnew(w http.ResponseWriter, r *http.Request) {
	t := template.New("addnew")
	t, err := t.ParseFiles("templates/addnew.html")
	if err != nil {
		fmt.Fprint(w, err)
	}

	err = t.ExecuteTemplate(w, "addnew.html", nil)
	if err != nil {
		fmt.Fprint(w, err)
	}
}

func add(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    e := Entry{
        Name:   r.FormValue("name"),
        Value:  r.FormValue("value"),
        Comment:    r.FormValue("comment"),
        Date:   time.Now(),
    }
    key := datastore.NewKey(c, "Entry", "default_entry", 0, nil)
    key = datastore.NewIncompleteKey(c, "Entry", key)
    _, err := datastore.Put(c, key, &e)
    if err != nil {
        fmt.Fprint(w, r.FormValue("name"))
    } else {
        fmt.Fprint(w, key)
    }
	
}








