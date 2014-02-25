package gpass

import (
    "fmt"
    "time"

    "html/template"
    "net/http"
    "appengine"
    "appengine/datastore"
    "appengine/user"
)

type Entry struct {
    Name		string
    Value		string
    Comment  	string
    Date 		time.Time
}

func init() {
    http.HandleFunc("/h", handler)
    http.HandleFunc("/add", add)    
}

func handler(w http.ResponseWriter, r *http.Request) {

    c := appengine.NewContext(r)
    u := user.Current(c)

    if u == nil || u.Email != "healer.kx.yu@gmail.com" {
        loginUrl, _ := user.LoginURL(c, "h")
        c.Infof("User =: %v", u)
        http.Redirect(w, r, loginUrl, http.StatusMovedPermanently)
        return
    }

    t := template.New("gpass template")
    t, err := t.ParseFiles("templates/gpass.html")

    if err != nil {
        fmt.Fprint(w, "Error: %v", err)
    }

    logoutUrl, _ := user.LogoutURL(c, "/")

    query := datastore.NewQuery("Entry")
    var entries []Entry
    _, qe := query.GetAll(c, &entries)

    if qe == nil {
        vars := map[string]interface{} {
            "email": u.Email,
            "items": entries,
            "logoutUrl": logoutUrl,
        }

        err = t.ExecuteTemplate(w, "gpass.html", vars)
        if err != nil {
            fmt.Fprint(w, "Error: %v", err)
        }
    }
}

func add(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    e := Entry{
        Name:       r.FormValue("name"),
        Value:      r.FormValue("value"),
        Comment:    r.FormValue("comment"),
        Date:       time.Now(),
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








