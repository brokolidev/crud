from flask import Flask, render_template, url_for, request, redirect, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Restaurant CRUD
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        return redirect('/restaurant/new')
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit',  methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    edit_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_restaurant.name = request.form['name']
            session.add(edit_restaurant)
            session.commit()
            return redirect('/')
        else:
            return "Error occured"
        return "edited"
    else:
        return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant=edit_restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    delete_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(delete_restaurant)
        session.commit()
        return redirect('/')
    else:
        return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant=delete_restaurant)

# Menu CRUD
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, menu=menu)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['POST', 'GET'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            new_menu = MenuItem(name=request.form['name'], restaurant_id=restaurant.id)
            session.add(new_menu)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    edit_menu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_menu.name = request.form['name']
            session.add(edit_menu)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', menu=edit_menu, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    delete_menu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(delete_menu)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', menu=delete_menu, restaurant_id=restaurant_id)

# JSON API
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant)
    return jsonify(restaurants=[i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/JSON')
def showMenuJSON(restaurant_id):
    memu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(menu=[i.serialize for i in memu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuInfoJSON(restaurant_id, menu_id):
    memu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id)
    return jsonify(memu=[i.serialize for i in memu])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
