from config import PAGE_ROUTES, CUSTOM_STYLES, TOPIC_NAMES, ROOT_DIR


def rgb_to_rgba(rgb_value, alpha):
	return f"rgba{rgb_value[3:-1]}, {alpha})"


def generate_css_colors():
	import os
	style = ''

	for idx, topic in enumerate(TOPIC_NAMES):
		style += f'.Select-value[title={filter_special_characters(topic)}] {{\n' \
						f'    background-color: {TOPIC_NAMES[topic]}; \n' \
						f'}}\n\n' \
						f'.Select-value[title={filter_special_characters(topic)}] > .Select-value-icon {{\n' \
						f'    background-color: inherit;\n' \
						f'    border-right: none;\n' \
						f'}}\n\n' \
						f'.Select-value[title={filter_special_characters(topic)}] > .Select-value-label {{\n' \
						f'    background-color: rgb(255 255 255 / 80%);\n' \
						f'}}\n\n'

	with open(os.path.join(ROOT_DIR, CUSTOM_STYLES), 'a') as writer:
		writer.write(style)


def get_page_name(id):
	for page in PAGE_ROUTES:
		if page['id'] == id:
			return page['name']


def get_page_route(id):
	for page in PAGE_ROUTES:
		if page['id'] == id:
			return page['route']


def decompose_callback(callback):
	decomposed_callback = []

	for component in callback:
		component_parts = component.split('.')
		component_id, component_property = component_parts[0], component_parts[1]
		property_value = callback[component]

		if len(callback) > 1:
			decomposed_callback.append({
				'id': component_id,
				'property': component_property,
				'value': property_value
			})
		else:
			decomposed_callback = {
				'id': component_id,
				'property': component_property,
				'value': property_value
			}

	return decomposed_callback


if __name__ == "__main__":
	generate_css_colors()