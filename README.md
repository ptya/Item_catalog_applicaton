# Item Catalog Udacity Project :star:
This is my Item Catalog project for Udacity's Full Stack Developer Nanodegree.

It is a Python web application using the [Flask](http://flask.pocoo.org/) framework along with [SQLAlchemy](https://www.sqlalchemy.org/) for an items catalog.
In it you can view categories and related items.

Once logged in you can create, edit and delete items.

Front-end was built for mobile first.

For best experience, use [Google Chrome](https://www.google.com/chrome/browser/desktop/index.html). :stuck_out_tongue_winking_eye:

#### It features:
- CSRF protection
- Flask-login based login module
- OAUTH signup with:
  - Facebook
  - Google
  - Github
- Image upload
- JSON API endpoints

#### 3rd party modules:
- [Flask WTF](https://flask-wtf.readthedocs.io/en/stable/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Bootstrap 3.1.1](http://getbootstrap.com/)
- [Font Awesome](http://fontawesome.io/)
- [Social Buttons for Bootstrap](https://lipis.github.io/bootstrap-social/)
- [jQuery 1.8.2](https://jquery.com/)

#### Default image references:
- [Item description image](https://pixabay.com/hu/tan%C3%BAs%C3%ADtv%C3%A1ny-pap%C3%ADr-pergamen-tekercs-154169/)
- [User avatar image](https://pixabay.com/hu/avat%C3%A1r-bbs-%C3%A9rzelmek-gui-ikon-2029980/)


# Installation :coffee:
### Prerequisites: :video_game:
- [Installed VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Installed Vagrant](https://www.vagrantup.com/downloads.html)
- [Registered Facebook App for OAUTH](https://developers.facebook.com/apps/)
- [Registered Github App for OAUTH](https://developer.github.com/apps/building-integrations/setting-up-and-registering-github-apps/registering-github-apps/)
- [Registered Google App for OAUTH](https://console.developers.google.com/apis/dashboard)

## First time setup :boom:
#### Environment setup
1. Clone the repository
2. Using your console `cd` into the repository's directory
3. Use `vagrant up` :exclamation: __Note:__ this can take a few minutes
4. The VM needs a restart once setup - use `vagrant halt` to stop the VM
5. Use `vagrant up` again to start the VM
6. Lastly, install Flask-WTF with `sudo pip install Flask-WTF`


#### Application setup
1. Using your console `cd` into the repository's directory
2. Start the VM using `vagrant up`
3. SSH into your VM using `vagrant ssh`
4. `cd` into the app folder as `/vagrant/catalog`
5. Create the dummy DB using `python setup.py`


#### Login system setup
1. Open `/vagrant/catalog/instance/fb_client_secret.json` with your editor
2. Enter your `app_id` and `app_secret` for Facebook login and save
3. Open `/vagrant/catalog/instance/gh_client_secret.json` with your editor
4. Enter your `client_id` and `client_secret` for Github login and save
5. Open `/vagrant/catalog/instance/goo_client_secret.json` with your editor
6. Enter your `client_id`, `project_id` and `client_secret` for Google login and save

In case you'd like to modify the DB items, edit `setup.py` file

# Usage :computer:
0. Make sure your application is setup (check __First time setup__ step above)
1. Using your console `cd` into the repository's directory
2. Start the VM using `vagrant up`
3. SSH into your VM using `vagrant ssh`
4. `cd` into the app folder as `/vagrant/catalog`
5. Launch the application using `python run.py`
6. In your browser open http://localhost:8000/catalog


## JSON API endpoints
#### Category listing
Open `http://localhost:8000/catalog/categories/JSON` to see the list of categories.

##### Structure
```
{
  "categories": [
    {
      "id": 1,
      "name": "Armor"
    },
    ...
  ]
}
```
#### Item listing for given category
Open `http://localhost:8000/catalog/<category_name>/items/JSON` where `category_name` is an existing category's name.

##### Structure
```
{
  "items": [
    {
      "category": "Jewelry",
      "description": "It induces honesty, induces wakefulness, aids certain skin problems,     and enhances the sense of touch.",
      "id": 1,
      "image": null,
      "name": "Longevity Canopic Jar"
    },
    ...
  ]
}
```
#### Item information listing
Open `http://localhost:8000/catalog/<category_name>/<item_name>/JSON` where `category_name` is an existing category's name and `item_name` is an existing item's name of that category.

##### Structure
```
{
  "item": [
    {
      "category": "Jewelry",
      "description": "It wards off nightmares.",
      "id": 35,
      "image": null,
      "name": "Fortitude Sword"
    }
  ]
}
```

# License :trollface:
Copyright (c) 2017 Péter Szabó. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
