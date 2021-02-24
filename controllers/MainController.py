import re

from dash.dependencies import Input, Output, State, MATCH, ClientsideFunction
from flask import request

import views
from WebApp import WebApp
from config import INITIAL_LOCATION_ID, USER_ANGENT_REGEX
from controllers import get_page_route


@WebApp.callback(
	Output('page-content', 'children'),
	Output('page-nav', 'children'),
	Output('header', 'children'),
	Input('url', 'pathname'),
	State('page-nav', 'children'),
)
def page_to_render(pathname, menu_links):
	if pathname == '/' or pathname == '' or pathname == get_page_route(INITIAL_LOCATION_ID):
		header = views.InitView.header
		layout = views.InitView.layout
		actual_location = 'inicio'
	elif pathname == get_page_route('analisis-partidos'):
		header = None
		layout = views.PartyAnalysisView.layout
		actual_location = 'analisis-partidos'
	else:
		header = None
		layout = views.NotFoundView.layout
		actual_location = None

	for menu_item in menu_links:
		if menu_item['props']['id'] == actual_location:
			menu_item['props']['active'] = True
		else:
			menu_item['props']['active'] = False

	return layout, menu_links, header


@WebApp.callback(
	Output('mobile_device', 'data'),
	Input('url', 'pathname'),
	State('mobile_device', 'data')
)
def mobile_device(_, data):
	data = data or {
		'mobile_device': len(re.findall(USER_ANGENT_REGEX, request.headers['User_Agent'])) > 0
	}

	return data


@WebApp.callback(
	Output("navbar-collapse", "is_open"),
	Input("navbar-toggler", "n_clicks"),
	State("navbar-collapse", "is_open")
)
def toggle_navbar_collapse(n, is_open):
	if n:
		return not is_open
	return is_open


WebApp.clientside_callback(
	ClientsideFunction(
		namespace='clientside',
		function_name='collapse_function'
	),
	[
		Output({'type': 'collapsible-item', 'ref': MATCH}, "is_open"),
		Output({'type': 'collapse-icon', 'ref': MATCH}, "className")
	],
	Input({'type': 'collapse-button', 'ref': MATCH}, "n_clicks"),
	State({'type': 'collapsible-item', 'ref': MATCH}, "is_open"),
	prevent_initial_call=True
)