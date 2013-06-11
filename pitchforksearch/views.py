from pitchforksearch import app

from flask import request, redirect, flash

#use mako instead of jinja2 (its less ugly)
from flask.ext.mako import MakoTemplates,render_template

from flask.ext.wtf import Form
from wtforms import fields, validators

import MySQLdb as mdb
import MySQLdb.cursors as cursors

#TODO 
# 1. source control
# 2. sorting 
# 3. separate artist per table
# 4. about page
# 5. message when zero results
# 6. WTForms
# 7. sqlalchemy

# mako initilization
app.template_folder = "templates"
mako = MakoTemplates(app)

class SearchForm(Form):
    artist = fields.TextField("Artist")
    score_lower = fields.DecimalField("Score Lower Limit", [validators.NumberRange(min=0.0, max=10.0)], 
    	places=1, default=0.0)
    score_upper = fields.DecimalField("Score Upper Limit", [validators.NumberRange(min=0.0, max=10.0)], 
    	places=1, default=10.0)
    sort_option = fields.RadioField("Sort by:", choices=[("date_reviewed","Date"),("score","Score")],
    	default='date_reviewed')
    table_per_artist = fields.BooleanField("One table per artist")

@app.route('/', methods=("GET", "POST"))
def index():
	# limit to 100 results
	limit = 100

	form = SearchForm(csrf_enabled=True)
	if form.validate_on_submit():
		flash("Success")

		columns = ['Score', 'Artist', 'Album', 'BNM', 'Date Reviewed', 'Link']
	
		artists = [x.strip() for x in form.artist.data.split(',')]
		search_results = []
		titles = []

		cur = connect_db()

		for artist in artists:
			q = build_query(artist, form.sort_option.data, form.score_lower.data, form.score_upper.data, limit)
			status,stuff = execute_query(q, cur)
			#return str(stuff)

			if(status):
				search_results.append(stuff)
				titles.append('Results for artist names containing: "%s"' % (artist))
			else:
				return stuff

		return render_template('table.html', result_set = search_results, columns=columns, titles=titles,
				form=form)

	else:
		return render_template('layout.html', form=form)

def build_query(artist, sort_option, score_lower, score_upper, limit):
	q = "select score,artist,album,flag,date_reviewed,url from ratings"
	if(artist == '*'):
		q += " where"
	else:
		q += " where artist like '%%%s%%' and" % (artist)
	q += " score >= %s and score <= %s" % (score_lower, score_upper)
	q += " order by artist,%s" % (sort_option)
	q += " limit %d" % limit
	return q

def execute_query(query, cur):
	try:
		# skip first line
		cur.execute(query)
		results = cur.fetchall()
		return True,results

	except mdb.Error, e:

		err="Error %d: %s" % (e.args[0],e.args[1])
		return False,err + query

def connect_db():
	con = mdb.connect(app.config['HOST'], app.config['DBUSER'], 
		app.config['DBPASS'], app.config['DBNAME'], charset='utf8')
	#, cursorclass=cursors.OrderedDictCursor)
	cur = con.cursor()
	return cur
