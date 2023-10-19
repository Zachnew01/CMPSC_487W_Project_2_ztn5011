# -------------------------------------------
#
# CMPSC 487W - Project 2 - Web-based generic item management system
#
# Zachary T. Newman
#
# -------------------------------------------


# -=- Import Statements -=-


from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename


# -=- Global Variables and Initialization


app = Flask(__name__) # Flask Initialization

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ztn5011SQL'
app.config['MYSQL_DB'] = 'websystem'
mysql = MySQL(app)
print("Connected to Database\n")

img = os.path.join('static','Image')

app.config['UPLOAD'] = img


# -=- CRUD Functions -=-


def browseItems(crsr, sortType, search):
    ''' Returns a list of the results of a selection statement based on the type of sort and the search value provided'''
    if(search == ""): # If there is no search term
        if(sortType == 0): # No sort
            sql = "SELECT * FROM items"
            crsr.execute(sql)
            items = crsr.fetchall()
            return items
        elif(sortType == 1): # Sort by ID increasing
            sql = "SELECT * FROM items ORDER BY ID ASC"
            crsr.execute(sql)
            items = crsr.fetchall()
            return items
        elif(sortType == 2): # Sort by ID decreasing
            sql = "SELECT * FROM items ORDER BY ID DESC"
            crsr.execute(sql)
            items = crsr.fetchall()
            return items
        elif(sortType == 3): # Sort by Name increasing
            sql = "SELECT * FROM items ORDER BY name ASC"
            crsr.execute(sql)
            items = crsr.fetchall()
            return items
        elif(sortType == 4): # Sort by Name decreasing
            sql = "SELECT * FROM items ORDER BY name DESC"
            crsr.execute(sql)
            items = crsr.fetchall()
            return items
        else:
            print("Invalid Input")
            return False
    else: # If there is a search term
        search = "%" + search + "%"
        if(sortType == 0): # No sort w/ search term
            sql = "SELECT * FROM items WHERE ID LIKE %s OR name LIKE %s OR description LIKE %s"
            sqlInput = (search, search, search)
            crsr.execute(sql,sqlInput)
            items = crsr.fetchall()
            return items
        elif(sortType == 1): # Sort by ID increasing w/ search term
            sql = "SELECT * FROM items WHERE ID LIKE %s OR name LIKE %s OR description LIKE %s ORDER BY ID ASC"
            sqlInput = (search, search, search)
            crsr.execute(sql,sqlInput)
            items = crsr.fetchall()
            return items
        elif(sortType == 2): # Sort by ID decreasing w/ search term
            sql = "SELECT * FROM items WHERE ID LIKE %s OR name LIKE %s OR description LIKE %s ORDER BY ID DESC"
            sqlInput = (search, search, search)
            crsr.execute(sql,sqlInput)
            items = crsr.fetchall()
            return items
        elif(sortType == 3): # Sort by Name increasing w/ search term
            sql = "SELECT * FROM items WHERE ID LIKE %s OR name LIKE %s OR description LIKE %s ORDER BY name ASC"
            sqlInput = (search, search, search)
            crsr.execute(sql,sqlInput)
            items = crsr.fetchall()
            return items
        elif(sortType == 4): # Sort by Name decreasing w/ search term
            sql = "SELECT * FROM items WHERE ID LIKE %s OR name LIKE %s OR description LIKE %s ORDER BY name DESC"
            sqlInput = (search, search, search)
            crsr.execute(sql,sqlInput)
            items = crsr.fetchall()
            return items
        else:
            print("Invalid Input")
            return False
            # Invalid Input
# End of Browse Items


def addItem(crsr, name, description, image):
    ''' Inserts a new item with a sequential ID and the given values.
        Returns True if the addition was successful, False otherwise.'''
    sql = "INSERT INTO items (name, description, image) VALUES(%s, %s, %s)"
    sqlInput = (name, description, image)
    crsr.execute(sql,sqlInput)
    mysql.connection.commit()
    return True
# End of Add Item


def removeItem(crsr, ID):
    ''' Removes an item from items with the given ID.
        Returns True if the removal was successful, False otherwise.'''
    if(ID != None):
        sql = "DELETE FROM items WHERE ID = %s"
        sqlInput = (ID,)
        crsr.execute(sql,sqlInput)
        mysql.connection.commit()
        return True
    else:
        return False

# End of Remove Item


def editItem(crsr, ID, updateType, newValue):
    ''' Updates the updateType field to the given newValue of the item with the given ID.
        Returns True if the edit was successful, False otherwise.'''
    if(ID != None):
        if(updateType == 'name'):
            sql = "UPDATE items SET name = %s WHERE ID = %s"
            sqlInput = (newValue, ID)
            crsr.execute(sql,sqlInput)
            mysql.connection.commit()
            return True
        elif(updateType == 'description'):
            sql = "UPDATE items SET description = %s WHERE ID = %s"
            sqlInput = (newValue, ID)
            crsr.execute(sql,sqlInput)
            mysql.connection.commit()
            return True
        elif(updateType == 'image'):
            sql = "UPDATE items SET image = %s WHERE ID = %s"
            sqlInput = (newValue, ID)
            crsr.execute(sql,sqlInput)
            mysql.connection.commit()
            return True
        else:
            return False
    else:
        return False
# End of Edit Item


# -=- FLASK Stuff -=-


@app.route('/', methods =['GET', 'POST'])
def mainpage():
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
    if request.method == 'POST' and 'sortType' in request.form and 'search' in request.form:
        # mainpage if sort/search
        sortType = int(request.form['sortType'])
        search = request.form['search']
        items = browseItems(crsr, sortType, search)
        if(items):
            crsr.close()
            return render_template('mainpage.html',items=items)
    # Default mainpage
    items = browseItems(crsr, 0, "")
    crsr.close()
    return render_template('mainpage.html',items=items)
# End of mainpage


@app.route('/add', methods =['GET', 'POST'])
def addpage():
    feedback = ""
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        # addpage if attempting to add an item
        name = request.form['name']
        description = request.form['description']
        imageFile = request.files['imageFile']
        image = secure_filename(imageFile.filename)

        if(name != "" and description != "" and image != ""):
            addItem(crsr, name, description, image)
            imageFile.save(os.path.join(app.config['UPLOAD'], image))
            feedback = "Add Successful"
        else:
            feedback = "Add Unsuccessful"

    crsr.close()
    return render_template('addPage.html',feedback=feedback)
# End of addpage


@app.route('/edit', methods =['GET', 'POST'])
def editpage():
    feedback = ""
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        # editpage if attempting to edit an item
        ID = request.form['id']
        name = request.form['name']
        description = request.form['description']
        imageFile = request.files['imageFile']
        image = secure_filename(imageFile.filename)

        # Verify ID exists
        sql = "SELECT * FROM items WHERE ID = %s"
        sqlInput = (ID,)
        crsr.execute(sql,sqlInput)
        item = crsr.fetchone()
        
        if(item != None): # Edits values only if ID is valid
            # Name Editting
            if(name != ""):
                editItem(crsr,ID,'name',name)
                feedback = feedback + "Name Edit Success "

            # Description Editting
            if(description != ""):
                editItem(crsr,ID,'description',description)
                feedback = feedback + "Description Edit Success "

            # Image Editting
            if(image != ""):
                editItem(crsr,ID,'image',image)
                imageFile.save(os.path.join(app.config['UPLOAD'], image))
                feedback = feedback + "Image Edit Success "
        else:
            feedback = "Edit Unsuccessful - Invalid ID"

    crsr.close()
    return render_template('editPage.html',feedback=feedback)
# End of editpage


@app.route('/remove', methods =['GET', 'POST'])
def deletepage():
    feedback = ""
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        # deletepage if attempting to delete an item
        ID = request.form['id']

        # Verify ID exists
        sql = "SELECT * FROM items WHERE ID = %s"
        sqlInput = (ID,)
        crsr.execute(sql,sqlInput)
        item = crsr.fetchone()

        if(item != None): # Removes the item only if ID is valid
            if (removeItem(crsr,ID)):
                feedback = "Item Removed Successfully"
            else:
                feedback = "Item Removed Unsuccessfully"
        else:
            feedback = "Item Removed Unsuccessfully - Invalid ID"

    crsr.close()    
    return render_template('deletepage.html',feedback=feedback)
# End of deletepage


if __name__ == '__main__': # "Main" Method
    app.run()
# End of "Main" method
