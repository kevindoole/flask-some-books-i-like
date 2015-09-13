## Some books I like
This little app enables you to keep track of books you like, because how
the heck are you supposed to do that without a Flask app?

I mean, you could likely use "Some books I like" to keep track of anything
you like, although since I've embedded things like Title, Author and the word
"Book" all over the place, it might be confusing for other stuff. Whatever, I
don't care. Do what you want.

-

### Installation
If you're still here, you're clearly satisfied with the "why" and are now
likely wondering how you can use "Some books i like."

First things first, make sure you have VirtualBox and Vagrant installed:
- [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Install Vagrant](https://www.vagrantup.com/downloads.html)

All good? Ok, now download the repo and start up the virtual machine:
```bash
$ git clone https://github.com/kevindoole/flask-some-books-i-like
$ cd flask-some-books-i-like
$ vagrant up
```
The `vagrant up` command boots up the VM and create a database that will
store your books. It also seeds a bit of data so I can share some books that I
like. I did not bother to include images for all of these books, but you're
more than welcome to rummage around the internet and fill them in. (But that
would be weird if you did that.) I did include a single image for example
purposes, but didn't bother loading all images into this repo.

For the next few steps, you'll need to ssh into the VM:
```bash
$ vagrant ssh
### <bunch of output> ###
vagrant@vagrant-ubuntu-trusty-32:~$ # this is your command prompt inside the VM
```

If you don't care to see my book list, you're more than welcome to clean out
the database so you can start fresh.
```bash
vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/catalog/
vagrant@vagrant-ubuntu-trusty-32:~$ python
> from cat_app import db
> db.drop_all()
> db.create_all()
> exit()
```
You can reload all my books at anytime by running
`python /vagrant/catalog/seed.py`

Ok, all set to load the app now. Just run
`python /vagrant/catalog/run_server.py` and visit
[http://localhost:8000](http://localhost:8000).

### Running the tests
It's pretty easy:
```
vagrant@vagrant-ubuntu-trusty-32:~$ python /vagrant/catalog/testCatalog.py
```


-

### Stuff to do inside the app

- [view a list of all the books](http://localhost:8000)
- [view lists of categories of books](http://localhost:8000/catalog/programming/items)
- [view individual books](http://localhost:8000/catalog/programming/extreme-programming-explained)
- [log in with Google+ (Oath2)](http://localhost:8000/login)
- [log out](http://localhost:8000/logout)
- [edit books and their images](http://localhost:8000/catalog/the-mythical-man-month/edit)
- [create books with images](http://localhost:8000/catalog/create-product)
- [delete books](http://localhost:8000/catalog/the-mythical-man-month/delete)
- [look at a json representation of all the books](http://localhost:8000/catalog.json)
- [look at an Atom representation of all the books](http://localhost:8000/catalog.atom)
- don't even bother trying to CSRF into this app; it's airtight :facepunch:

:grin: **Enjoy!** :grin:
