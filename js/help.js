var count;
var files = Array()

function main() {
    count = 0
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    ul = document.getElementById("sul");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i]
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().includes(filter)) {
            count += 1
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    document.getElementById("counter").innerText = `${count} items found`
}

function init() {
    let mylist = document.getElementById("sul")
    
    //This should make it location-proof
    let theurl = window.location.pathname
    let stheurl = theurl.split("/")
    if (theurl.endsWith("index.html")) {
        stheurl.pop()//Remove index.html if necessary
    }
    stheurl.push("/api/get_all_help_titles.php")
    let thenewurl = stheurl.join("/").replace("///","/").replace("//","/")//Re-join URL
    //alert(thenewurl)
    fetch(thenewurl).then(function(r) {
        r.text().then(function(t) {
            let ti = 0;
            t.split("``").forEach(ele => {
                let tz = ti
            
                if (ele === "") {
                    //Rubbish
                } else {
                    let elex = ele.split(";;")//Returned as title;;filename``title;;filename...
                    files.push(elex[1])
                    let li = document.createElement("li")
                    li.innerText = elex[0]
                    li.onclick = function() {
                        loadhelp(tz)//This should lock the locator position.
                    }
                    mylist.appendChild(li)//Add list option

                    ti++
                    
                }
            })
            document.getElementById("counter").innerText = `${ti} items found`
            count = ti
            document.getElementById("waiter").hidden = true
        })
    })  
}

function loadhelp(loc) {
    let filename = files[loc]
    //I sure love copied codes
    let theurl = window.location.pathname
    let stheurl = theurl.split("/")
    if (theurl.endsWith("index.html")) {
        stheurl.pop()//Remove index.html if necessary
    }
    stheurl.push(`/api/get_help.php?name=${filename}`)
    
    let thenewurl = stheurl.join("/").replace("///","/").replace("//","/")//Re-join URL
    fetch(thenewurl).then(function(r) {
        r.text().then(function(t) {
            document.getElementById("help").innerHTML = t
            document.getElementById("helpertut").hidden = true
            unfade(document.getElementById("help"))
        })
    })
}
var fready = false
//The following code is completely copied from SO!
function fade(element) {
    fready = false
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1){
            fready = true
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}
function unfade(element) {
    var op = 0.1;  // initial opacity
    element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}